def is_prime(n: int) -> bool:
    """Check if n is prime as per this definition: https://en.wikipedia.org/wiki/Prime_number >>> is_prime(3) True >>> is_prime(4) False"""
    if n < 4:
        return n > 1
    if (n % 2 == 0) or (n % 3 == 0):
        return False
    if n < 11:
        return True
    return (n % 5 != 0) and (n % 7 != 0)


# print(is_prime(5))


import math


def is_truly_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # Check for divisors from 3 up to the square root of n, only odd numbers
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


for i in range(1000):
    if is_prime(i) != is_truly_prime(i):
        print(i)
