import pytest


def test_divide():  # Un test Pytest est préfixé par test_
    assert 23 % 2 == 0, "Le restant de la division est différent de 0."


@pytest.mark.parametrize("dividend", range(100))  # Paramétrage du test
def test_divide_from_0_to_99(dividend):  # Doit avoir un argument présent dans le paramétrage
    assert dividend % 2 == 0, "Le restant de la division est différent de 0."


def test_fail_or_error():  # Une erreur donne un fail ou error?
    dividende = 23 / 0
    assert dividende % 2 == 0, \
        "Le restant de la division est différent de 0."
