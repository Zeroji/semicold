"""Core of ;; program."""
from cmds import cmd, command   # Command dictionary
import asyncio
from message import Message
import chat
import cipher
import image
import math_
import string_
import watcher
import subprocess

prefix = ';'
moduleNames = {'math_': 'math', 'string_': 'string'}  # Because it's prettier.


# command: min/max rank, channel B/W list, private

# cmd['rot'] = [0, None, True, "Rot things", 'send', True, cipher.rot, ('%T',)]


@command('source', __name__, help='Sauce!')
def source(_):
    """Link to the source."""
    return Message('`;; source code` http://github.com/Zeroji/semicolon', Message.PLAIN)


@command('pull', __name__, help='Execute `git pull`', minRank=4)
def pull(_):
    """Pull source code from github."""
    process = subprocess.Popen(['git', 'pull'], stdout=subprocess.PIPE)
    try:
        process.wait(5)
    except:
        return Message('Runtime error', 1)
        process.kill()
        process.wait()
        raise
    else:
        lines = [l.decode('ascii').ljust(80) for l in process.stdout]
        return Message(('Executing \\`git pull\\` in \\`~/semicolon/\\`\n`' +
                        '`\n`'.join(lines) + '`'), Message.PLAIN)


@command('request', __name__, help='Request a feature', usage='<text>')
def request(_):
    """Log requests from users."""
    with open('data/requests', 'a') as f:
        try:
            f.write(_['T'] + '\n')
            return Message('Your request has been heard.')
        except:
            pass


@command('report', __name__, help='Report a bug/misbehaviour.', usage='<text>')
def report(_):
    """Log bug reports from users."""
    with open('data/bugs', 'a') as f:
        try:
            f.write(_['T'] + '\n')
            return Message('Thank you for your report.', 1)
        except:
            pass


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


def commandList(_, show=False):
    """Return a dictionary of commands."""
    ls = {}
    for name in cmd.keys():
        for c in cmd[name]:
            if access(c, _['rank'], _['private'], _['bot'], _['cID']):
                if not c['hidden'] or show:
                    module = c[1]
                    if module in moduleNames.keys():
                        module = moduleNames[module]
                    if module not in ls.keys():
                        ls[module] = []
                    ls[module].append((name, c))
    return ls


@command('about', __name__, help='About me :3')
def about(_):
    """Basic information about me."""
    return Message('Small bot in Python. Does stuff. Type ;; or ask Zeroji for more.')


@command('bots', __name__, help='Lists bots.', hidden=True)
def bots(_):
    """List bots."""
    r = ('Hi, ;; here. I do stuff. I halp. Type ;; for moar. PM also works.' +
         '\nI\'m not alone here, you can type !bots to have more information' +
         '.\nBots detected: ')
    for m in _['message'].channel.server.members:
        if m.status != 'offline' and 'Bots' in [x.name for x in m.roles]:
            r += m.name + ', '
    return Message(r[:-2], Message.BLOCK)


@command('help', __name__, help='Print help.', usage='[<command>|<module>]')
def helpCommand(_):
    """Help about bot, command, or module."""
    ls = commandList(_, show=True)
    if _['T']:
        name = _['T']
        ismodule = True
        for k in ls.keys():
            for n, c in ls[k]:
                if n == name:
                    ismodule = False
                    message = 'Command: `' + prefix + n + '`'
                    if c['reversible']:
                        message += (' (reversible by calling `' + prefix * 2 +
                                    name + '`)')
                    message += ('\nUsage: `' + prefix + name + ' ' +
                                c['usage'] + '`\n' + c['help'])
                    return Message(message, Message.PLAIN)
        if ismodule:
            if _['T'] not in ls.keys():
                return Message('Invalid module/command name.')
                return
            ls = ls[_['T']]
            ls.sort()
            return Message('\n'.join([((prefix if c['reversible'] else '') +
                           prefix + name + ' ' + c['usage']).ljust(28) +
                           c['help'] for name, c in ls]), Message.BLOCK)
    else:
        return Message('Hi, I\'m ;; :smile: I\'m split into several modules,' +
                       ' you can type `;help <module>` for more information.', Message.PLAIN)
        return Message('Here are my modules: `' + '`, `'.join(ls.keys()) + '`', Message.PLAIN)


@command('commands', __name__, help='List all commands available.',
         usage='[<module>]')
def commands(_):
    """List all commands available to the user."""
    ls = commandList(_)
    lk = list(ls.keys())
    if _['T']:
        module = _['T']
        if module not in lk:
            return Message('Invalid module name.')
        else:
            ls = ls[module]
            ls.sort()
            return Message('\n'.join([((prefix if c['reversible'] else '') +
                           prefix + name + ' ' + c['usage']).ljust(28) +
                           c['help'] for name, c in ls]), Message.BLOCK)
    else:
        lk.sort()
        for k in lk:
            ls[k].sort()
        return Message('\n'.join([(k + ':').ljust(12) + ' '.join([';' +
                       c[0] for c in ls[k]]) for k in lk]), Message.BLOCK)


@asyncio.coroutine
def process(client, message, admins):
    """Handle commands."""
    # @asyncio.coroutine
    # def reply(text, code=2, pm=False, tts=False):
    #     """Reply stuff with some options."""
    #     destination = message.author if pm else message.channel
    #     if code == 1:
    #         text = '`' + text.replace('\n', '') + '`'
    #     elif code == 2:
    #         text = '`' * 3 + ('\n' if '\n' in text else '') + text + '`' * 3
    #     print(destination.name, text)
    #     yield from client.send_message(destination, text)

    # S, ID, A contain message, author name, author ID
    S, ID, A = message.content, message.author.id, message.author.name
    cID = message.channel.id

    # Hacking stuff
    transforms = ('asc', 'b64', 'bin', 'dec', 'hex', 'utf')
    if(len(S) > 8 and S[0] == ';' and S[7] == ' ' and
       S[1:4].lower() in transforms and S[4:7].lower() in transforms):
        S = ';transform ' + S[1:4] + ' ' + S[4:]

    if S == ';;':
        S = ';commands'

    if S == '!bots':
        yield from client.send_message(message.channel, ('`Hi, ;; here. I do stuff. I halp.' +
                                                         ' Type ;; for moar. PM also works.'))

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
            output = c[0]({'S': S, 'ID': ID, 'A': A, 'P': P, 'L': L, 'T': T, 'R': R,
                           'private': private, 'rank': rank, 'cID': cID,
                           'client': client, 'message': message, 'bot': bot})
            if type(output) == Message:
                output = (output,)
            for mess in output:
                yield from client.send_message(mess.get_channel(message.author, message.channel),
                                               mess.text, tts=mess.tts)
