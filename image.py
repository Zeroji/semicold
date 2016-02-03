"""Image processing module for ;; bot."""
from cmds import command        # Command dictionary
import exifread                 # EXIF metadata extraction
from string_ import nsplit      # XMP tags formatting
import requests                 # Image Fetching


@command('meta', __name__, help='Get EXIF metadata from an image',
         usage='[<tag filter>] <URL>')
def meta(_):
    """Wrapper for the EXIF metadata function."""
    mask = ''
    url = _['T']
    if len(_['P']) > 2:
        mask = _['P'][1]
        url = _['L'][2]
    print('Getting tags `' + mask + '` from', url)
    tags = gettags(url)
    if tags == -2:
        _['send']('Not an image file', code=1)
    elif tags == -1:
        _['send']('An error occcured while searching for the file', code=1)
    elif tags == 0:
        _['send']('No metadata found.', code=1)
    else:
        tbl = ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote')
        tag = {}
        for t in tags.keys():
            if t not in tbl and mask in t:
                tag[t] = tags[t]
        tn = len(tag.keys())
        tagnamelength = sum([len(t) for t in tag.keys()])
        message = '\n'.join([t[:30].ljust(32) + str(tag[t])[:40]
                             for t in tag.keys()])
        print(-1, len(message))
        if len(message) <= 2000:
            _['send'](message)
        else:
            print('urgh')
            if tagnamelength >= 1800:
                print('urgh')
                if tn > 100:
                    print('urgh')
                    _['send']('Too many tags! (' + str(tn) + ')', code=1)
                else:
                    message = 'Found the following ' + str(tn) + ' tags: '
                    for t in tag.keys():
                        message += t[:1960 // tn - 2]
                        if len(t) > 1960 // tn - 2:
                            message += '…'
                        message += ', '
                    print(len(message))
                    _['send'](message[:-2], code=1)
            else:
                message = 'Found the following ' + str(tn) + ' tags: '
                for t in tag.keys():
                    message += t + ', '
                print(0, len(message))
                _['send'](message[:-2], code=1)


@command('meta_xmp', __name__, minRank=1,
         help='Get XMP metadata from an image', usage='<URL>')
def metaXMP(_):
    """Wrapper for the XMP metadata function."""
    xmp = getxmp(_['T'])
    if xmp == -2:
        _['send']('Not an image file', code=1)
    elif xmp == -1:
        _['send']('An error occcured while searching for the file', code=1)
    elif xmp == 0:
        _['send']('No metadata found.', code=1)
    else:
        lines = xmp.replace('> <', '>\n<').replace('://', ':/ /').splitlines()
        message = ''
        for l in lines:
            if len(message + l) > 2000:
                _['send'](message[:-1])
                message = ''
            message += l + '\n'
        _['send'](message[:-1])


class seeker:
    """Wrapper giving file functions on a stream from requests.get()."""

    def __init__(self, url):
        """Initialize the stream."""
        self.url = url
        self.raw = b''
        self.lng = 0
        self.pos = 0
        self.rps = 0
        self.r = requests.get(url, stream=True).raw

    def read(self, n=-1):
        """Read n bytes."""
        if n >= 0 and self.pos + n <= self.lng:
            self.pos += n
            return self.raw[self.pos - n:self.pos]
        else:
            rw = self.raw[self.pos:]
            bs = self.r.read(n - len(rw))
            self.raw += bs
            self.rps += len(bs)
            self.pos += len(bs) + len(rw)
            self.lng = self.pos
            return rw + bs

    def seek(self, off):
        """Go to a certain offset."""
        if off <= self.lng:
            self.pos = off
        else:
            self.pos = self.lng
            bs = self.r.read(off - self.pos)
            self.rps += len(bs)
            self.raw += bs
            self.lng = off
            self.pos = off

    def tell(self):
        """Get current position."""
        return self.pos


def gettags(url):
    """Get EXIF tags from an image given its URL."""
    print("getting from url", url)
    try:
        data = seeker(url)
        if 'image' not in data.r.headers['Content-Type']:
            return -2
    except:
        return -1
    else:
        tags = exifread.process_file(data)
        if not tags.keys():
            return 0
        return tags


def getxmp(url):
    """Get XMP metadata from an image given its URL."""
    print('getting from url', url)
    try:
        data = seeker(url)
        if 'image' not in data.r.headers['Content-Type']:
            return -2
    except:
        return -1
    else:
        head = data.read(2**16)
        xmp_head = head.find(b'<x:xmpmeta')
        xmp_tail = head.find(b'</x:xmpmeta')
        if xmp_head < 0 or xmp_tail < 0:
            return 0
        xmp = head[xmp_head:xmp_tail + 12].decode('utf-8')
        return xmp
