"""Chat module for ;; bot."""
import random                   # 8ball
import subprocess               # Used by ping
import discord
import requests
from cmds import command        # Command dictionary
from message import Message

LENNY = '( ͡° ͜ʖ ͡°)'              # Needed for reasons


@command('anime', __name__, help='Find information about an anime.', usage='<anime>')
def anime(_):
    """Get information from MyAnimeList.net."""
    try:
        data = requests.get("http://myanimelist.net/anime.php?q=" + '+'.join(_['T'].split()) +
                            "&type=0&score=0&status=0&p=0&r=0&sm=0&sd=0&sy=0&em=0&ed=0"
                            "&ey=0&c[]=a&c[]=b&c[]=c&c[]=d&c[]=f&c[]=g&gx=1&genre[]=12").content
    except requests.exceptions.HTTPError:
        pass
    else:
        if b'<title>Search Anime' in data:
            link_start = data.find(b'<a href="/anime/')
            link_end = data.find(b'"', link_start+12)
            link = 'http://myanimelist.net' + data[link_start + 9:link_end].decode('utf-8')
            title_start = data.find(b'<strong>', link_end)
            title_end = data.find(b'</strong>', title_start)
            title = data[title_start + 8:title_end].decode('utf-8')
            desc_start = data.find(b'<div class="spaceit">', title_end)
            desc_end = data.find(b'</div>', desc_start)
            desc = data[desc_start + 21:desc_end].decode('utf-8')
            if '<a href' in desc:
                desc = desc[:desc.find('<a href')]
            desc = desc.strip()
            stats_start = data.find(b'align="center">', desc_end)
            stats_end = data.find(b'</td> </tr>', stats_start)
            stats = data[stats_start + 15:stats_end].decode('utf-8')
            stats = stats.split('</td><td class="borderClass bgColor1" align="center">')
            stats[3] = ('20' if stats[3][-2:] < '20' else '19') + stats[3][-2:]
        else:
            title_start = data.find(b'<span itemprop="name">')
            title_end = data.find(b'</span>', title_start)
            title = data[title_start + 22:title_end].decode('utf-8')
            link_start = data.find(b'<a href="', title_end)
            link_end = data.find(b'/pics">', link_start)
            link = data[link_start + 9:link_end].decode('utf-8')
            stats = [''] * 6
            type_start = data.find(b'">', data.find(b'Type:</span>'))
            type_end = data.find(b'</a>', type_start)
            stats[0] = data[type_start + 2:type_end].decode('utf-8')
            eps_start = data.find(b'Episodes:</span>')
            eps_end = data.find(b'</div>', eps_start)
            stats[1] = data[eps_start + 16:eps_end].decode('utf-8').strip()
            score_start = data.find(b'"ratingValue">')
            score_end = data.find(b'</span>', score_start)
            stats[2] = data[score_start + 14:score_end].decode('utf-8')
            date_start = data.find(b'Aired:</span>')
            date_end = data.find(b'</div>', date_start)
            stats[3] = data[date_start + 13:date_end].decode('utf-8').strip()
            if 'Not available' in stats[3]:
                stats[3] = 'not yet aired'
            elif ', ' in stats[3]:
                comma = stats[3].find(', ')
                stats[3] = stats[3][comma+2:comma+6]
            members_start = data.find(b'Members:</span>')
            members_end = data.find(b'</div>', members_start)
            stats[4] = data[members_start + 15:members_end].decode('utf-8').strip()
            rating_start = data.find(b'Rating:</span>')
            rating_end = data.find(b'</div>', rating_start)
            stats[5] = data[rating_start + 14:rating_end].decode('utf-8').strip()
            desc_start = data.find(b'"description">')
            desc = data[desc_start + 14:desc_start + 256].decode('utf-8')
            desc = ' '.join(desc.replace('<br />', '')[:200].split()[:-1]) + '...'

        ratings = [('G', 'All Ages'), ('PG', 'Children'), ('PG-13', 'Teens 13 or older'),
                   ('R', '17+ - (violence and profanity)'), ('R+', 'Mild Nudity'), ('Rx', 'Hentai')]
        rating = stats[5]
        for short, full in ratings:
            if stats[5].startswith(short):
                rating = short + ' - ' + full
        stats[5] = rating
        # Stats: Type, Eps, Score, Date, Members, Rating
        message = link + '   **' + title + '** (' + stats[3] + ')\nType: ' + stats[0]
        if stats[0] != 'Movie':
            message += ', ' + stats[1] + ' episodes'
        message += '. Scored ' + stats[2] + '/10 (' + stats[4] + ' members). Rating: ' + stats[5]
        message += '.\n' + desc
        return Message(message, Message.PLAIN)


@command('channel', __name__, help='Give current channel information.')
def channel_info(_):
    """Return channel name/ID."""
    return Message('Channel #' +
                   (_['A'] if _['private'] else _['message'].channel.name) +
                   ' - ID ' + _['cID'])


@command('del', __name__, minRank=2, help='Delete last N messages from ;;',
         usage='<N>')
