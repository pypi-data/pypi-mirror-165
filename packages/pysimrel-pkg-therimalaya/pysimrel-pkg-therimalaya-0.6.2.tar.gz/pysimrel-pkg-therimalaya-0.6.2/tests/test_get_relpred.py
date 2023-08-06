import pytest
import numpy as np
from pysimrel.utilities import *

@pytest.fixture
def relpred():
    n_pred = 10
    n_relpred = [5]
    pos_relcomp = [[1, 2, 3, 4]]
    ret = get_relpred(n_pred, n_relpred, pos_relcomp, 777)
    return ret['rel'], ret['irrel'], n_pred, n_relpred, pos_relcomp

def test_extra_pos_length(relpred):
    rel, irrel, n_pred, n_relpred, pos_relcomp = relpred
    assert len(rel[0]) == n_relpred[0]
    assert len(set(pos_relcomp[0]) - set(rel[0])) == 0
    assert len(set(rel[0]) - set(pos_relcomp[0])) >= 0
    assert len(set([x for y in rel for x in y] + list(irrel))) == n_pred

def test_extra_pos_value(relpred):
    rel, irrel, n_pred, n_relpred, pos_relcomp = relpred
    assert rel[0] == {0, 1, 2, 3, 4}
    assert irrel == {5, 6, 7, 8, 9}
	
