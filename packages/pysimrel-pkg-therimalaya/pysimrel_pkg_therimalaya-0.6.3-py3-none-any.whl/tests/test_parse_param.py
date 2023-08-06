import pytest
import numpy as np
from pysimrel.utilities import *

def test_parse_param_values():
    with pytest.raises(ValueError) as param_only_semicolon:
        parse_param(";")
    with pytest.raises(ValueError) as param_only_comma:
        parse_param(",")
    with pytest.raises(ValueError) as param_only_empty:
        parse_param("")
    assert parse_param("1, 2") == [[1, 2]]
    assert parse_param("1; 2") == [[1], [2]]
    assert parse_param("1, 2; 2, 3")
    assert parse_param("1") == [[1]]
    assert parse_param("1,") == [[1]]
    assert parse_param("1;") == [[1]]
    assert str(param_only_semicolon.value) == "Argument must include an integer."
    assert str(param_only_comma.value) == "Argument must include an integer."
    assert str(param_only_empty.value) == "Argument must include an integer."