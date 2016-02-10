"""Cipher module for semicolon."""
import base64                   # Used for Base64 functions
import hashlib as hl            # Used for hash functions
from operator import itemgetter
from string import ascii_uppercase as uppercase
import requests                 # Used for http hashes
from cmds import command        # Command dictionary
from message import Message
from string_ import nsplit      # Used for bin/hex input


def close_to(text, lang):
    """Basic frequency analysis to determine language."""
    text = text.upper()
    freq_list = [[len([c for c in text if c == d]), d] for d in uppercase]
    freq_list.sort(reverse=True)
    close = 0
    for i in range(10):
        close += abs(lang.find(freq_list[i][1]) - i) * (26 - i)
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
        line_len = 2000 // len(lines[0])
        message = ['\n'.join(lines[i:i + line_len]) for i in range(0, 26, line_len)]
        output = []
        for msg in message:
            output.append(Message(msg, style=Message.BLOCK, private=private))
        if private:
            output.append(Message('This command was disabled due to spam.' +
                                  'The output was sent to you via PM.'))
        return output
    else:
        try:
            shift = int(arg)
            if _['R']:
                shift *= -1
            return Message(rot(_['L'][2], shift), Message.BLOCK)
        except ValueError:
            results = rotall(_['T'], 'ETAOINSRHDLUCMFYWGPBVKXQJZ')
            lines = ['ROT' + str(i // 10) + str(i % 10) + ': ' +
                     r for f, r, i in results[:3]]
            return Message('\n'.join(lines), Message.BLOCK)


@command('transform', __name__,
         help='Transform text between bases. (asc/utf, bin, dec, hex, b64)',
         usage='B1 B2 <text>', reversible=True)
def transform(_):
    """Wrapper for translate function."""
    return Message(translate(_['L'][3], _['P'][1].lower(), _['P'][2].lower(), _['R']),
                   Message.BLOCK)


@command('vigenere', __name__, help='Encode with Vigenere cipher.',
         usage='<key> <text>', reversible=True)
def vig_wrap(_):
    """Wrapper for vigenere function."""
    return Message(vigenere(_['L'][2], _['P'][1], _['R']), Message.BLOCK)


@command('vigbreak', __name__, help='Attempt to break a Vigenere cipher.',
         usage='<text>')
def vigbreak(_):
    """Vigenere cipher breaker."""
    key, out = vigenere_decrypt(_['T'])
    return Message('Key: ' + key + '\n' + out, Message.BLOCK)


@command('hash', __name__, help='Compute hash of URL, string or hex (bytes).',
         usage='<hash> <data>')
def hasher(_):
    """Wrapper for hash function."""
    return Message(gethash(_['L'][2], _['P'][1]))


def rot(text, shift, reverse=False):
    """Encode text with Caesar cipher."""
    if reverse:
        shift *= -1
    result = ''
    for char in text:
        val = ord(char)
        if val > 64 and val <= 90:
            val = (val - 65 + shift) % 26 + 65
        if val > 96 and val < 123:
            val = (val - 97 + shift) % 26 + 97
        result += chr(val)
    return result


def rotall(text, lang):
    """Find the Caesar cipher closest to a language."""
    results = [rot(text, shift) for shift in range(26)]
    proximity = [(close_to(result, lang), result, shift) for shift, result in enumerate(results)]
    proximity.sort()
    return proximity


# Now for the conversion functions
# Instead of having around N^2 functions let's have N*2


def from_b64(text):
    """Convert a Base64 string to bytes."""
    text = text.replace('-', '+').replace('_', '/')
    return base64.b64decode(text)


def from_bin(text):
    """Convert a string of bits to bytes."""
    data = nsplit(text.replace(' ', ''), 8)
    return bytes([int(byte, 2) for byte in data])


def from_dec(text):
    """Convert a string of ints to bytes."""
    data = text.split()
    return bytes([int(byte) for byte in data])


def from_hex(text):
    """Convert an hex string to bytes."""
    data = nsplit(text.lower().replace(' ', ''), 2)
    return bytes([int(byte, 16) for byte in data])


def from_utf(text):
    """Convert an UTF-8 string to bytes."""
    return bytes(text, 'utf-8')


def to_b64(data):
    """Convert a bytestring to Base64."""
    return base64.b64encode(data, b'-_').decode('ascii')


def to_bin(data, spacing=True):
    """Convert a bytestring to human-readable binary."""
    text = []
    for byte in data:
        bits = bin(byte)[2:].rjust(8, '0')
        text.append(bits)
    return (' ' if spacing else '').join(text)


def to_dec(data):
    """Convert a bytestring to decimal numbers."""
    return ' '.join([str(byte) for byte in data])


def to_hex(data, spacing=True, upper=False):
    """Convert a bytestring to hexadecimal."""
    text = []
    for byte in data:
        hexa = hex(byte)[2:].rjust(2, '0')
        if upper:
            hexa = hexa.upper()
        text.append(hexa)
    return (' ' if spacing else '').join(text)


def to_utf(data):
    """Convert a bytestring to UTF-8."""
    return data.decode('utf-8')


INPUTS = {'b64': from_b64, 'bin': from_bin, 'dec': from_dec,
          'hex': from_hex, 'asc': from_utf, 'utf': from_utf}
OUTPUTS = {'b64': to_b64, 'bin': to_bin, 'dec': to_dec,
           'hex': to_hex, 'asc': to_utf, 'utf': to_utf}


def translate(text, inp, out, reverse=False):
    """Translate text between two bases."""
    if reverse:
        inp, out = out, inp
    if inp in INPUTS.keys() and out in OUTPUTS.keys():
        return OUTPUTS[out](INPUTS[inp](text))
    return


def vigenere(text, key, reverse=False):
    """Encode a text with Vigenere cipher."""
    key = key.upper()
    key *= (len(text) // len(key)) + 1
    result = ''
    i = 0
    for char in text:
        val = ord(char)
        shift = ord(key[i]) - 65
        if reverse:
            shift *= -1
        if val > 64 and val <= 90:
            val = (val - 65 + shift) % 26 + 65
            i += 1
        if val > 96 and val < 123:
            val = (val - 97 + shift) % 26 + 97
            i += 1
        result += chr(val)
    return result


def vigenere_decrypt(text, target_freqs=[
        0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
        0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
        0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
        0.00978, 0.02360, 0.00150, 0.01974, 0.00074]):
    """Shamelessly stolen from rosettacode.org."""
    # pylint: disable=C0103, W0102, R0914, C0111
    nchars = len(uppercase)
    ordA = ord('A')
    sorted_targets = sorted(target_freqs)

    def frequency(text):
        result = [[c, 0.0] for c in uppercase]
        for c in text:
            result[c - ordA][1] += 1
        return result

    def correlation(text):
        result = 0.0
        freq = frequency(text)
        freq.sort(key=itemgetter(1))

        for i, f in enumerate(freq):
            result += f[1] * sorted_targets[i]
        return result

    cleaned = [ord(c) for c in text.upper() if c.isupper()]
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


HASHES = {'md5': hl.md5, 'sha1': hl.sha1, 'sha224': hl.sha224,
          'sha256': hl.sha256, 'sha384': hl.sha384, 'sha512': hl.sha512}


def gethash(text, hash_name='md5'):
    """Compute hash of given URL, string or hex."""
    if hash_name not in HASHES:
        return 'Invalid hash function'
    data = b''
    if text.startswith('http'):
        try:
            url = requests.get(text, stream=True, timeout=0.2)
            try:
                if int(url.raw.headers['Content-Length']) > 2**20:
                    return 'Content over 4MB'
            except ValueError:
                pass
            except KeyError:
                pass
            data = url.raw.read()
        except requests.exceptions.HTTPError:
            return 'Error accessing address'
        except requests.exceptions.Timeout:
            return 'Error accessing address'
    else:
        try:
            data = from_hex(text[2 if text.startswith('0x') else 0:])
        except ValueError:
            data = bytes(text[1 if text.startswith('"') else 0:], 'utf-8')
    return HASHES[hash_name](data).hexdigest()
