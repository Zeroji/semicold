"""AFK module for ;; bot."""
import discord
from cmds import command
from message import Message


class AFKUser:
    """AFK user."""

    def __init__(self, line, user_id):
        """Initialization."""
        self.user_id = user_id
        self.message = {}
        data = line.split('{~}')
        (self.is_afk, self.pm_settings, self.pm_count,
         self.afk_on_idle, self.afk_on_offline) = [int(x) for x in data[:5]]
        self.message['main'], self.message['afk'], self.message['back'] = data[-3:]
        self.pm_settings = int(self.pm_settings)

    def line(self):
        """Return formatted line to save."""
        return '{~}'.join([str(int(x)) for x in (self.is_afk, self.pm_settings, self.pm_count,
                                                 self.afk_on_idle, self.afk_on_offline)] +
                          [self.message[key] for key in ('main', 'afk', 'back')])

    def check(self, client):
        """Update the AFK status."""
        status = discord.Status.offline
        for member in client.get_all_members():
            if member.id == self.user_id:
                status = member.status
        if self.is_afk:
            if status == discord.Status.online:
                if self.afk_on_idle or self.afk_on_offline:
                    self.is_afk = self.is_afk  # False
            elif status == discord.Status.idle:
                if not self.afk_on_idle or self.afk_on_offline:
                    self.is_afk = self.is_afk  # False
        else:
            if status == discord.Status.idle:
                if self.afk_on_idle:
                    self.is_afk = True
            elif status == discord.Status.offline:
                if self.afk_on_offline:
                    self.is_afk = True

    def is_set(self):
        """Check if the user settings are correct."""
        return self.pm_count >= 0 and self.message['main'] != ''

    def afk(self):
        """Set user as AFK."""
        self.is_afk = True
        self.pm_count = 0

    def back(self):
        """Set user as not AFK."""
        self.is_afk = False

    def trigger(self, message, client):
        """Mention from someone."""
        self.check(client)
        print(self.is_afk)
        if not self.is_afk:
            return
        return Message(message.author.mention + ' ' + self.message['main'], Message.PLAIN)


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


@command('afk', __name__, private=False, help='Be afk')
def enter_afk(_):
    """Enter AFK state or configure it."""
    user_id = _['message'].author.id
    user = AFK.get(user_id)
    print(_['A'], user)
    if user is None or not user.is_set():
        return (Message('Please set your afk parameters through PM.'),
                Message('Type ;afk for more information.', private=True))
    elif not user.is_afk:
        print(user.user_id, user.message)
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
        print(user.user_id, user.message)
        user.back()
        AFK.save(AFK_PATH)
        message = user.message['back']
        if message:
            return Message(message, Message.PLAIN)
