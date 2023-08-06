import pytest
import numpy as np
from pysimrel.utilities import *

@pytest.fixture
def cov_mat():
    n_pred = 10
    n_resp = 4
    lmd = get_eigen(0.8, n_pred)
    kappa = get_eigen(1.2, n_resp)
    pos_relcomp = [list(range(4)), list(range(5, 7))]
    rsq = [0.7, 0.8]
    rs = np.random.RandomState(123)
    covs = get_cov(pos_relcomp, rsq, kappa, lmd)
    return n_pred, n_resp, lmd, kappa, pos_relcomp, rsq, covs
    
def test_cov_mat_shape(cov_mat):
    p, m, l, k, relpos, rsq, covs = cov_mat
    assert covs.shape == (m, p)

def test_cov_mat_values(cov_mat):
    p, m, l, k, relpos, rsq, covs = cov_mat
    irrel_cov_idx = np.squeeze(np.where(np.all(covs==0, axis=1)))
    rel_cov_idx = np.squeeze(np.where(~np.all(covs==0, axis=1)))
    rel_cov_idx = [list(np.squeeze(np.nonzero(covs[x]))) for x in rel_cov_idx]
    assert np.all(covs[irrel_cov_idx]==0)
    assert rel_cov_idx == relpos
