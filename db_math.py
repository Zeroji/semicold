"""Math module for semicolon."""
import math                     # Just in case
from array import array         # Used to get the primes
from string import ascii_lowercase, ascii_uppercase

# Fetching prime list
# primesData = open('data/primes', 'rb')
primes = array('I')
# primes.fromstring(primesData.read())
# primesData.close()


def factor(n, mx=len(primes)):
    """Return the prime factors of n, up to P(mx)."""
    l = []
    for p in primes[:mx]:
        while n % p == 0:
            l.append(p)
            n //= p
            if n in primes:
                return l + [n]
    return ['Over capacity']


def isPrime(n):
    """Tell if n is a prime number. Return None if over capacity."""
    for p in primes:
        if n % p == 0:
            return False
    if n > primes[-1] ** 2:
        return None
    return True


def calc(s):
    """Evaluate the mathematical expression contained in a string."""
    allowedMath = ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh',
                   'cos', 'cosh', 'degrees', 'exp', 'factorial', 'floor',
                   'log', 'log2', 'log10', 'radians', 'sin', 'sinh', 'sqrt',
                   'tan', 'tanh', 'e', 'pi']
    s = s.replace('^', '**')
    s = s.replace('int(', 'floor(')
    s = s.replace('PI', 'pi').replace('E', 'e').replace('π', 'pi')
    r, i = '', 0
    while i < len(s):
        c = s[i]
        if c in ascii_lowercase:
            func, j = c, i + 1
            while j < len(s) and s[j] in ascii_lowercase:
                func += s[j]
                j += 1
            print(func)
            if func in allowedMath:
                r += 'math.' + func
            i = j - 1
        elif c not in ascii_uppercase:
            r += c
        i += 1
    print(r)
    return eval(r)
