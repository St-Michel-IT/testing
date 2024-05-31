import pytest

from witness_number import WitnessNumber

FIRST_HUNDRED = range(2, 100)


@pytest.mark.parametrize("x", FIRST_HUNDRED)
def test_instantiation(x):
    """
    Test instantiation of WitnessNumber.
    """
    try:
        WitnessNumber(x)
    except Exception as error:
        pytest.fail("WitnessNumber(%s) raised %s" % (x, error))


@pytest.mark.parametrize("x", FIRST_HUNDRED)
def test_is_int(x):
    """
    Test a WitnessNumber instance is an int.
    """
    assert isinstance(WitnessNumber(x), int)


def test_747_is_prime():
    """
    Test 747 with witness 23 is_prime() as in the first part of the video
    https://www.youtube.com/watch?v=_MscGSN5J6o.
    23 is not a liar as number sum in 747 is 18, multiple of 9, 747 is a
    multiple of 9 as well.
    """
    witness_number = WitnessNumber(23)
    witness_number.set_witness_of(747)
    assert witness_number.is_prime() is False


def test_10_is_prime():
    """
    Test 747 with witness 23 is_prime() as in the second part of the video
    https://www.youtube.com/watch?v=_MscGSN5J6o. 10 is a liar for 91 as it is
    13 * 7.
    """
    witness_number = WitnessNumber(10)
    witness_number.set_witness_of(91)
    assert witness_number.is_prime() is True


@pytest.mark.parametrize("x", [1, 0, -100, -200, -300])
def test_witness_greater_to_one(x):
    """
    According to wikipedia the witness has to be greater to one
    https://en.wikipedia.org/wiki/Fermat_primality_test.
    Test a ValueError is raised if the witness is inferior or equal to 1.
       :param x: Integers, inferior to one, to instantiate as a witness.
    """
    with pytest.raises(ValueError):
        WitnessNumber(x)


@pytest.mark.parametrize("x", [100, 200, 300])
def test_even_cannot_be_prime(x):
    """
    A prime number can not be even, test ValueError is raised.

       :param x: Even number to test, supérior to 10 the witness number.
    """
    witness_number = WitnessNumber(10)
    with pytest.raises(ValueError):
        witness_number.set_witness_of(x)


@pytest.mark.parametrize("x", [100, 200, 300])
def test_witness_cannot_be_superior_prime(x):
    """
    The witness number has to be inferior to possible prime, test ValueError is
    raised.

       :param x: Even number to test, supérior to 10 the witness number.
    """
    witness_number = WitnessNumber(100)
    with pytest.raises(ValueError):
        witness_number.set_witness_of(x)


@pytest.mark.parametrize("x", [-100, -200, -300])
def test_negative_cannot_be_prime(x):
    """
    A prime - number can not be even, test ValueError is raised.

       :param x: Even number to test, supérior to 10 the witness number.
    """
    witness_number = WitnessNumber(10)
    with pytest.raises(ValueError):
        witness_number.set_witness_of(x)
