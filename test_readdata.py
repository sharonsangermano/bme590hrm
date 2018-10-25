import pytest
from readdata import can_float
from readdata import get_data


@pytest.mark.parametrize("a, expected", [
    ('-0.34', True),
    ('1.45', True),
    ('.12', True),
    ('not', False),
    ('1', True),
])
def test_can_float(a, expected):
    assert can_float(a) == expected


@pytest.mark.parametrize("filename, exp1, exp2", [
    ('test_get.csv', [0.04, 0.12, 0.3], [0.2, 0.3, 0.4]),
    ('test_get_str.csv', [0.2, 0.3, 0.6, 0.7], [0.9, 0.45, -0.45, -0.3]),
    ('test_get_null.csv', [0.6, 0.9], [-0.12, 0.4])
])
def test_get_data(filename, exp1, exp2):
    d, c = get_data(filename)
    assert d == exp1
    assert c == exp2