def delete(_):
    """Delete the last N messages from the bot."""
    def logs(number, last=None):
        """Seriously this doesn't need a docstring."""
        return _['client'].logs_from(_['message'].channel, number, before=last)
    last = list(logs(1))[0]
    try:
        todo = int(_['T'])
    except ValueError:
        pass
    else:
        while todo:
            for i, message in enumerate(list(logs(100, last))):
                if i == 99:
                    last = message
                if message.author.id == _['client'].user.id:
                    print('Deleting', message.content)
                    _['client'].delete_message(message)
                    todo -= 1
                    if not todo:
                        return


M8B = ['It is certain', 'It is decidedly so', 'Without a doubt',
       'Yes, definitely', 'You may rely on it', 'As I see it, yes',
       'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
       'Reply hazy try again', 'Ask again later', 'Better not tell you now',
       'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it',
       'My reply is no', 'My sources say no', 'Outlook not so good',
       'Very doubtful']


@command('8ball', __name__, help=';8ball should I help them?', hidden=True)
def mball(_):
    """."""
    i = random.randint(0, len(M8B)-1)
    typ = '[yup]' if i < 10 else '[...]' if i < 15 else '[nah]'
    return Message(typ + ' ' + M8B[i])


@command('channels', __name__, minRank=1, help='List all channel information.')
def list_channels(_):
    """List channels."""
    channels = []
    maxlength = 0
    for channel in _['message'].channel.server.channels:
        if channel.type == discord.ChannelType.text:
            channels.append((channel.position, channel.name, channel.id))
            maxlength = max(maxlength, len(channel.name))
    channels.sort()
    return Message('\n'.join(['Channel #' + (c[1] + ' ' * maxlength)[:maxlength] +
                              ' - ID ' + c[2] for c in channels]), Message.BLOCK)


command('cookie', __name__, help='Give this man a cookie.', hidden=True)(
    lambda _: Message(':cookie:', Message.PLAIN))


command('hug', __name__, help='For the lonely.', hidden=True, private=False)(
    lambda _: Message('*hugs ' + _['A'] + '*', Message.PLAIN))


command('hug', __name__, help=LENNY, hidden=True, privateOnly=True)(
    lambda _: Message('Oh, ' + _['A'] + '... you want to get into this?' +
                      'But.. you know we can\'t...', Message.PLAIN))


@command('info', __name__, privateOnly=True, help='Get your ID')
def info_pm(_):
    """Give info about self."""
    return Message('Member ' + _['A'] + ' - ID: ' + _['message'].author.id)


@command('info', __name__, minRank=1, help='Get member information',
         usage='<name|ID>, ...', private=False)
def info(_):
    """Give info about members."""
    output = []
    targets = _['T'].split(',')
    for target in targets:
        if target[0] == ' ':
            target = target[1:]
        if target[-1] == ' ':
            target = target[:-1]
        for message in _['message'].channel.server.members:
            if target in (message.name, message.id):
                roles = ', '.join([r.name for r in message.roles])
                roles = roles.replace('@everyone', 'Default')
                roles = roles.replace('Trusted', 'Purple')
                output.append(Message('Member ' + message.name + ', roles: ' +
                                      roles + ' - ID: ' + message.id))
    return output


command('lmgtfy', __name__, help='Googles that for you.', usage='<text>')(
    lambda _: Message('http://lmgtfy.com/?q=' + '+'.join(_['P'][1:]), Message.PLAIN))


command('ok', __name__, help='OK.', hidden=True)(
    lambda _: Message('http://i.imgur.com/XtC4At2.jpg', Message.PLAIN))


@command('oneliner', __name__, help='Steals a neat oneliner from StuffBot.',
         usage='[<filter>]', hidden=True)
def oneliner(_):
    """You wouldn't steal Stuff."""
    try:
        with open('/home/tomg777/StuffBot/oneliner.txt', 'r') as oneliner_file:
            lines = oneliner_file.read().splitlines()
        if _['T']:
            lines = [l for l in lines if _['T'] in l]
        if lines:
            return Message(random.choice(lines))
    except FileNotFoundError:
        pass


@command('ping', __name__, help='Give ping statistics for a given URL',
         usage='<URL>', minRank=1)
def ping(_):
    """Print ping statistics for an URL."""
    process = subprocess.Popen(['ping', '-q', '-c', '4', '-i', '0.2', _['T']],
                               stdout=subprocess.PIPE)
    process.wait()
    lines = [l.decode('ascii') for l in process.stdout]
    if len(lines) == 5:
        return Message(''.join(lines[-2:]), Message.BLOCK)


command('say', __name__, minRank=1, help='Repeat', usage='<text>')(
    lambda _: Message(_['T'], Message.PLAIN))


@command('sayto', __name__, minRank=2, help='Repeat to channel', usage='<#channel> <text>')
def sayto(_):
    """Send a message to a specific channel."""
    chan, message = _['P'][1], _['L'][2]
    if chan.startswith('<#'):
        chan = chan[2:-1]
    output = []
    for channel in _['client'].get_all_channels():
        if channel.id == chan:
            output.append(Message(message, channel=channel, style=Message.PLAIN))
    return output


command('tts', __name__, minRank=1, help='Text-to-speech', usage='<text>')(
    lambda _: Message(_['T'], Message.PLAIN, tts=True))


command('xkcd', __name__, help='xkcd', usage='<N>', hidden=True)(
    lambda _: Message('http://xkcd.com/' + _['T'] + '/', Message.PLAIN))
