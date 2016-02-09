"""Launcher for ;; bot."""
import os                       # Checking for source updates
import sys                      # Checking for source updates
import asyncio                  # Discord requirement
import discord                  # Discord API wrapper
import core                     # ;; main source code
from cmds import stime          # Had to put it somewhere


class Client(discord.Client):
    """Wrapper around discord.Client class."""

    def __init__(self, master='', admins=None):
        """Init client."""
        super(Client, self).__init__()
        self.running = False
        self.master = master
        self.admins = admins
        self.check_updates = True
        self.sources = []
        self.last_updated = 0
        self._watchlist = ([], [])

    def watch(self, *user_ids):
        """Add users to watchlist."""
        self._watchlist[0].extend(list(user_ids))

    def watch_output(self, *channels):
        """Add channels to watcher output."""
        self._watchlist[1].extend(list(channels))

    def update(self, val):
        """Set the auto-update behavior."""
        self.check_updates = val

    def run(self, login, password):
        """Start the client."""
        if self.check_updates:
            self.sources = [f for f in os.listdir('.') if f.endswith('.py')]
            self.last_updated = max([os.stat(f)[8] for f in self.sources])
        self.running = True
        super(Client, self).run(login, password)

    @asyncio.coroutine
    def play(self, game_name):
        """Change client game."""
        game = discord.Game
        game.name = game_name
        yield from self.change_status(game=game)

    @asyncio.coroutine
    def on_member_update(self, _, after):
        """Monitor status updates and change AFK state accordingly. Also watch users."""
        if after.id in self._watchlist[0]:
            for channel in self.get_all_channels():
                if channel.id in self._watchlist[1]:
                    print(channel.name, after.name, _.status.name, after.status.name)
                    yield from self.send_message(channel, ('`Status update: ' + after.name +
                                                           ' went ' + after.status.name + '`'))
        try:
            user = core.afk.AFK.get(after.id)
        except AttributeError:
            pass
        else:
            if user and user.is_set():
                user.check(self)

    @asyncio.coroutine
    def on_message(self, message):
        """Handle messages from Discord."""
        text, author_id, author = message.content, message.author.id, message.author.name

        if self.check_updates:  # Update check
            edit_time = max([os.stat(f)[8] for f in self.sources])
            if edit_time > self.last_updated or (text == 'RLD' and author_id in self.admins):
                print(stime() + ' reloading')
                os.execl(sys.executable, *([sys.executable]+sys.argv))

        if author_id in self.admins and text == ';masterkill':
            print(stime() + ' masterkill by ' + author)
            self.running = False
            self.client.logout()
            exit(0)
        elif author_id in self.admins and text == ';kill':
            print(stime() + ' killed by ' + author)
            self.running = False
        elif author_id in self.admins and text == ';reload':
            print(stime() + ' reloaded by ' + author)
            self.running = True
            yield from self.send_message(message.channel, '`Bot reloaded.`')
        elif self.running:
            yield from core.process(self, message, self.admins)

    @asyncio.coroutine
    def on_ready(self):
        """Initialize bot."""
        # Taking good habits
        yield from self.change_status(idle=True)
        try:
            core.watcher.start(self)
        except AttributeError:
            print('Error loading watcher.')


def main():
    """Main function."""
    # Fetching login data
    with open('data/login', 'r') as login_file:
        email = login_file.readline()[:-1]
        passw = login_file.readline()[:-1]

    # Fetching master/admin data
    master_id = '111100569845784576'
    with open('data/admins') as admin_file:
        admins = admin_file.read().splitlines()

    client = Client(master_id, admins)
    client.play('with StuffBot')
    client.watch('143120006618677248', '142356131837116417')
    client.watch_output('133648084671528961', '142370164376076288', '142380636915630080')
    client.run(email, passw)

if __name__ == '__main__':
    main()
