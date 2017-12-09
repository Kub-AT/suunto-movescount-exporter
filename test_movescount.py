import pytest
from movescount.scraper import Movescount


def test_wrong_format():
    with pytest.raises(AssertionError):
        Movescount(['pdf'])


def test_one_wrong_format():
    with pytest.raises(AssertionError):
        Movescount([Movescount.AVAILABLE_FORMATS[0], 'pdf'])


def test_correct_format():
    assert isinstance(Movescount([Movescount.AVAILABLE_FORMATS[0]]), Movescount)
