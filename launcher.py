"""Launcher for ;; bot."""
import discord                  # Discord API wrapper
import core                     # ;; main source code
import os                       # Checking for source updates
from imp import reload          # Reloading source code
import traceback                # Handling errors
from cmds import stime          # Had to put it somewhere

# Fetching login data
login = open('data/login')
email = login.readline()[:-1]
passw = login.readline()[:-1]
login.close()

# Logging in
client = discord.Client()
client.login(email, passw)
email, passw = None, None

# Fetching master/admin data
masterID = '111100569845784576'
adminisTRAITORs = open('data/admins')
admins = adminisTRAITORs.read().splitlines()
adminisTRAITORs.close()

Master = None       # discord.Member to PM when necessary
last_update = os.stat('core.py')[8]     # time since last core.py update
running = True      # Status


@client.event
def on_message(message):
    """Handle messages from Discord."""
    global client, last_update, running
    S, ID, A = message.content, message.author.id, message.author.name

    # Update check
    edit_time = os.stat('core.py')[8]
    if edit_time > last_update or (S == 'RLD' and ID in admins):
        try:
            print(stime() + ' reloading core.py')
            last_update = edit_time
            reload(core)
            running = True
        except:
            client.send_message(Master, traceback.format_exc())

    if ID in admins and S == ';masterkill':
        print(stime() + ' masterkill by ' + A)
        running = False
        client.logout()
        client = None
        exit(-1)
    elif ID in admins and S == ';kill':
        print(stime() + ' killed by ' + A)
        running = False
    elif ID in admins and S == ';reload':
        print(stime() + ' reloaded by ' + A)
        running = True
        client.send_message(message.channel, '`Bot reloaded.`')
    elif running:
        core.process(client, message, admins)


@client.event
def on_ready():
    """Initialize bot."""
    global Master

    # Finding Master Zeroji
    for member in client.get_all_members():
        if member.id == masterID:
            Master = member

    # Taking good habits
    client.change_status(None, True)

    try:
        core.watcher.oniichan._args = (client,)
        core.watcher.oniichan.start()
    except:
        print('Error loading watcher.')

# FINISH HIM!
client.run()
