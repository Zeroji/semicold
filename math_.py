"""Math module for semicolon."""
import math                     # Used by eval() in calc()
from array import array         # Used to get the primes
from cmds import command        # Command dictionary
from string import ascii_lowercase, ascii_uppercase, digits

# Fetching prime list
primesData = open('data/primes', 'rb')
primes = array('I')
primes.fromstring(primesData.read())
primesData.close()


def calc(s):
    """Evaluate the mathematical expression contained in a string."""
    # (a)cos/sin/tan(h) atan2 degrees radoa,s
    # exp log log2 log10 factorial sqrt e pi floor int
    allowedMath = ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh',
                   'cos', 'cosh', 'degrees', 'exp', 'factorial', 'floor',
                   'log', 'log2', 'log10', 'radians', 'sin', 'sinh', 'sqrt',
                   'tan', 'tanh', 'e', 'pi']
    s = s.replace('^', '**')
    s = s.replace('int(', 'floor(')
    s = s.replace('PI', 'pi').replace('E', 'e').replace('π', 'pi')
    r, i = '', 0
    math.pi  # dummy statement to avoid F401 (flake8)
    while i < len(s):
        c = s[i]
        # Supports binary (0b), octal (0o) and hexadecimal (0x)
        if c in ascii_lowercase and c not in 'obx':
            func, j = c, i + 1
            while j < len(s) and s[j] in ascii_lowercase + digits:
                func += s[j]
                j += 1
            if func in allowedMath:
                r += 'math.' + func
            i = j - 1
        elif c not in (ascii_uppercase + '_'):
            r += c
        i += 1
    return eval(r)


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
