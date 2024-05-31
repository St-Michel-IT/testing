import pytest

from ..src.fib import fibonacci


@pytest.mark.parametrize(
    "n,result",
    (
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2),
            (4, 3),
            (5, 5),
            (6, 8),
            (7, 13),
            (8, 21),
            (9, 34),
            (10, 55),
    )
)
def test_fibonacci(n, result):
    """
    Test result are from https://www.dcode.fr/nombres-fibonacci
    and store in the above parametrize.
    """
    assert fibonacci(n) == result
