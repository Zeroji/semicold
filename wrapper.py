"""Wrapper for ;; bot."""
import discord                  # Discord API wrapper
import db                       # ;; main source code
import os                       # Checking for source updates
from imp import reload          # Reloading source code
import traceback                # Handling errors

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
masters = open('data/admins')
admins = masters.read().splitlines()
masters.close()

Master = None       # discord.Member to PM when necessary
last_update = 0     # time since last db.py update
running = True      # Status


@client.event
def on_message(message):
    """Handle messages from Discord."""
    global client, last_update, running
    S, ID, A = message.content, message.author.id, message.author.name

    # Update check
    edit_time = os.stat('db.py')[8]
    if edit_time > last_update or (S == 'RLD' and ID == masterID):
        try:
            print(db.stime() + ' reloading db.py')
            last_update = edit_time
            reload(db)
            running = True
        except:
            client.send_message(Master, traceback.format_exc())

    if ID in admins and S == ';masterkill':
        print(db.stime() + ' masterkill by ' + A)
        running = False
        client.logout()
        client = None
        exit(-1)
    elif ID in admins and S == ';kill':
        print(db.stime() + ' killed by ' + A)
        running = False
    elif ID in admins and S == ';reload':
        print(db.stime() + ' reloaded by ' + A)
        running = True
        client.send_message(message.channel, '`Bot reloaded.`')
    elif running:
        db.process(client, message)


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

    # Sending initialization message
    for channel in client.get_all_channels():
        if channel.name == 'development':
            client.send_message(channel, '`Wrapper initialized.`')

# FINISH HIM!
client.run()
