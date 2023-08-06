import pytest
import numpy as np
from pysimrel.utilities import *

@pytest.fixture
def eigenvalues():
    rate, nvar, min_value = 0.8, 10, 1e-4
    return get_eigen(rate, nvar), rate, nvar, min_value

def test_extra_pos_length(eigenvalues):
    eigen, rate, nvar, min_value = eigenvalues
    assert len(eigen) == nvar
    assert len(eigen) == len(np.unique(eigen))
    
def test_extra_pos_value(eigenvalues):
    eigen, rate, nvar, min_value = eigenvalues
    nu = min_value * np.exp(-rate) / (1 - min_value)
    assert eigen[0] == 1
    assert eigen[-1] >= min_value
    assert all([x > y for x, y in zip(eigen, eigen[1:])])

	
