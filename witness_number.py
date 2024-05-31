import logging

logging.basicConfig(
    format="%(asctime)s;%(levelname)s;%(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y %I:%M:%S %p"
)


class WitnessNumber(int):
    """
    Implementation of the numberphile video on witness numbers
    https://www.youtube.com/watch?v=_MscGSN5J6o.
    """

    def __new__(cls, *args, **kwargs):
        """
        Modify the int class. Check the witness number is greater to 1. Not in
        the video but in https://en.wikipedia.org/wiki/Fermat_primality_test

           :param args: any args you can pass to an int
           :param kwargs: any kwargs you can pass to an int
        """
        if 1 >= args[0]:
            raise ValueError("Witness number must be greater to 1.")
        return super(WitnessNumber, cls).__new__(cls, *args, **kwargs)

    def __init__(self, number: int) -> None:
        """
        Initialize a witness number.
        :param number: number of witnesses
        """
        self.__number = number
        self.__witness_of = None

    def set_witness_of(self, test_number: int) -> None:
        """
        Check if the witness number is a witness of the given number.
        Must be superior to the witness number.
        The video says "it can be any number smaller to n".
        But greater to 1.

           :param test_number: number to check
           :raise ValueError: if the witness number is not superior to the
              witness number
        """
        if self.__number > test_number:
            raise ValueError(
                "Test number must be superior to the witness number."
            )
        if test_number % 2 == 0 and test_number > 2:
            raise ValueError(
                "Number must be odd, an even number > 2 is never prime."
            )
        if test_number <= 0:
            raise ValueError("Prime numbers are always positive.")
        self.__witness_of = test_number

    def is_prime(self) -> bool:
        """
        Ask the witness the number under test is prime or not.
        If false, the number is composite for sure, if true, the number can be
        prime ~75% of the time.

           :return: True if the number is prime, False otherwise
        """
        if self.__witness_of is None:
            raise ValueError("Test number must be set.")
        __d = int((self.__witness_of - 1) / 2)
        logging.info("d is %s" % __d)
        __r = pow(self.__witness_of, int(__d), self.__number)
        logging.info("a^d mod n is %s" % __r)
        return __r == 1 or __r - self.__witness_of == -1
