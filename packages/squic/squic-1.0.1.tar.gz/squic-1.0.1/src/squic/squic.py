# SQUIC
#
# Copyright (C) Aryan Eftekhari
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from ctypes import *
import numpy as np
import sys
from scipy.sparse import csr_matrix, identity

lib_custom_location = os.environ.get("SQUIC_LIB_PATH", os.getenv('HOME'))

squic_libs = {
    "darwin" : "libSQUIC.dylib",
    "linux" : "libSQUIC.so"
}

dll = None
try:
    dll = CDLL(os.path.join(lib_custom_location, squic_libs[sys.platform]))
except KeyError:
    raise Exception("#SQUIC: OS not supported.")
except OSError as e:
    print(e)
    print("SQUIC library not found, please use SQUIC_LIB_PATH env variable!!")
    exit(1)

def run(Y:np.array, l:float, max_iter:int=100, tol:float=1e-3,verbose:int=1, M:np.array=None, X0:np.array=None, W0:np.array=None)->list:
    """SQUIC is a second-order, L1-regularized maximum likelihood method for performant large-scale sparse precision matrix estimation.
See help(squic) for further details. Note: If max_iter=0, the returned value for the inverse of the precision matrix (W) is the sparse sample covariance matrix (S).

    Args:
        Y (np.array): Input data in the form p (dimensions) by n (samples).
        l (float): Scalar tuning parameter λ>0.
        max_iter (int, optional): Maximum number of Newton iterations of the outer loop. Defaults to 100.
        tol (float, optional): Tolerance for convergence and approximate inversion. Defaults to 1e-3.
        verbose (int, optional): Level of printing output (0 or 1). Defaults to 1.
        M (np.array, optional):  Defines the penalty matrix parameters where Λ_ij = M_ij if M_ij ≠ 0 else λ. Defaults to Zeros (denoted by None).
        X0 (np.array, optional): Initial guess of the precision matrix Θ. Defaults to Identity (denote by None).
        W0 (np.array, optional): Initial guess of the inverse of the precision matrix W=inv(Θ). Defaults to Identity (denote by None).

    Returns:
        list->[X,W,info_times,info_objective,info_logdetX,info_trSX]:
        - X: Estimated precision matrix.
        - W: Estimated inverse of the precision matrix.
        - info_times: Component runtimes times.
            info_times[0]: Total runtime.
            info_times[1]: Runtime of the sample covariance matrix.
            info_times[2]: Runtime of the Newton steps.
            info_times[3]: Runtime of the Cholesky factorization.
            info_times[4]: Runtime of the approximate matrix inversion.
            info_times[5]: Runtime of the coordinate descent update.
        - info_objective: Objective at each iteration.
        - info_logdetX: Log-determinant of the estimated precision matrix.
        - info_trSX: Trace of the sample covariance matrix times the final estimate precision matrix.
    """
    if(dll is None):
        print(f"Error loading the SQUIC library: {squic_libs[sys.platform]}")
        exit(1)

    p,n= Y.shape

    if(p<3):
        raise ValueError("#SQUIC: number of random variables (p) must larger than 2");

    if(n<2):
        raise ValueError("#SQUIC: number of samples (n) must be larger than 1 .");

    if(l<=0):
        raise ValueError("#SQUIC: lambda must be great than zero.");

    if(max_iter<0):
        raise ValueError("#SQUIC: max_iter cannot be negative.");

    if(tol<=0):
        raise ValueError("#SQUIC: tol must be great than zero.");

    #################################################
    # if mode = [0,1,2,3,4] we Block-SQUIC or [5,6,7,8,9] Scalar-SQUIC
    mode  = c_int(0)

    # The data needs to be fortran (column major)
    Y     = np.array(Y,order='F')
    Y_ptr = Y.ctypes.data_as(POINTER(c_double))

    #################################################
    # tolerances
    # Hard code both tolerances to be the same
    term_tol = tol
    inv_tol  = tol

    #################################################
    # Matrices
    #################################################

    # X & W Matrix Checks
    if(X0 is None or W0 is None ): 
        # Make identity sparse matrix.
        X0= identity(p, dtype='float64', format='csr')
        W0= identity(p, dtype='float64', format='csr')
    else:
        
        X0 = csr_matrix(X0)
        W0 = csr_matrix(W0)
        
        X0.eliminate_zeros()
        W0.eliminate_zeros()

        # Check size
        [X0_p,X0_n]=X0.shape
        if(X0_p!=p or X0_n!=p ):
            raise TypeError("#SQUIC: X0 must be square matrix with size pxp.")

        # Check size
        [W0_p,W0_n]=W0.shape
        if(W0_p!=p or W0_n!=p ):
            raise TypeError("#SQUIC: W0 must be square matrix with size pxp.")    

        # Force Symmetric
        X0=(X0+X0.T)/2;
        W0=(W0+W0.T)/2;

    #################################################
    # Allocate data fo X
    #################################################
    X_rinx = POINTER(c_long)()
    X_cptr = POINTER(c_long)()
    X_val  = POINTER(c_double)()
    X_nnz  = c_long(X0.nnz)

    # Use the SQUIC_CPP utility function for creating and populating data buffers.
    # This makes creating and delete buffers consistent.
    # All SQUIC datastructions are 64 bit! Thus we need to cast the CSR index buffers to int64
    dll.SQUIC_CPP_UTIL_memcopy_integer(byref(X_rinx) , np.int64(X0.indices).ctypes.data_as(POINTER(c_long))  , X_nnz       )
    dll.SQUIC_CPP_UTIL_memcopy_integer(byref(X_cptr) , np.int64(X0.indptr).ctypes.data_as(POINTER(c_long))   , c_long(p+1) )
    dll.SQUIC_CPP_UTIL_memcopy_double( byref(X_val)  , X0.data.ctypes.data_as(POINTER(c_double))             , X_nnz       )

    #################################################
    # Allocate data fo W
    #################################################
    W_rinx = POINTER(c_long)()
    W_cptr = POINTER(c_long)()
    W_val  = POINTER(c_double)()
    W_nnz  = c_long(W0.nnz)

    dll.SQUIC_CPP_UTIL_memcopy_integer(byref(W_rinx) , np.int64(W0.indices).ctypes.data_as(POINTER(c_long))  , W_nnz       )
    dll.SQUIC_CPP_UTIL_memcopy_integer(byref(W_cptr) , np.int64(W0.indptr).ctypes.data_as(POINTER(c_long))   , c_long(p+1) )
    dll.SQUIC_CPP_UTIL_memcopy_double( byref(W_val)  , W0.data.ctypes.data_as(POINTER(c_double))             , W_nnz       )

    #################################################
    # Check and Allocated data for M
    #################################################
    M_rinx = POINTER(c_long)()
    M_cptr = POINTER(c_long)()
    M_val  = POINTER(c_double)()

    if(M is None):
        M_nnz  = c_long(0)
    else:
        
        M = csr_matrix(M)
        M.eliminate_zeros()
        
        # Check size
        [M_p,M_n]=M.shape
        if(M_p!=p or M_n!=p ):
            raise Exception("#SQUIC: M must be square matrix with size pxp..")    

        # Make all postive, drop all zeros and force symmetrix
        M.eliminate_zeros()
        M = abs(M)
        M = (M + M)/2

        M_nnz  = c_long(M.nnz)
        dll.SQUIC_CPP_UTIL_memcopy_integer(byref(M_rinx) , np.int64(M.indices).ctypes.data_as(POINTER(c_long))  , M_nnz       )
        dll.SQUIC_CPP_UTIL_memcopy_integer(byref(M_cptr) , np.int64(M.indptr).ctypes.data_as(POINTER(c_long))   , c_long(p+1) )
        dll.SQUIC_CPP_UTIL_memcopy_double( byref(M_val)  , M.data.ctypes.data_as(POINTER(c_double))             , M_nnz       )


    #################################################
    # Parameters
    #################################################
    max_iter_ptr  = c_int(max_iter);
    term_tol_ptr  = c_double(term_tol);
    inv_tol_ptr  = c_double(inv_tol);
    verbose_ptr   = c_int(verbose)

    p_ptr    = c_long(p)
    n_ptr    = c_long(n)
    l_ptr    = c_double(l)

    #################################################
    # Information output buffers
    #################################################
    info_num_iter_ptr    = c_int(-1);
    info_logdetX_ptr     = c_double(-1);
    info_trSX_ptr        = c_double(-1);

    info_times_ptr = POINTER(c_double)()
    dll.SQUIC_CPP_UTIL_memset_double(byref(info_times_ptr),c_int(6))

    info_objective_ptr = POINTER(c_double)()
    dll.SQUIC_CPP_UTIL_memset_double(byref(info_objective_ptr),max_iter_ptr)

    #################################################
    # Run SQUIC
    #################################################
    dll.SQUIC_CPP(mode,
        p_ptr, n_ptr, Y_ptr,
        l_ptr,
        M_rinx, M_cptr, M_val, M_nnz,
        max_iter_ptr, inv_tol_ptr, term_tol_ptr, verbose_ptr,
        byref(X_rinx), byref(X_cptr), byref(X_val), byref(X_nnz),
        byref(W_rinx), byref(W_cptr), byref(W_val), byref(W_nnz),
        byref(info_num_iter_ptr),
        byref(info_times_ptr),     # length must be 6: [time_total,time_impcov,time_optimz,time_factor,time_aprinv,time_updte]
        byref(info_objective_ptr), # length must be size max_iter
        byref(info_logdetX_ptr),
        byref(info_trSX_ptr))


    #################################################
    # Transfer Restusl from C to Python
    #################################################

    #Convert all scalars values back python
    p               = p_ptr.value
    X_nnz           = X_nnz.value
    W_nnz           = W_nnz.value
    info_num_iter   = info_num_iter_ptr.value
    info_logdetX    = info_logdetX_ptr.value
    info_trSX       = info_trSX_ptr.value

    # Transfer Matrix from C to Python
    # First we link the C buffer to a numpy array, than we make CSR matrix using a Copy of the array.

    X_rinx_py   =np.ctypeslib.as_array(X_rinx,(X_nnz,))
    X_cptr_py   =np.ctypeslib.as_array(X_cptr,(p+1,))
    X_val_py    =np.ctypeslib.as_array(X_val,(X_nnz,))
    X           =csr_matrix((X_val_py, X_rinx_py, X_cptr_py),shape=(p, p),copy=True)

    W_rinx_py   =np.ctypeslib.as_array(W_rinx,(W_nnz,))
    W_cptr_py   =np.ctypeslib.as_array(W_cptr,(p+1,))
    W_val_py    =np.ctypeslib.as_array(W_val,(W_nnz,))
    W           =csr_matrix((W_val_py, W_rinx_py, W_cptr_py),shape=(p, p),copy=True)

    if(info_num_iter==0):
        info_objective=np.array(-1)
    else:
        temp            =np.ctypeslib.as_array(info_objective_ptr,(info_num_iter,))
        info_objective  =np.array(temp,copy=True)

    temp            =np.ctypeslib.as_array(info_times_ptr,(6,))
    info_times      =np.array(temp,copy=True)

    #################################################
    # Transfer results from C to Python
    #################################################
    dll.SQUIC_CPP_UTIL_memfree_integer(byref(X_rinx))
    dll.SQUIC_CPP_UTIL_memfree_integer(byref(X_cptr))
    dll.SQUIC_CPP_UTIL_memfree_double(byref(X_val))

    dll.SQUIC_CPP_UTIL_memfree_integer(byref(W_rinx))
    dll.SQUIC_CPP_UTIL_memfree_integer(byref(W_cptr))
    dll.SQUIC_CPP_UTIL_memfree_double(byref(W_val))

    if( not (M is None) ) :
        dll.SQUIC_CPP_UTIL_memfree_integer(byref(M_rinx))
        dll.SQUIC_CPP_UTIL_memfree_integer(byref(M_cptr))
        dll.SQUIC_CPP_UTIL_memfree_double(byref(M_val))

    if(info_num_iter>0):    
        dll.SQUIC_CPP_UTIL_memfree_double(byref(info_objective_ptr))

    dll.SQUIC_CPP_UTIL_memfree_double(byref(info_times_ptr))

    return [X,W,info_times,info_objective,info_logdetX,info_trSX]
