"""Chat module for ;; bot."""
from cmds import command        # Command dictionary
from random import randint      # 8ball
import subprocess               # Used by ping

lenny = '( ͡° ͜ʖ ͡°)'              # Needed for reasons


command('channel', __name__, help='Give current channel information.')(
    lambda _: _['send']('Channel #' + _['message'].channel.name + ' - ID ' +
                        _['cID'], code=1))


@command('del', __name__, minRank=2, help='Delete last N messages from ;;',
         usage='<N>')
def delete(_):
    """Delete the last N messages from the bot."""
    def logs(n, last=None):
        return _['client'].logs_from(_['message'].channel, n, before=last)
    last = list(logs(1))[0]
    try:
        todo = int(_['T'])
    except:
        pass
    else:
        while todo:
            for i, m in enumerate(list(logs(100, last))):
                if i == 99:
                    last = m
                if m.author.id == _['client'].user.id:
                    print('Deleting', m.content)
                    _['client'].delete_message(m)
                    todo -= 1
                    if not todo:
                        return


m8b = {'It is certain', 'It is decidedly so', 'Without a doubt',
       'Yes, definitely', 'You may rely on it', 'As I see it, yes',
       'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
       'Reply hazy try again', 'Ask again later', 'Better not tell you now',
       'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it',
       'My reply is no', 'My sources say no', 'Outlook not so good',
       'Very doubtful'}


@command('8ball', __name__, help=';8ball should I help them?', hidden=True)
def mball(_):
    """."""
    i = randint(0, len(m8b)-1)
    t = '[yup]' if i < 10 else '[...]' if i < 15 else '[nah]'
    _['send'](t + ' ' + m8b[i], 1)


@command('channels', __name__, minRank=1, help='List all channel information.')
def listChannels(_):
    """List channels."""
    channels = []
    maxlength = 0
    for channel in _['message'].channel.server.channels:
        if channel.type == 'text':
            channels.append((channel.position, channel.name, channel.id))
            maxlength = max(maxlength, len(channel.name))
    channels.sort()
    _['send']('\n'.join(['Channel #' + (c[1] + ' ' * maxlength)[:maxlength] +
                         ' - ID ' + c[2] for c in channels]))


command('cookie', __name__, help='Give this man a cookie.', hidden=True)(
    lambda _: _['send'](':cookie:', 0))


command('hug', __name__, help='For the lonely.', hidden=True, private=False)(
    lambda _: _['send']('*hugs ' + _['A'] + '*', 0))


command('hug', __name__, help=lenny, hidden=True, privateOnly=True)(
    lambda _: _['send']('Oh, ' + _['A'] + '... you want to get into this?' +
                        'But.. you know we can\'t...', 0))


@command('info', __name__, minRank=1, help='Get member information',
         usage='<name|ID> ...', private=False)
def info(_):
    """Give info about members."""
    for target in _['P'][0:]:
        for m in _['message'].channel.server.members:
            if target in (m.name, m.id):
                roles = ', '.join([r.name for r in m.roles])
                roles = roles.replace('@everyone', 'Default')
                roles = roles.replace('Trusted', 'Purple')
                _['send']('Member ' + m.name + ', roles: ' + roles +
                          ' - ID: ' + m.id, code=1)


command('lmgtfy', __name__, help='Googles that for you.', usage='<text>')(
    lambda _: _['send']('http://lmgtfy.com/?q=' + '+'.join(_['P'][1:]), 0))


@command('ping', __name__, help='Give ping statistics for a given URL',
         usage='<URL>', minRank=1)
def ping(_):
    """Print ping statistics for an URL."""
    process = subprocess.Popen(['ping', '-q', '-c', '4', '-i', '0.2', _['T']],
                               stdout=subprocess.PIPE)
    process.wait()
    lines = [l.decode('ascii') for l in process.stdout]
    if len(lines) == 5:
        _['send'](''.join(lines[-2:]))


command('ok', __name__, help='OK.', hidden=True)(
    lambda _: _['send']('http://i.imgur.com/XtC4At2.jpg', 0))


command('say', __name__, minRank=1, help='Repeat', usage='<text>')(
    lambda _: _['send'](_['T'], 0))


command('tts', __name__, minRank=1, help='Text-to-speech', usage='<text>')(
    lambda _: _['send'](_['T'], 0, tts=True))


command('xkcd', __name__, help='xkcd', usage='<N>', hidden=True)(
    lambda _: _['send']('http://xkcd.com/' + _['T'] + '/', code=0))
