import pytest
import numpy as np
from pysimrel.utilities import *

@pytest.fixture
def rotation_matrix():
    shape = (4, 4)
    pos = [0, 1, 3]
    mat = get_rotate(np.zeros(shape), pos)
    mat_ = mat[pos][:,pos]
    return shape, pos, mat, mat_
    
def test_rotmat_shape(rotation_matrix):
    shape, pos, mat, mat_ = rotation_matrix
    nonzero_row = np.argwhere(~np.all(mat==0, axis=0)).flatten()
    nonzero_col = np.argwhere(~np.all(mat==0, axis=1)).flatten()
    assert np.all(mat_ == mat[nonzero_row][:,nonzero_col])
    assert shape == mat.shape
    assert list(nonzero_row) == pos
    assert list(nonzero_col) == pos

def test_rotmat_properties(rotation_matrix):
   shape, pos, mat, mat_ = rotation_matrix 
   AtA_ = np.dot(mat_.T, mat_)
   AAt_ = np.dot(mat_, mat_.T)
   eye_ = np.eye(mat_.shape[0])
   # Test if Square
   assert mat.shape[0] == mat.shape[1]
   assert mat_.shape[0] == mat_.shape[1]
   # Test if Orthogonal
   assert np.allclose(AtA_, eye_, atol=1e-15, rtol=1e-15)
   assert np.allclose(AAt_, eye_, atol=1e-15, rtol=1e-15)
