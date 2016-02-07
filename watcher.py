"""Monitor URL for changes."""
import requests                 # Open URLs
import time                     # Timer
import threading                # Threading
import hashlib                  # Check URLs
from cmds import command        # Command dictionary
from message import Message

WWF = 'data/watch'  # Watcher Watch File

settings = open('data/watcher').read().splitlines()
interval = float(settings[0])
channels = settings[1:]
watchout = False
silenced = False


def nightswatch(client):
    """Run the check function repeatedly."""
    global watchout
    watchout = True
    while watchout:
        check(client)
        time.sleep(interval)


def check(client):
    """Check URLs for changes."""
    wf = [x.split(' ', 2) for x in open(WWF).read().splitlines() if len(x) > 0]
    updates = []
    rewrite = False
    for i, (md5, sha1, url) in enumerate(wf):
        data = b''
        try:
            r = requests.get(url, timeout=2, stream=True)
            try:
                size = int(r.raw.header['Content-Type'])
            except Exception:
                pass
            else:
                if size > 2**20:
                    raise Exception

            data = r.raw.read()
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
        with open(WWF, 'w') as f:
            for x in wf:
                f.write(' '.join(x) + '\n')
    if updates and not silenced:
        message = '\n'.join([''.join(x) for x in updates])
        for channel in client.get_all_channels():
            if channel.id in channels:
                client.send_message(channel, message)


@command('urls', __name__, help='Prints a list of watched URLs')
def urls(_):
    """List watched URLs."""
    wf = open(WWF).read().splitlines()
    return Message('\n'.join([x.split(' ', 2)[2] for x in wf]), Message.BLOCK)


@command('add', __name__, help='Adds an URL to watching list', minRank=2,
         usage='<URL>')
def addurl(_):
    """Add URL to watchlist."""
    with open(WWF, 'a') as f:
        f.write('  ' + _['T'] + '\n')


@command('rm', __name__, help='Removes an URL from watching list',
         minRank=2, usage='<URL>')
def rmurl(_):
    """Remove URL from watchlist."""
    lines = []
    with open(WWF, 'r') as f:
        for l in f.read().splitlines():
            if not l.split(' ', 2)[-1] == _['T']:
                lines.append(l)
    with open(WWF, 'w') as f:
        for l in lines:
            f.write(l + '\n')


@command('interval', __name__, help='Set or get the current check interval.',
         minRank=2, usage='[<value>]')
def setInterval(_):
    """Command to set/get watcher interval."""
    global interval
    try:
        val = float(_['T'])
    except:
        return Message('Current delay between checks is ' + str(interval) + 's.')
    else:
        if val < 5 or val > 600:
            return Message('Interval must be set between 5 and 600 seconds.')
        else:
            interval = val
            with open('data/watcher', 'w') as f:
                f.write(str(val) + '\n')
                for channel in channels:
                    f.write(channel + '\n')
            return Message('Interval set to ' + str(val) + ' seconds.')


def rewrite():
    """Rewrite information to data file."""
    with open('data/watcher', 'w') as f:
        f.write(str(interval) + '\n')
        for channel in channels:
            f.write(channel + '\n')


@command('lsch', __name__, minRank=2, help='List output channels.')
def listChannels(_):
    """List output channels."""
    return Message(' '.join(channels))


@command('addch', __name__, minRank=2, help='Add output channel.',
         usage='<channel name|ID>')
def addChannel(_):
    """Add a channel to the list of output channels."""
    global channels
    serverChannels = list(_['message'].channel.server.channels)
    valid = _['T'] in [c.name for c in serverChannels]
    valid = valid or _['T'] in [c.id for c in serverChannels]
    if not valid:
        return Message('Invalid channel name/ID.')
    else:
        channels.append(_['T'])
        rewrite()
        return Message('Channel ' + _['T'] + ' added.')


@command('rmch', __name__, minRank=2, help='Remove output channel.',
         usage='<channel name|ID>')
def removeChannel(_):
    """Remove a channel from the list of output channels."""
    global channels
    if _['T'] not in channels:
        return Message('Invalid channel. Type ;lsch to list output channels.')
    else:
        channels = [channel for channel in channels if channel != _['T']]
        rewrite()
        return Message('Channel ' + _['T'] + ' removed.')


@command('mute', __name__, minRank=2,
         help='Mute watcher output. Does not stop it from checking websites.')
def mute(_):
    """Mute watcher."""
    global silenced
    if silenced:
        return Message('Already muted.')
    else:
        return Message('Watcher muted. Type ;unmute to unmute.')
        silenced = True


@command('unmute', __name__, minRank=2, help='Unmute watcher.')
def unmute(_):
    """Unmute watcher."""
    global silenced
    if not silenced:
        return Message('Not muted.')
    else:
        silenced = False
        return Message('Watcher unmuted.')


def start(client):
    """Start watching process."""
    oniichan = threading.Thread(target=nightswatch, args=(client,), daemon=True)
    oniichan.start()


@command('wkill', __name__, minRank=3, help='Effectively kill watcher.')
def wkill(_):
    """Kill watcher process."""
    global watchout
    watchout = False
    return Message('And now his watch is ended.')


@command('watch', __name__, minRank=3, help='Restart watcher thread.')
def watch(_):
    """Restart watcher thread."""
    start(_['client'])
    return Message('Night gathers, and now my watch begins.')
