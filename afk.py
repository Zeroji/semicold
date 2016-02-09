"""AFK module for ;; bot."""
from time import time
import discord
from cmds import command
from message import Message


class AFKUser:
    """AFK user."""

    def __init__(self, line, user_id):
        """Initialization."""
        self.user_id = user_id
        self.afk_on = {}
        self.message = {}
        data = line.split('{~}')
        (self.is_afk, self.pm_settings, self.pm_count,
         self.afk_on['idle'], self.afk_on['off'], self.afk_on['type']) = [int(x) for x in data[:6]]
        self.message['msg'], self.message['afk'], self.message['back'], self.last_seen = data[6:]
        self.last_seen = int(self.last_seen)
        self.pm_settings = int(self.pm_settings)

    def line(self):
        """Return formatted line to save."""
        return '{~}'.join([str(int(x)) for x in (self.is_afk, self.pm_settings, self.pm_count,
                                                 self.afk_on['idle'], self.afk_on['off'],
                                                 self.afk_on['type'])] +
                          [self.message[key] for key in ('msg', 'afk', 'back')] +
                          [str(self.last_seen)])

    def check(self, client):
        """Update the AFK status."""
        status = discord.Status.offline
        for member in client.get_all_members():
            if member.id == self.user_id:
                status = member.status
        if self.is_afk:
            if status == discord.Status.online:
                if self.afk_on['idle'] or self.afk_on['off']:
                    self.back()
            elif status == discord.Status.idle:
                if not self.afk_on['idle'] or self.afk_on['off']:
                    self.back()
        else:
            if status == discord.Status.idle:
                if self.afk_on['idle']:
                    self.afk()
            elif status == discord.Status.offline:
                if self.afk_on['off']:
                    self.afk()
        print(self.is_afk)

    def is_set(self):
        """Check if the user settings are correct."""
        return self.pm_count >= 0 and self.message['msg'] != ''

    def afk(self):
        """Set user as AFK."""
        self.is_afk = True
        self.pm_count = 0
        self.last_seen = int(time())

    def back(self):
        """Set user as not AFK."""
        self.is_afk = False

    def trigger(self, message, client):
        """Mention from someone."""
        if not self.is_afk:
            return
        msg = self.message['msg']
        msg = msg.replace('%mention%', message.author.mention)
        if '%me%' in msg:
            for member in client.get_all_members():
                if member.id == self.user_id:
                    msg = msg.replace('%me%', member.name)
        if '%for%' in msg:
            delta = int(time() - self.last_seen)
            alpha = 'long'
            if delta < 1:
                alpha = 'a strange amount of time'
            elif delta < 10:
                alpha = 'a few seconds'
            elif delta < 60:
                alpha = str(delta) + ' seconds'
            elif delta < 120:
                alpha = 'one minute'
            elif delta < 3600:
                alpha = str(delta // 60) + ' minutes'
            elif delta < 7200:
                alpha = 'one hour'
            elif delta < 86400:
                alpha = str(delta // 3600) + ' hours'
            elif delta < 132800:
                alpha = 'one day'
            else:
                alpha = str(delta // 86400) + ' days'
            msg = msg.replace('%for%', alpha)
        return Message(msg, Message.PLAIN)


# Ne faites pas d'enfants, mais pensez à eux quand même
# Pour une meilleure planète, recyclez vos capotes


class AFKList:
    """AFK list."""

    def __init__(self):
        """Initialization."""
        self.users = {}

    def load(self, filename):
        """Load contents from file."""
        with open(filename, 'r') as afk_file:
            self.users = {}
            for lines in afk_file.read().splitlines():
                user_id, data = lines.split(':', 1)
                self.users[user_id] = AFKUser(data, user_id)

    def save(self, filename):
        """Save contents to file."""
        with open(filename, 'w') as afk_file:
            for user in self.users.keys():
                afk_file.write(user + ':')
                afk_file.write(self.users[user].line())
                afk_file.write('\n')

    def get(self, user_id):
        """Get AFKUser object from id."""
        return self.users[user_id] if user_id in self.users.keys() else None


AFK_PATH = 'data/afk'
AFK = AFKList()
AFK.load(AFK_PATH)


@command('afk', __name__, help='Be afk')
def enter_afk(_):
    """Enter AFK state or configure it."""
    user_id = _['message'].author.id
    user = AFK.get(user_id)
    if user is None or not user.is_set():
        return (Message('Please set your afk parameters through PM.'),
                Message('Type ;afk for more information.', private=True))
    elif not user.is_afk:
        user.afk()
        AFK.save(AFK_PATH)
        message = user.message['afk']
        if message:
            return Message(message, Message.PLAIN)


@command('back', __name__, help='Be back', hidden=True)
def leave_afk(_):
    """Leave AFK."""
    user_id = _['message'].author.id
    user = AFK.get(user_id)
    if user is not None and user.is_set() and user.is_afk:
        user.back()
        AFK.save(AFK_PATH)
        message = user.message['back']
        if message:
            return Message(message, Message.PLAIN)


@command('afkset', __name__, help='Set your AFK parameters', privateOnly=True,
         usage='<parameter> <value>')
def afk_setting(_):
    """Set the AFK parameters."""
    print('setting')
    user_id = _['message'].author.id
    user = AFK.get(user_id)
    if user is None:
        user = AFKUser('0{~}0{~}1{~}0{~}0{~}unset{~}{~}', user_id)
        AFK.users[user_id] = user
    was_set = user.is_set()
    output = []

    keys = ('msg', 'afk', 'back', 'pms', 'idle', 'off', 'type')
    if len(_['P']) >= 3 and _['P'][1] in keys:
        key = _['P'][1]
        val = _['L'][2]
        if key == 'pm':
            val = -1 if val == 'never' else val
            val = 0 if val == 'always' else val
            try:
                val = int(val)
            except ValueError:
                pass
            else:
                user.pm_settings = val
                message = ('You will ' + ('always' if not val else '') +
                           ('never' if val < 0 else '') + ' be sent ')
                if val > 0:
                    message += 'at most ' + str(val)
                output.append(Message(message + 'notifications.'))
        elif key in keys[-3:]:
            val = val in ('TRUE', 'True', 'true', 1)
            user.afk[key] = val
            message = 'You will ' + ('' if val else 'not ') + 'be considered '
            message += ('back' if key == 'type' else 'AFK') + ' when you '
            message += {'type': 'send a message.', 'idle': 'are idle.', 'off': 'are offline.'}[key]
            output.append(Message(message))
        else:
            val = val.replace('\n', '').replace('http://', '').replace('https://', '')[:200]
            user.message[key] = val
            message = ('Your ' + {'msg': 'main AFK', 'afk': ';afk', 'back': ';back'}[key] +
                       ' message has been set to:\n' + val)
        AFK.save(AFK_PATH)
    else:
        output.append(Message('Use `;afkset <parameter> <value>` to set your preferences. '
                              'Parameters:\n'
                              'msg  - Message sent when one mentions you.\n'
                              'afk  - Message printed when you go afk.\n'
                              'back - Message printed when you\'re back.\n'
                              'pm   - <never|always|N> Sends you a PM when one mentions you.\n'
                              'idle - <true|false> Auto-AFK when your status is idle\n'
                              'off  - <true|false> Auto-AFK when your status is offline\n'
                              'type - <true|false> Auto-back when you send a message',
                              Message.BLOCK))
        output.append(Message('Messages can be at most 200 characters long, and cannot contain '
                              'newlines or links. You can use `%mention%` to mention who talked '
                              'to you, %me% to insert your name and `%for%` to tell for how long '
                              'you are AFK. (like "2 hours")',
                              Message.PLAIN))

    if user.is_set() and not was_set:
        output.append(Message('Your parameters have been set properly. '
                              'You can now user ;afk and ;back.'))
    return output
