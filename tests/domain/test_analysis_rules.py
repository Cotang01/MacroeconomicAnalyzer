from src.domain.analysis_rules import OPERATIONS


def test_max_returns_zero_on_empty_list():
    assert OPERATIONS["max"]([]) == 0
    
def test_min_returns_zero_on_empty_list():
    assert OPERATIONS["min"]([]) == 0
    
def test_average_returns_zero_on_empty_list():
    assert OPERATIONS["average"]([]) == 0
    