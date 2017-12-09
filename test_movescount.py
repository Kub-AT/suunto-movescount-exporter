import pytest
from movescount.scraper import Movescount


def test_wrong_format():
    with pytest.raises(AssertionError):
        Movescount('pdf')


def test_correct_format():
    assert isinstance(Movescount('fit'), Movescount)
