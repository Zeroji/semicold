"""Cipher module for semicolon."""
import ngrams                   # Used to check language
import hashlib as hl            # Used for hash functions
import base64                   # Used for Base64 functions
from string_ import nsplit      # Used for bin/hex input
import urllib.request           # Used for http hashes

english = ''  # ngrams.ngram_score(open('english_trigrams.txt'))


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


def rotall(s, fit):
    """Find the Caesar cipher closest to a language."""
    S = [rot(s, n) for n in range(26)]
    p = [(fit.score(r), r, i) for r, i in enumerate(S)]
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
    x = nsplit(s.replace(' ', ''), 8)
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
    return ' '.join([int(n) for n in x])


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

hashes = {'md5': hl.md5, 'sha1': hl.sha1, 'sha224': hl.sha224,
          'sha256': hl.sha256, 'sha384': hl.sha384, 'sha512': hl.sha512}


def gethash(s, h='md5'):
    """Compute hash of given URL, string or hex."""
    if h not in hashes:
        return 'Invalid hash function'
    data = b''
    if s.startswith('http'):
        try:
            data = urllib.request.urlopen(s, None, 2).read()
        except:
            return 'Error accessing address'
    else:
        try:
            data = fromHex(s)
        except:
            data = bytes(s, 'utf-8')
    return hashes[h](data).hexdigest()
