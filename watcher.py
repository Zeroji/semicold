import urllib.request           # Open URLs
import time                     # Timer
import hashlib                  # Check URLs

WWF = 'data/watch'  # Watcher Watch File


def check():
    """Check URLs for changes."""
    wf = [x.split(' ', 2) for x in open(WWF).read().splitlines()]
    updates = []
    rewrite = False
    for i, (md5, sha1, url) in enumerate(wf):
        data = b''
        try:
            data = urllib.request.urlopen(url, None, 2)
        except:
            pass  # Because we don't really care if it times out.
        md = hashlib.md5(data).hexdigest()
        sh = hashlib.sha1(data).hexdigest()
        if md != md5 or sh != sha1:  # Update!
            if len(md5) * len(sha1) > 0:
                warning = '' # Warning if the MD5 or SHA1 didn't change
                warning = ' - Identical MD5!!' if md == md5 else warning
                warning = ' - Identical SHA1!!' if sh == sha1 else warning
                updates.append((url, warning))
            wf[i][0] = md
            wf[i][1] = sh
            rewrite = True
    if rewrite:
        open(WWF, 'w').write('\n'.join([' '.join(x) for x in wf]))
    if update:
        message = '\n'.join([''.join(x) for x in update])
        
            
            

def urls(_):
    """List watched URLs."""
    wf = open(WWF).read.splitlines()
    _['send']('\n'.join([x.split(' ', 2)[2] for x in wf]))
