"""Math module for semicolon."""
import math                     # Used by eval() in calc()
import multiprocessing          # Used because of eval() in calc()
from array import array         # Used to get the primes
from cmds import command        # Command dictionary
from string import ascii_lowercase, ascii_uppercase, digits
from message import Message

# Fetching prime list
primesData = open('data/primes', 'rb')
primes = array('I')
primes.fromstring(primesData.read())
primesData.close()


@command('calc', __name__, help='Evaluate an expression, e.g. log(sin(pi))',
         usage='<expression>')
def calc_command(_):
    """Wrapper for the calc command."""
    r = calc(_['T'])
    if r is None:
        return Message('Over capacity')
    else:
        return Message(r)


@command('calcb', __name__, help='Evaluate an expression (binary output).',
         usage='<expression>')
def calcb_command(_):
    """Wrapper for the calc command (bin)."""
    r = calc(_['T'])
    if r is None:
        return Message('Over capacity')
    else:
        return Message(bin(r).replace('0b', ''))


@command('calco', __name__, help='Evaluate an expression (octal output).',
         usage='<expression>')
def calco_command(_):
    """Wrapper for the calc command (oct)."""
    r = calc(_['T'])
    if r is None:
        return Message('Over capacity')
    else:
        return Message(oct(r).replace('0o', ''))


@command('calcx', __name__, help='Evaluate an expression (hex output).',
         usage='<expression>')
def calcx_command(_):
    """Wrapper for the calc command (hex)."""
    r = calc(_['T'])
    if r is None:
        return Message('Over capacity')
    else:
        return Message(hex(r).replace('0x', ''))


@command('prime', __name__, help='Return the Nth prime number (up to 1e7).',
         usage='<N>')
def nthprime(_):
    """Return Nth prime."""
    try:
        l = list(map(int, _['P'][1:]))
        if max(l) > len(primes) or min(l) < 1:
            return Message('Over capacity')
        return Message(' '.join([str(primes[n - 1]) for n in l]))
    except:
        pass


@command('isprm', __name__, help='Tell if N is a prime number (up to 3e16).',
         usage='<N>')
def isprim(_):
    """Wrapper for isPrime function."""
    try:
        l = list(map(int, _['P'][1:]))
    except:
        return
    answers = []
    for x in l:
        r = isPrime(x)
        s = 'Over capacity' if r is None else str(r)
        if r and x <= primes[-1]:
            i = dicho(x, primes)
            pref = 'th'
            if i % 10 < 3 and (i // 10 % 10 != 1):
                pref = ('st', 'nd', 'rd')[i % 10]
            s += ' (' + str(i + 1) + pref + ')'
        answers.append(s)
    return Message(' '.join(answers))


@command('factor', __name__, help='Factor an integer into primes.',
         usage='<N>')
def factorize(_):
    """Wrapper for factor function."""
    try:
        n = int(_['T'])
    except:
        pass
    l = factor(n) if _['rank'] else factor(n, 1e4)
    u = {}
    for x in l:
        if x not in u.keys():
            u[x] = 0
        u[x] += 1
    f = ' * '.join([str(x) + '^' + str(u[x]) for x in u.keys()]) + ' '
    return Message(str(n) + ' = ' + f.replace('^1 ', ' ')[:-1])


def calc(s):
    """Evaluate the mathematical expression contained in a string."""
    # (a)cos/sin/tan(h) atan2 degrees radoa,s
    # exp log log2 log10 factorial sqrt e pi floor int
    allowedMath = ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh',
                   'cos', 'cosh', 'degrees', 'exp', 'factorial', 'floor',
                   'log', 'log2', 'log10', 'radians', 'sin', 'sinh', 'sqrt',
                   'tan', 'tanh', 'e', 'pi']
    s = s.lower()
    s = s.replace('^', '**')
    s = s.replace('int(', 'floor(')
    s = s.replace('π', 'pi')
    r, i = '', 0
    math.pi  # dummy statement to avoid F401 (flake8)
    while i < len(s):
        c = s[i]
        # Supports binary (0b), octal (0o) and hexadecimal (0x)
        if c in ascii_lowercase and c not in 'obxacdef':
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

    def calculator(expr, output):
        """Append eval(expr) to list."""
        try:
            result = eval(expr)
        except:
            result = 'ERR'
        output.put(result)

    q = multiprocessing.Queue()
    ev = multiprocessing.Process(target=calculator, args=(r, q))
    ev.start()
    ev.join(2)
    if ev.is_alive():
        ev.terminate()
        ev.join()
        return None
    else:
        result = q.get()
        if result != 'ERR':
            return result


def factor(n, mx=len(primes)):
    """Return the prime factors of n, up to P(mx)."""
    l = []
    for p in primes[:mx]:
        while n % p == 0:
            l.append(p)
            n //= p
            if n in primes:
                return l + [n]
    if n <= primes[mx - 1] ** 2:
        return l + [n]
    return ['Over capacity']


def isPrime(n):
    """Tell if n is a prime number. Return None if over capacity."""
    if n in primes:
        return True
    for p in primes:
        if n % p == 0:
            return False
    if n > primes[-1] ** 2:
        return None
    return True


def dicho(x, l):
    """Return the index of x in a sorted list, assuming x is present once."""
    a, b = 0, len(l)
    while l[a] != x and l[b] != x:
        m = (a + b) // 2
        n = l[m]
        if x < n:
            b = m
        elif x > n:
            a = m
        else:
            return m
    return a if l[a] == x else b
