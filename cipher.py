"""Cipher module for semicolon."""
import ngrams                   # Used to check language
import hashlib as hl            # Used for hash functions
import base64                   # Used for Base64 functions
from string_ import nsplit      # Used for bin/hex input
import requests                 # Used for http hashes
from cmds import command        # Command dictionary
from string import ascii_uppercase as uppercase
from operator import itemgetter


def closeTo(s, lang):
    """Basic frequency analysis to determine language."""
    s = s.upper()
    l = [[len([c for c in s if c == d]), d] for d in uppercase]
    l.sort(reverse=True)
    close = 0
    for i in range(10):
        close += abs(lang.find(l[i][1]) - i) * (26 - i)
    return close


@command('rot', __name__, help='Use Caesar cipher on text.',
         reversible=True, usage='[all|<N>] <text>')
def rot_command(_):
    """Apply Caesar cipher to text."""
    arg = _['P'][1]
    if arg == 'all':
        private = _['rank'] == 0 and not _['private']
        lines = ['ROT' + str(i // 10) + str(i % 10) + ': ' +
                 rot(_['L'][2], i) for i in range(26)]
        n = 2000 // len(lines[0])
        message = ['\n'.join(lines[i:i + n]) for i in range(0, 26, n)]
        for m in message:
            _['send'](m, pm=private)
        if private:
            _['send']('This command was disabled due to spam.' +
                      'The output was sent to you via PM.', 1)
    else:
        try:
            n = int(arg)
            if _['R']:
                n *= -1
            _['send'](rot(_['L'][2], n))
        except:
            results = rotall(_['T'], 'ETAOINSRHDLUCMFYWGPBVKXQJZ')
            lines = ['ROT' + str(i // 10) + str(i % 10) + ': ' +
                     r for f, r, i in results[:3]]
            _['send']('\n'.join(lines))


@command('transform', __name__, help='Transform text between bases.',
         usage='<in> <out> <text>', reversible=True)
def transform(_):
    """Wrapper for translate function."""
    _['send'](translate(_['L'][3], _['P'][1].lower(), _['P'][2].lower(),
              _['R']))


@command('vigenere', __name__, help='Encode with Vigenere cipher.',
         usage='<key> <text>', reversible=True)
def vig_wrap(_):
    """Wrapper for vigenere function."""
    _['send'](vigenere(_['L'][2], _['P'][1], _['R']))


@command('vigbreak', __name__, help='Attempt to break a Vigenere cipher.',
         usage='<text>')
def vigbreak(_):
    """Vigenere cipher breaker."""
    try:
        key, out = vigenere_decrypt(_['T'])
        _['send']('Key: ' + key + '\n' + out)
    except:
        pass


@command('hash', __name__, help='Compute hash of URL, string or hex (bytes).',
         usage='<hash> <url|text|hex>')
def hasher(_):
    """Wrapper for hash function."""
    _['send'](gethash(_['L'][2], _['P'][1]))


def rot(s, n, reverse=False):
    """Encode s with Caesar cipher."""
    if reverse:
        n *= -1
    r = ''
    for c in s:
        x = ord(c)
        if x > 64 and x <= 90:
            x = (x - 65 + n) % 26 + 65
        if x > 96 and x < 123:
            x = (x - 97 + n) % 26 + 97
        r += chr(x)
    return r


def rotall(s, lang):
    """Find the Caesar cipher closest to a language."""
    S = [rot(s, n) for n in range(26)]
    p = [(closeTo(r, lang), r, i) for i, r in enumerate(S)]
    p.sort()
    return p


# Now for the conversion functions
# Instead of having around N^2 functions let's have N*2


def fromB64(s):
    """Convert a Base64 string to bytes."""
    s = s.replace('-', '+').replace('_', '/')
    return base64.b64decode(s)


def fromBin(s):
    """Convert a string of bits to bytes."""
    x = nsplit(s.replace(' ', ''), 8)
    return bytes([int(n, 2) for n in x])


def fromDec(s):
    """Convert a string of ints to bytes."""
    x = s.split()
    return bytes([int(n) for n in x])


def fromHex(s):
    """Convert an hex string to bytes."""
    x = nsplit(s.lower().replace(' ', ''), 2)
    return bytes([int(n, 16) for n in x])


def fromUTF(s):
    """Convert an UTF-8 string to bytes."""
    return bytes(s, 'utf-8')


def toB64(x):
    """Convert a bytestring to Base64."""
    return base64.b64encode(x, b'-_').decode('ascii')


def toBin(x, spacing=True):
    """Convert a bytestring to human-readable binary."""
    s = []
    for n in x:
        bits = bin(n)[2:]
        bits = '0' * (8 - len(bits)) + bits
        s.append(bits)
    return (' ' if spacing else '').join(s)


def toDec(x):
    """Convert a bytestring to decimal numbers."""
    return ' '.join([str(n) for n in x])


def toHex(x, spacing=True, upper=False):
    """Convert a bytestring to hexadecimal."""
    s = []
    for n in x:
        hexa = hex(n)[2:]
        if n < 16:
            hexa = '0' + hexa
        if upper:
            hexa = hexa.upper()
        s.append(hexa)
    return (' ' if spacing else '').join(s)


def toUTF(x):
    """Convert a bytestring to UTF-8."""
    return x.decode('utf-8')


inputs = {'b64': fromB64, 'bin': fromBin, 'dec': fromDec,
          'hex': fromHex, 'asc': fromUTF, 'utf': fromUTF}
outputs = {'b64': toB64, 'bin': toBin, 'dec': toDec,
           'hex': toHex, 'asc': toUTF, 'utf': toUTF}


def translate(text, i, o, reverse=False):
    """Translate text between two bases."""
    if reverse:
        i, o = o, i
    if i in inputs.keys() and o in outputs.keys():
        return outputs[o](inputs[i](text))
    return


def vigenere(text, key, reverse=False):
    """Encode a text with Vigenere cipher."""
    key = key.upper()
    key *= (len(text) // len(key)) + 1
    r = ''
    i = 0
    for c in text:
        x = ord(c)
        v = ord(key[i]) - 65
        if reverse:
            v *= -1
        if x > 64 and x <= 90:
            x = (x - 65 + v) % 26 + 65
            i += 1
        if x > 96 and x < 123:
            x = (x - 97 + v) % 26 + 97
            i += 1
        r += chr(x)
    return r


def vigenere_decrypt(input, target_freqs=[
        0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
        0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
        0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
        0.00978, 0.02360, 0.00150, 0.01974, 0.00074]):
    """Shamelessly stolen from rosettacode.org."""
    nchars = len(uppercase)
    ordA = ord('A')
    sorted_targets = sorted(target_freqs)

    def frequency(input):
        result = [[c, 0.0] for c in uppercase]
        for c in input:
            result[c - ordA][1] += 1
        return result

    def correlation(input):
        result = 0.0
        freq = frequency(input)
        freq.sort(key=itemgetter(1))

        for i, f in enumerate(freq):
            result += f[1] * sorted_targets[i]
        return result

    cleaned = [ord(c) for c in input.upper() if c.isupper()]
    best_len = 0
    best_corr = -100.0

    # Assume that if there are less than 20 characters
    # per column, the key's too long to guess
    for i in range(2, len(cleaned) // 20):
        pieces = [[] for _ in range(i)]
        for j, c in enumerate(cleaned):
            pieces[j % i].append(c)

        # The correlation seems to increase for smaller
        # pieces/longer keys, so weigh against them a little
        corr = -0.5 * i + sum(correlation(p) for p in pieces)

        if corr > best_corr:
            best_len = i
            best_corr = corr

    if best_len == 0:
        return ("Text is too short to analyze", "")

    pieces = [[] for _ in range(best_len)]
    for i, c in enumerate(cleaned):
        pieces[i % best_len].append(c)

    freqs = [frequency(p) for p in pieces]

    key = ""
    for fr in freqs:
        fr.sort(key=itemgetter(1), reverse=True)

        m = 0
        max_corr = 0.0
        for j in range(nchars):
            corr = 0.0
            c = ordA + j
            for frc in fr:
                d = (ord(frc[0]) - c + nchars) % nchars
                corr += frc[1] * target_freqs[d]

            if corr > max_corr:
                m = j
                max_corr = corr

        key += chr(m + ordA)

    r = (chr((c - ord(key[i % best_len]) + nchars) % nchars + ordA)
         for i, c in enumerate(cleaned))
    return (key, "".join(r))


hashes = {'md5': hl.md5, 'sha1': hl.sha1, 'sha224': hl.sha224,
          'sha256': hl.sha256, 'sha384': hl.sha384, 'sha512': hl.sha512}


def gethash(s, h='md5'):
    """Compute hash of given URL, string or hex."""
    if h not in hashes:
        return 'Invalid hash function'
    data = b''
    if s.startswith('http'):
        try:
            r = requests.get(s, stream=True, timeout=2)
            if int(r.raw.header['Content-Length']) > 2**20:
                return 'Content over 4MB'
            data = r.raw.read()
        except:
            return 'Error accessing address'
    else:
        try:
            data = fromHex(s[2 if s.startswith('0x') else 0:])
        except:
            data = bytes(s[1 if s.startswith('"') else 0:], 'utf-8')
    return hashes[h](data).hexdigest()
