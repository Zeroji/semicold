"""Monitor URL for changes."""
import urllib.request           # Open URLs
import time                     # Timer
import threading                # Threading
import hashlib                  # Check URLs
from cmds import command        # Command dictionary

WWF = 'data/watch'  # Watcher Watch File

settings = open('data/watcher').read().splitlines()
interval = float(settings[0])
channels = settings[1:]
watchout = False

# Started by wrapper
oniichan = threading.Thread(target=nightswatch, daemon='HELL YEAH')


def nightswatch(client):
    """Run the check function repeatedly."""
    global watchout
    start = time.time()
    loop = start + interval
    watchout = True
    while watchout:
        check(client)
        time.sleep(loop - time.time())
        loop += interval

command(name='check', minRank=4)(lambda _: check(_['client']))


def check(client):
    """Check URLs for changes."""
    wf = [x.split(' ', 2) for x in open(WWF).read().splitlines()]
    updates = []
    rewrite = False
    for i, (md5, sha1, url) in enumerate(wf):
        data = b''
        try:
            data = urllib.request.urlopen(url, None, 2).read()
        except:
            pass  # Because we don't really care if it times out.
        md = hashlib.md5(data).hexdigest()
        sh = hashlib.sha1(data).hexdigest()
        if md != md5 or sh != sha1:  # Update!
            if len(md5) * len(sha1) > 0:
                warning = ''  # Warning if the MD5 or SHA1 didn't change
                warning = ' - Identical MD5!!' if md == md5 else warning
                warning = ' - Identical SHA1!!' if sh == sha1 else warning
                updates.append((url, warning))
            wf[i][0] = md
            wf[i][1] = sh
            rewrite = True
    if rewrite:
        open(WWF, 'w').write('\n'.join([' '.join(x) for x in wf]))
    if updates:
        message = '\n'.join([''.join(x) for x in updates])
        for channel in client.get_all_channels():
            if channel.id in channels:
                client.send_message(channel, message)


@command('urls', __name__, help='Prints a list of watched URLs')
def urls(_):
    """List watched URLs."""
    wf = open(WWF).read().splitlines()
    _['send']('\n'.join([x.split(' ', 2)[2] for x in wf]))


@command('add', __name__, help='Adds an URL to watching list', minRank=2)
def addurl(_):
    """Add URL to watchlist."""
    with open(WWF, 'a') as f:
        f.write('  ' + _['T'] + '\n')


@command('rm', __name__, help='Removes an URL from watching list', minRank=2)
def rmurl(_):
    """Remove URL from watchlist."""
    lines = []
    print('removing', _['T'])
    with open(WWF, 'r') as f:
        for l in f.readlines():
            if not l[:-1].endswith(_['T']):
                lines.append(l)
                print("appending", l)
    with open(WWF, 'w') as f:
        for l in lines:
            f.write(l)

# TODO : `;mute` & `;votemute`, `;addch` & `rmch`
