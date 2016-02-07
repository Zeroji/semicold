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
            self.client.send_message(message.channel, '`Bot reloaded.`')
        elif self.running:
            yield from core.process(self, message, self.admins)

    @asyncio.coroutine
    def on_ready(self):
        """Initialize bot."""
        # Taking good habits
        self.change_status(None, True)
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
    client.run(email, passw)

if __name__ == '__main__':
    main()
