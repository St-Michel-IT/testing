def fibonacci(n: int) -> int:
    """
    According to https://www.dcode.fr/nombres-fibonacci.
    This should return the n-th Fibonacci number.

       :param n: The n-th
       :return: The corresponding Fibonacci number
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
