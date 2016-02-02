"""Provide command dictionary and decorator to register commands."""
import time                     # Used for stime

cmd = {}


def command(name, module='', minRank=0, maxRank=None, private=True,
            privateOnly=False, channelBlackList=None, channelWhiteList=None,
            help='', usage='', botsAllowed=True, reversible=False,
            hidden=False):
    """Register commands."""
    def _(f):
        if name not in cmd.keys():
            cmd[name] = []
        c = {0: f, 'minRank': minRank, 'maxRank': maxRank, 'private': private,
             'privateOnly': privateOnly, 'channelBlackList': channelBlackList,
             'channelWhiteList': channelWhiteList, 'botsAllowed': botsAllowed,
             'help': help, 'usage': usage, 'reversible': reversible,
             'hidden': hidden, 1: module}
        if c not in cmd[name]:
            cmd[name].append(c)
    return _


# I had to put that somewhere
def stime():
    """Return current time formatted like 2016-12-31T23:59:59."""
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
