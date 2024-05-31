"""
Test an embedded system with an Arduino Uno board
=================================================

Using an Arduino Uno board and a communication using simple RPC over the serial
port, this test checks that the results of the division of two float numbers.
It also us to explore the difference between the arithmetical operations on an
embedded system and on a computer that we all know or should know
(https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html ^^).
Keep in mind Python float numbers have a 64 bits precision, it is  a C double!
Arduino double are in fact float, but Python float are double...
Play with arduino integer/long overflow and buffer overflow protection.
"""
import pytest
from simple_rpc import Interface

RANDOM_DIVIDENDS_AND_DIVISORS = [
    (2, 3),
    (3, 9),
    (3, 5),
    (5, 3),
    (6, 7),
    (7, 6),
]


@pytest.fixture(scope='module')
def interface_port_com() -> str:
    """
    This fixture returns the port COM of the Arduino Uno board.
    Scope is module, as the interface only needs to be initialized once

       :return: The COM port name as a string
    """
    return '/dev/ttyACM0'


@pytest.fixture(scope='module')
def interface(interface_port_com: str) -> Interface:
    """
    Fixture that returns an interface with the Arduino Uno board.

       :param interface_port_com: The name of the COM port
       :return: An instantiated interface
    """
    return Interface(interface_port_com, baudrate=115200)


@pytest.mark.parametrize("dividend, divisor", RANDOM_DIVIDENDS_AND_DIVISORS)
def test_divide_float(
        interface: Interface,
        dividend: int,
        divisor: int
) -> None:
    """
    This test checks that the result of the division of 2 by 3 from Python
    having a 64 bits precision is not the same as the one from the Arduino Uno
    float division having a 32 bits precision.
    See https://www.arduino.cc/reference/en/language/variables/data-types/float/.

       :param interface: RPC interface with the Arduino Uno
       :param dividend: Dividend sent to the Arduino Uno
       :param divisor: Divisor sent to the Arduino Uno
    """
    python_division_result = dividend / divisor
    arduino_division_result = interface.floatDivision(dividend, divisor)
    error_message = """
    The result of the Arduino division %s is the same as the one calculated
    by Python %s
    """ % (arduino_division_result, python_division_result)
    assert arduino_division_result != python_division_result, error_message


@pytest.mark.parametrize("dividend, divisor", RANDOM_DIVIDENDS_AND_DIVISORS)
def test_float_and_double_identical_precision(
        interface: Interface,
        dividend: int,
        divisor: int
) -> None:
    """
    According to the Arduino documentation, the float and double types have the
    same precision. This test checks that the results of the division of two
    float and two double numbers are the same.
    See https://www.arduino.cc/reference/en/language/variables/data-types/double/

       :param interface: RPC interface with the Arduino Uno
       :param dividend: Dividend sent to the Arduino Uno
       :param divisor: Divisor sent to the Arduino Uno
    """
    arduino_float_division_result = interface.floatDivision(
        dividend, divisor
    )
    arduino_double_division_result = interface.doubleDivision(
        dividend, divisor
    )
    error_message = """
    Result of the Arduino float division %s is not the same as the one from
    the Arduino double division %s
    """ % (
        arduino_float_division_result,
        arduino_double_division_result
    )
    assert arduino_float_division_result == arduino_double_division_result, error_message


@pytest.mark.parametrize("value_to_add", range(1, 100))
def test_unsigned_long_overflow(
        interface: Interface,
        value_to_add
) -> None:
    """
    According to the Arduino documentation
    https://www.arduino.cc/reference/en/language/variables/data-types/unsignedlong/
    those integers are store in 32 bits and therefore range from 0 to 4,294,967,295.
    This check the Arduino has not much overflow protection using Python that has
    a 64 bits integer and therefor cannot overflow at this range of values.

       :param interface: RPC interface with the Arduino Uno
       :param value_to_add: An integer to add to the unsigned long
    """
    max_unsigned_long = 2 ** 32 - 1  # For the 32 bits Arduino one
    arduino_addition_result = interface.longOverflow(
        value_to_add
    )
    python_addition_result = value_to_add + max_unsigned_long
    error_message = """
    Result of the Arduino addition %s is the same as the one from Python %s
    """ % (
        max_unsigned_long,
        arduino_addition_result
    )
    assert arduino_addition_result != python_addition_result, error_message


def test_no_overflow_until_16_bytes(
        interface: Interface
) -> None:
    """
    This test checks that the Arduino Uno does not overflow until 16 bytes

       :param interface: RPC interface with the Arduino Uno
    """
    for _ in range(100):
        overflow: bool = interface.isBufferOverflow(
            bytes(
                "".join("\x11" * 16).encode()
            )
        )
        assert overflow is False, "No buffer overflow detected"
        assert interface.is_open() is True, "The serial port not open"


@pytest.mark.skip(reason="Might break the board and/or the port")
def test_overflow_with_more_16_bytes(
        interface: Interface
) -> None:
    """
    This test might break the Arduino Uno board and the port when a too long
    byte array is sent.

       :param interface: RPC interface with the Arduino Uno
    """
    for _ in range(100):
        overflow: bool = interface.isBufferOverflow(
            bytes(
                "".join("\x11" * 3000).encode()
            )
        )
        assert overflow is False, "No buffer overflow detected"
        assert interface.is_open() is True, "The serial port not open"
