"""Core of ;; program."""
from cmds import cmd, command   # Command dictionary
import chat
import cipher
import image
import math_
import string_
import watcher

prefix = ';'
moduleNames = {'math_': 'math', 'string_': 'string'}  # Because it's prettier.


# command: min/max rank, channel B/W list, private

# cmd['rot'] = [0, None, True, "Rot things", 'send', True, cipher.rot, ('%T',)]


@command('source', __name__, help='Sauce!')
def source(_):
    """Link to the source."""
    _['send']('`;; source code` http://github.com/Zeroji/semicolon')


@command('request', __name__, help='Request a feature', usage='<text>')
def request(_):
    """Log requests from users."""
    with open('data/requests', 'a') as f:
        try:
            f.write(_['T'], '\n')
            _['send']('Your request has been heard.', 1)
        except:
            pass


@command('report', __name__, help='Report a bug/misbehaviour.', usage='<text>')
def report(_):
    """Log bug reports from users."""
    with open('data/bugs', 'a') as f:
        try:
            f.write(_['T'], '\n')
            _['send']('Thank you for your report.', 1)
        except:
            pass


@command('commands', __name__, help='List all commands available.',
         usage='[<module>]')
def commands(_):
    """List all commands available to the user."""
    ls = {}
    for name in cmd.keys():
        for c in cmd[name]:
            if access(c, _['rank'], _['private'], _['bot'], _['cID']):
                if not c['hidden']:
                    module = c[1]
                    if module in moduleNames.keys():
                        module = moduleNames[module]
                    if module not in ls.keys():
                        ls[module] = []
                    ls[module].append((name, c))
    lk = list(ls.keys())
    if _['T']:
        module = _['T']
        if module not in lk:
            _['send']('Invalid module name.', 1)
        else:
            ls = ls[module]
            ls.sort()
            _['send']('\n'.join([((prefix if c['reversible'] else '') +
                                 prefix + name + ' ' + c['usage']).ljust(26) +
                                 c['help'] for name, c in ls]))
    else:
        lk.sort()
        for k in lk:
            ls[k].sort()
        _['send']('\n'.join([(k + ':').ljust(12) + ' '.join([';' +
                             c[0] for c in ls[k]]) for k in lk]))


print('`' + '`, `'.join(cmd) + '`')


def access(c, rank=0, chan='', private=False, bot=False):
    """Tell if one can use a command."""
    if rank < c['minRank']:
        return False
    if c['maxRank'] is not None and rank > c['maxRank']:
        return False
    if c['channelBlackList'] is not None and chan in c['channelBlackList']:
        return False
    if c['channelWhiteList'] is not None and chan not in c['channelWhiteList']:
        return False
    if bot and not c['botsAllowed']:
        return False
    if private and not c['private']:
        return False
    if not private and c['privateOnly']:
        return False
    return True


def process(client, message, admins):
    """Handle commands."""
    # code = 0 is plaintext
    # code = 1 is a code line
    # code = 2 is a code block
    def reply(text, code=2, pm=False, mentions=True, tts=False):
        """Reply stuff with some options."""
        destination = message.author if pm else message.channel
        if code == 1:
            text = '`' + text.replace('\n', '') + '`'
        elif code == 2:
            text = '`' * 3 + ('\n' if '\n' in text else '') + text + '`' * 3
        client.send_message(destination, text, mentions, tts)

    # S, ID, A contain message, author name, author ID
    S, ID, A = message.content, message.author.id, message.author.name
    cID = message.channel.id

    # Hacking stuff
    transforms = ('asc', 'b64', 'bin', 'dec', 'hex', 'utf')
    if(len(S) > 8 and S[0] == ';' and S[7] == ' ' and
       S[1:4].lower() in transforms and S[4:7].lower() in transforms):
        S = ';transform ' + S[1:4] + ' ' + S[4:]

    # C and T contain command and parameter
    # P contains list of parameters
    # L contains list of what comes after
    # if you have ;<C> <arg> <arg> <text>
    # then it'll be C P[1] P[2] L[3]
    C, T, P, L, R = '', '', [], [], False
    if S.startswith(prefix):
        if len(S) > 1 and S[1] == prefix:
            R = True
            S = S[1:]
        P = S[1:].split()
        if len(P) > 0:
            C = P[0]
            L = [' '.join(P[n:]) for n in range(len(P))]
            T = ' '.join(P[1:])

    private = message.channel.is_private
    rank, bot = 0, False
    if not private:
        for role in message.author.roles:
            if role.name not in ('@everyone', 'Bots'):
                rank = 1
            if role.name == 'Bots':
                bot = True
    # if ID in managers: rank = 2
    if ID in admins:
        rank = 3 + int(ID == '111100569845784576')
# def command(name, minRank=0, maxRank=None, private=True, privateOnly=False,
#             channelBlackList=None, channelWhiteList=None, help='', usage='',
#             botsAllowed=True, reversible=False):
    # if '<@' in S: # afk
    if C in cmd.keys():
        for c in cmd[C]:
            if not access(c, rank, private, bot, cID):
                continue
            c[0]({'S': S, 'ID': ID, 'A': A, 'P': P, 'L': L, 'T': T, 'R': R,
                  'send': reply, 'private': private, 'rank': rank, 'cID': cID,
                  'client': client, 'message': message, 'bot': bot})
