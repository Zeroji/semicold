"""String module for semicolon."""
from cmds import command        # Command dictionary


@command('nospace', __name__, help='Remove whitespaces from a string.',
         usage='<text>')
def nospace_wrapper(_):
    """Wrapper for nospace function."""
    _['send'](nospace(_['T']), code=1)


@command('unspace', __name__, help='Remove extra whitespaces from a string.',
         usage='<text>')
def unspace_wrapper(_):
    """Wrapper for unspace function."""
    _['send'](unspace(_['T']), code=1)


command('len', __name__, help='Return the length of a string.',
        usage='<text>')(lambda _: _['send'](str(len(_['T'])), code=0))


def nospace(s):
    """Remove whitespaces from a string."""
    return s.replace(' ', '')


def unspace(s):
    """Remove extra whitespaces from a string."""
    # 'a  b  _  c  d' to 'ab cd'
    if max([len(x) for x in s.split()]) > 1:
        return s
    n = []
    m = 0
    for c in s:
        if c == ' ':
            m += 1
        elif m != 0:
            n.append(m)
            m = 0
    r = s.replace(' ' * min(n) * 2 + ' ', ' ' * min(n) + '§' + ' ' * min(n))
    return r.replace(' ' * min(n), '').replace('§', ' ')


def copyspaces(s, sp):
    """Insert spaces from sp into the string."""
    if isinstance(sp, str):
        sp = [len(x) for x in sp.split()]
    r = ''
    for n in sp:
        r += s[:n] + ' '
        s = s[n:]
    return r + s


def nsplit(s, n):
    """Split a string in chunks of n characters."""
    return [s[i:i + n] for i in range(0, len(s), n)]
