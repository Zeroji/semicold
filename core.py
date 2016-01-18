import discord                  # Discord API
import time                     # Get time
from cmds import cmd, command   # Command dictionary
import cipher

prefix = ';'

# command: min/max rank, channel B/W list, private

# cmd['rot'] = [0, None, True, "Rot things", 'send', True, cipher.rot, ('%T',)]


@command('help', help='Print this help.')
def help(client, message, S, ID, A, C, L, T, R):
    client.send_message(message.channel, 'Halp!')

print(cmd)


def process(client, message, admins):
    """Handle commands."""
    # S, ID, A contain message, author name, author ID
    # C and T contain command and parameter
    # P contains list of parameters
    # L contains list of what comes after
    # if you have ;<C> <arg> <arg> <text>
    # then it'll be C P[1] P[2] L[3]
    S, ID, A = message.content, message.author.id, message.author.name
    cID = message.channel.id
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
# def command(name, minrank=0, maxrank=None, private=True, privateonly=False,
#             channelBlackList=None, channelWhiteList=None, help='', usage='',
#             botsAllowed=True, reversible=False):
    # if '<@' in S: # afk
    if C in cmd.keys():
        for c in cmd[C]:
            if c['minRank'] > rank:
                continue
            if c['maxRank'] and c['maxRank'] < rank:
                continue
            if private and not c['private']:
                continue
            if not private and c['privateOnly']:
                continue
            if c['channelBlackList'] and cID in c['channelBlackList']:
                continue
            if c['channelWhiteList'] and cID not in c['channelWhiteList']:
                continue
            if bot and not c['botsAllowed']:
                continue
            c[0](client, message, S, ID, A, P, L, T, R)
