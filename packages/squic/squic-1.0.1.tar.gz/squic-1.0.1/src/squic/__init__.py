"""
#################
# Description:
#################

SQUIC is a second-order, L1-regularized maximum likelihood method for performant large-scale sparse precision matrix estimation.


#################
# Usage :
#################

[X,W,info_times,info_objective,info_logdetX,info_trSX]=SQUIC.run(Y, lambda, max_iter = 100, tol = 1e-3, verbose = 1, M = NULL,  X0 = NULL, W0 = NULL)
[_,S,info_times,_,_,_]=SQUIC.run(Y, lambda, max_iter = 0)

Arguments:
    Y:          Input data in the formp(dimensions) x n(samples).
    l:          Scalar tuning parameter a non-zero positive number.
    max_iter:   Maximum number of Newton iterations.
    tol:        Tolerance for convergence and approximate inversion.
    verbose:    Level of printing output (0 or 1).
    M:          A symmetric sparse (p by p); See note (3) below for details.
    X0:         Initial value of precision matrix as a sparse matrix (p x p) .
    W0:         Initial value of inverse precision matrix as a sparse matrix (p x p) ..

NOTE:
(1) If max_iter=0, the returned value for the inverse of the precision matrix (W) is the sparse sample covariance matrix (S).
(2) The number of threads used by SQUIC can be defined by setting the enviroment variable OMP_NUM_THREADS (e.g., base> export OMP_NUM_THREADS=12). This may require a restart of the session).
(3) The matrix tuning paramter Lambda:=M_{ij} for M_{ij} != 0 and Lambda_{ij}:=lambda, if otherwise. When M=NULL we have Lambda_{ij}=lambda.
(4) After importing the package the user must set the path of the shared library libSQUIC.*, using function SQUIC.PATH_TO_libSQUIC().

Return values:

 X: Estimated precision matrix (p x p).
 W: Estimated inverse of the precision matrix (p x p).
 S: Sparse (threashold) sample covariance matrix (p x p).
 info_times: Total runtime.
    [0] info_time_total: Total runtime.
    [1] info_time_sample_cov: Runtime of the sample covariance matrix.
    [2] info_time_optimize: Runtime of the Newton steps
    [3] info_time_factor: Runtime of the matrix factorization.
    [4] info_time_approximate_inv: Runtime of the approximate matrix inversion.
    [5] info_time_coordinate_upd: Runtime of the coordinate descent update.
 info_objective: Objective value at each Newton iteration.
 info_logdetX: Log determinant of the estimated precision matrix.
 info_trSX: Trace of the sample covariance matrix times the estimated precision matrix.

#################
# References :
#################

Bollhöfer, M., Eftekhari, A., Scheidegger, S. and Schenk, O., 2019. Large-Scale Sparse Inverse Covariance Matrix Estimation.
SIAM Journal on Scientific Computing, 41(1), pp.A380-A401.

Eftekhari, A., Bollhöfer, M. and Schenk, O., 2018, November. Distributed Memory Sparse Inverse Covariance Matrix Estimation
on High-performance Computing Architectures.
In SC18: International Conference for High Performance Computing, Networking, Storage and Analysis (pp. 253-264). IEEE.

Eftekhari, A., Pasadakis, D., Bollhöfer, M., Scheidegger, S. and Schenk, O., 2021. Block-Enhanced Precision Matrix Estimation
for Large-Scale Datasets. Journal of Computational Science, p. 101389.

#################
# Example:
#################

import SQUIC 
import numpy as np

# set location of libSQUIC (set after importing package)
SQUIC.PATH_TO_libSQUIC('/path/to/squic')

# generate sample from tridiagonal precision matrix
p = 1024
n = 100
l = .4
max_iter = 100
tol = 1e-3

# generate a tridiagonal matrix
a = -0.5 * np.ones(p-1)
b = 1.25 * np.ones(p)
iC_star = np.diag(a,-1) + np.diag(b,0) + np.diag(a,1)

# generate the data
L = np.linalg.cholesky(iC_star)
Y = np.linalg.solve(L.T,np.random.randn(p,n))

[X,W,info_times,info_objective,info_logdetX,info_trSX] = SQUIC.run(Y,l)
"""

from .squic import *

