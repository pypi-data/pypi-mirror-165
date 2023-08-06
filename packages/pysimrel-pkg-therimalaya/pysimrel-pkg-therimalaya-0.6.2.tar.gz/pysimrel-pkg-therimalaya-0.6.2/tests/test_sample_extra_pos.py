import pytest
import numpy as np
from pysimrel.utilities import *

@pytest.fixture
def rs():
	rs = np.random.RandomState(777)
	return rs

@pytest.fixture
def pos_samp(rs):
	n_extra_pos = [4]
	irrel_pos = [4, 5, 6, 7, 8, 9, 10]
	rel, irrel = sample_extra_pos(rs, n_extra_pos, [], irrel_pos)
	return rel, irrel, n_extra_pos, irrel_pos

def test_extra_pos_length(pos_samp):
	rel, irrel, n_extra_pos, irrel_pos = pos_samp
	assert len(rel[0]) == n_extra_pos[0]
	assert len(irrel) == len(irrel_pos) - n_extra_pos[0]

def test_extra_pos_value(pos_samp):
	rel, irrel, n_extra_pos, irrel_pos = pos_samp
	assert rel == [{9, 10, 4, 6}], "Test Failed"
	assert irrel == {8, 5, 7}, "Test Failed"
	
