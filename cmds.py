cmd = {}


def command(name, minRank=0, maxRank=None, private=True, privateOnly=False,
            channelBlackList=None, channelWhiteList=None, help='', usage='',
            botsAllowed=True, reversible=False):
    """Register commands."""
    def _(f):
        if name not in cmd.keys():
            cmd[name] = []
        c = {0: f, 'minRank': minRank, 'maxRank': maxRank, 'private': private,
             'privateOnly': privateOnly, 'channelBlackList': channelBlackList,
             'channelWhiteList': channelWhiteList, 'botsAllowed': botsAllowed,
             'help': help, 'usage': usage, 'reversible': reversible}
        if c not in cmd[name]:
            cmd[name].append(c)
    return _
