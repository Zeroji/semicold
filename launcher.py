"""Launcher for ;; bot."""
import os                       # Checking for source updates
import sys                      # Checking for source updates
import discord                  # Discord API wrapper
import core                     # ;; main source code
from cmds import stime          # Had to put it somewhere

# Fetching login data
LOGIN_FILE = open('data/login')
EMAIL = LOGIN_FILE.readline()[:-1]
PASSW = LOGIN_FILE.readline()[:-1]
LOGIN_FILE.close()

# Logging in
CLIENT = discord.Client()
CLIENT.login(EMAIL, PASSW)
EMAIL, PASSW = None, None

# Fetching master/admin data
MASTER_ID = '111100569845784576'
ADMIN_FILE = open('data/admins')
ADMINS = ADMIN_FILE.read().splitlines()
ADMIN_FILE.close()

# Update data
SOURCES = [f for f in os.listdir('.') if f.endswith('.py')]
LAST_UPDATED = max([os.stat(f)[8] for f in SOURCES])
RUNNING = True


@CLIENT.event
def on_message(message):
    """Handle messages from Discord."""
    global RUNNING

    text, author_id, author = message.content, message.author.id, message.author.name

    # Update check
    sources = [f for f in os.listdir('.') if f.endswith('.py')]
    edit_time = max([os.stat(f)[8] for f in sources])

    if edit_time > LAST_UPDATED or (text == 'RLD' and author_id in ADMINS):
        print(stime() + ' reloading')
        os.execl(sys.executable, *([sys.executable]+sys.argv))

    if author_id in ADMINS and text == ';masterkill':
        print(stime() + ' masterkill by ' + author)
        RUNNING = False
        CLIENT.logout()
        exit(-1)
    elif author_id in ADMINS and text == ';kill':
        print(stime() + ' killed by ' + author)
        RUNNING = False
    elif author_id in ADMINS and text == ';reload':
        print(stime() + ' reloaded by ' + author)
        RUNNING = True
        CLIENT.send_message(message.channel, '`Bot reloaded.`')
    elif RUNNING:
        core.process(CLIENT, message, ADMINS)


@CLIENT.event
def on_ready():
    """Initialize bot."""
    # Taking good habits
    CLIENT.change_status(None, True)
    try:
        core.watcher.start(CLIENT)
    except AttributeError:
        print('Error loading watcher.')

# FINISH HIM!
CLIENT.run()
