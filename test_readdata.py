import pytest
from readdata import can_float


@pytest.mark.parametrize("a, expected", [
    ('-0.34', True),
    ('1.45', True),
    ('.12', True),
    ('not', False),
    ('1', True),
])
def test_can_float(a, expected):
    assert can_float(a) == expected


def test_get_data():
    from readdata import get_data
    d, c = get_data('test_get.csv')
    print(d)
    print(c)
    assert d == [0.04, 0.12, 0.3]
    assert c == [0.2, 0.3, 0.4]
