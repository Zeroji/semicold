import discord
import time
from r import rot, closeTo, english
import urllib.request
import exifread
from array import array
import hashlib

primes = array('I')
primes.fromstring(open('data/primes', 'rb').read())

notActuallyOpenSource = open('data/secretCommands').read().splitlines()
metabot = ''

urls = '''http://pastebin.com/raw/Yf6dfuPT
https://raw.githubusercontent.com/7879/11.9/master/README.md
http://pastebin.com/raw/bw9V8Stw
http://104.131.44.161/fb53e74812173ad71c276f4bcc362505445be1948c817c37795171afc2eccf10.html
http://104.131.44.161/6469693230.html
http://104.131.44.161/'''.split('\n')

md = [''] * len(urls)
ttt = 0

afklist = {p[0]: p[1].split('¨¨') for p in [x.split('::') for x in open('data/afk').read().splitlines()]}

config = {'space': True, 'upper': False}
cfgtyp = {'space': 'B',  'upper': 'B'}
cfgdsc = {'space': 'Separate chunks for XXXasc conversion',
          'upper': 'Uppercase hexadecimal'}

arg_links = {
    'twitter':       'https://twitter.com/UGF0aWVuY2U',
    'reddit':        'https://www.reddit.com/user/1EC7',
    'bad horse':     'http://www.bad.horse/',
    'ip':            'http://104.131.44.161/',
    'map':           'https://www.google.com/maps/d/u/0/viewer?mid = zGwDMM8I2S0g.kyAvIUnIP0dA',
    '/r':            'https://www.reddit.com/r/7879arg/',
    'github':        'https://github.com/7879/identify',
    'book 2 runes':  'http://imgur.com/ngRtrQN',
    'book 2':        'https://docs.google.com/document/d/1SSiUN0D0uzbBtKy6c5qSFBEUa4WqrCitZVChzoaEqqI/edit?pref = 2&pli = 1',
    'books':         'https://docs.google.com/document/d/1zIYDEbwZVlgQ4mGlib717D6Ux7cDeevwDeCv5f3JtD0/edit?usp = sharing',
    'wiki':          'http://wiki.databutt.com/index.php?title = Main_Page',
    'bots':          'http://wiki.databutt.com/index.php?title = Bots'}


def factor(n, mx=len(primes)):
    l = []
#    while not n in primes and i<mx:
#        loop = True
#        while loop:
#            if n%primes[i]==0:
#                l.append(primes[i])
#                n// = primes[i]
#                loop = False
#            else:
#                i+ = 1
    for p in primes[:mx]:
        while n % p == 0:
            l.append(p)
            n //= p
            if n in primes:
                return l + [n]
    return ['Over capacity']
#    it = 0
#    while not (n in primes or n==1) and i<mx:
#        it+ = 1
#        while n%primes[i]==0:
#            it+ = 1
#            l.append(primes[i])
#            n// = primes[i]
#        i+ = 1
#    print('factored',n,'at',i,'with',it,'in',l)
#    if not n in primes and n>1: return ['Over capacity']
#    if n>1: l.append(n)
#    return l


def isRanked(mID, client):
    for m in client.get_all_members():
        if m.id == mID:
            for r in m.roles():
                if r not in '@everyoneBots':
                    return True
    return False


def writeAFK(ls):
    afkfile = open('data/afk', 'w')
    for i in ls.keys():
        if len(ls[i]) == 4:
            ls[i] += ['', '', 'Unknown']
        afkfile.write(i + '::' + '¨¨'.join(ls[i]) + '\n')
    afkfile.close()


def binint(s):
    r = 0
    for i in range(len(s)):
        if s[-i - 1] == '1':
            r += 2 ** i
    return r


def decint(s):
    return int(s)


def hexint(s):
    s = s.lower()
    h = '0123456789abcdef'
    r = 0
    for i in range(len(s)):
        r += 16 ** i * h.find(s[-i - 1])
    return r


def intbin(x, n=0):
    r = bin(x)[2:]
    if len(r) < n:
        r = '0' * (n - len(r)) + r
    return r


def inthex(x, n=0):
    r = hex(x)[2:]
    if config['upper']:
        r = r.upper()
    if len(r) < n:
        r = '0' * (n - len(r)) + r
    return r


def intdec(x, n=0):
    r = int(x)
    if len(r) < n:
        r = '0' * (n - len(r)) + r


def nsplit(s, n):
    return [s[i:i + n] for i in range(0, len(s), n)]


def sfill(s, n):
    return s + ' ' * (n - len(s))


def rotall(s, lang):
    S = [(rot(s, n), n) for n in range(26)]
    p = [(closeTo(s[0], lang), s[0], s[1]) for s in S]
    p.sort()
    r = '\n'.join(['ROT' + str(x[2]) + ': ' + x[1] for x in p[:3]])
    return r


def is_here():
    return True


def process(client, message):
    global md, ttt
    global metabot
    if time.time() > ttt:
        ttt = time.time() + 30
        for i in range(len(urls)):
            try:
                m = hashlib.md5(urllib.request.urlopen(urls[i], None, 0.5).read()).hexdigest()
                if md[i] == '':
                    md[i] = m
                if m != md[i]:
                    md[i] = m
                    for c in client.get_all_channels():
                        if c.name == 'development':
                            client.send_message(c, 'update on ' + urls[i])
            except:
                pass

    def sendT(text, m=True, t=False):
        client.send_message(message.channel, text, m, t)

    def send(text, m=True, t=False):
        sendT('`' * 3 + ('\n' if '\n' in text else '') + text + '`' * 3, m, t)

    def pm(text):
        client.send_message(message.author, '`' * 3 + ('\n' if '\n' in text else '') + text + '`' * 3)

    S = message.content
    A = message.author.name
    ID = message.author.id

    ranked, private, bot = False, True, False
    master = ID == '111100569845784576'
    Master = None
    for m in client.get_all_members():
        if m.id == '111100569845784576':
            Master = m
    if type(message.channel) == discord.channel.PrivateChannel:
        ranked = True
    else:
        private = False
        for r in message.author.roles:
            if r.name not in '@everyone Bots':
                ranked = True
            if r.name == 'Bots':
                bot = True

    if private and ID == client.user.id:
        bot = True

    if A == 'milton' and bot:
        S = S[2:]
        l = S.find('**')
        A = S[:l]
        S = S[l + 3:]

    T = S[S.find(' ') + 1:]
    C = (S[1:] if S.find(' ') < 0 else S[1:S.find(' ')]) if len(S) > 0 and S[0] == ';' else ''

    if S == ';;':
        send('''
;about                   'bout me.''' + ('''
;afk                     Setup your AFK message. Please use PMs.''' if ranked else '') + ('''
;bots                    Lists bots.''' if not private else '') + ('''
;config [<var> <value>]  Bot configuration''' if (ranked and not private) or master else '') + ('''
;info <member>           Gives info about member.''' if ranked and not private else '') + '''
;isprm <N>               Tells if <N> is a prime number.
;len <string>        [+] Prints the length of <string>.
;link <text>             Links useful things.
;links                   List of available links
;lmgtfy <text>           Googles <text> for you.
;meta <url>              Prints EXIF tags of image.
;prime <N>               Returns the <N>th prime.
;request <text>          Want to add a feature? It's here.''' + ('''
;say <text>              Prints <text> (debug purposes)
;tts <text>              Text-to-speech''' if ranked else '') + '''
;;;                      Lists all ciphering commands''')

    if S == ';;;':
        send('''
;rot <N> <text>          Uses ROT<N> on <text>.
;rot all <text>          Uses ROT1-25 on <text>.''' + (' Output via PM.' if not ranked else '') + '''
;rot <text>              Uses all ROT on text, gives top 3
;<in><out> <text>        Converts ASCii, BINary, DECimal, HEXadecimal
''')

    if C == 'urls':
        send('\n'.join(urls))

    if S == ';+':
        sendT('`Commands with a [+] before descriptions are contributed commands.`')

    #
    if '<@' + client.user.id + '>' in S:
        send("Hi, ;; here! Type ;; to get a list of my commands. PM also works.")

    # About
    if C == 'about':
        if private:
            send("Small bot in Python. Does stuff. Here. In private. Just the two of you.")
        else:
            send("Small bot in Python. Does stuff. Type ;source or ask Zeroji for more.")
    # """
    # if not away and not private and master and S=='<@'+client.user.id+'> please keep an eye on them ~':
    #     sendT('Will do!! \\*-\\*')
    #     away = True
    #     return
    # if away and not private and master and S=='<@'+client.user.id+'> I\'m back ~':
    #     sendT('Yay!! \\*-\\*')
    #     away = False
    #     return
    # if not private and '<@111100569845784576>' in S and away and not bot:
    #     sendT('<@'+ID+'> `Master Zeroji is busy. You can PM him for personal information or use ;request <text> if you would like him to improve my features.`')
    # """

    if not private and not bot:
        for k in afklist.keys():
            if '<@' + k + '>' in S and afklist[k][0] == '1':
                sendT('<@' + ID + '> ' + afklist[k][3])
                pmS, pmN = int(afklist[k][1]), int(afklist[k][2])
                if pmS == 0 or pmN < pmS:
                    pmC = None
                    for m in client.get_all_members():
                        if m.id == k:
                            pmC = m
                    if pmC:
                        client.send_message(pmC, '`User ' + A + ' tried to talk to you. Here is their message:`\n' + S.replace('<@' + k + '>', '@' + afklist[k][6]))
                        pmN += 1
                        afklist[k][2] = str(pmN)
                        writeAFK(afklist)

    # AFK feat
    if C == 'afk':
        if private:
            if ID not in afklist.keys():
                afklist[ID] = ['0', '0', '-1', 'unset', '', '', A]
            if len(afklist[ID]) == 4:
                afklist[ID] += ['', '', A]
            afkset = afklist[ID][2] != '-1' and afklist[ID][3] != 'unset'
            if S == ';afk':
                if afkset:
                    sendT('`Your AFK message: "' + afklist[ID][3] + '"`')
                    sendT('`Your notification setting: ' + ('never' if afklist[ID][1] == '-1' else ('always' if afklist[ID][1] == '0' else afklist[ID][1])) + '`')
                send('''Use the following commands to change your settings:
;afk msg <message>         Sets your AFK message (max 240 chars)
;afk pm <never|always|N>   Sends a PM when someone mentions you
If you choose <N>, it'll stop at N messages every afk cycle
After setup is complete you can use ;afk and ;back''')

            if T.startswith('pm'):
                T = T[3:]
                n = 3
                if T == 'always':
                    n = 0
                elif T == 'never':
                    n = -1
                else:
                    n = int(T)
                afklist[ID][1] = str(n)
                afklist[ID][2] = '0'
                if n < 0:
                    sendT("You won't be notified when someone mentions you.")
                elif n == 0:
                    sendT("You'll always be notified when someone mentions you.")
                else:
                    sendT("You'll be notified at most " + str(n) + " times when someone mentions you.")
            if T.startswith('msg'):
                T = T[4:]
                T = T.split(' ')
                for i in range(len(T)):
                    if T[i].startswith('http'):
                        breaklink = True
                        if breaklink:
                            T[i] = T[i].replace('://', ':// ')
                T = ' '.join(T)[:240]
                afklist[ID][3] = T
                sendT('Your AFK message has been set to:\n' + T)
            if T.startswith(notActuallyOpenSource[0]):
                afklist[ID][4] = T[6:]
            if T.startswith(notActuallyOpenSource[1]):
                afklist[ID][5] = T[7:]
            if afklist[ID][2] != '-1' and afklist[ID][3] != 'unset' and not afkset:
                send('AFK configuration complete!')
            afklist[ID][6] = A
            writeAFK(afklist)
        else:
            if ID in afklist.keys() and afklist[ID][3] != 'unset' and afklist[ID][2] != '-1':
                afklist[ID][0] = '1'
                writeAFK(afklist)
                if afklist[ID][4] != '':
                    sendT(afklist[ID][4])
            else:
                sendT('`Please enter your AFK settings via PM.`')
                pm('''Use the following commands to change your settings:
;afk msg <message>         Sets your AFK message
;afk pm <never|always|N>   Sends a PM when someone mentions you
If you choose <N>, it'll stop at N messages every afk cycle
After setup is complete you can use ;afk and ;back''')

    if S == ';back' and ID in afklist.keys():
        if afklist[ID][0] == '1':
            afklist[ID][0] = '0'
            afklist[ID][2] = '0'
            writeAFK(afklist)
            if afklist[ID][5] != '':
                sendT(afklist[ID][5])

    # Bot list
    if S == ';bots' and not private:
        print('Reporting in, listing the herd. (' + A + ')')
        r = "Hi, ;; here. I do stuff. I halp. Type ;; for moar. PM also works.\nI'm not alone here, you can type !bots to have more information.\nBots detected: "
        for m in message.channel.server.members:
            if m.status != 'offline' and 'Bots' in [x.name for x in m.roles]:
                r += m.name + ', '
        send(r[:-2])
    elif S[1:] == 'bots' and A != ';;':
        print('Reporting in. (' + A + ')')
        send("Hi, ;; here. I do stuff. I halp. Type ;; for moar. PM also works.")

    # Config
    if S == ';config' and ((ranked and not private) or master):
        send('\n'.join([cfgtyp[k] + ':' + sfill(k, 8) + sfill(str(config[k]), 8) + cfgdsc[k] for k in config.keys()]))
    elif C == 'config' and ((ranked and not private) or master):
        p = T.split()
        k, v = p[0], p[1]
        if k not in config.keys():
            send("Invalid variable name")
        elif len(p) != 2:
            send("Usage: ;config <var> <value>")
        else:
            r = None
            if cfgtyp[k] == 'B':
                r = v in 'TrueTRUEtrue1'
            if cfgtyp[k] == 'I':
                r = int(v)
            if cfgtyp[k] == 'S':
                r = v
            config[k] = r
            print(A + ' changed ' + k + ' to ' + v)

    # Cookie
    if S == ';cookie':
        sendT(':cookie:')

    # Factor
    if C == 'factor':
        n = int(T)
        l = factor(n) if ranked else factor(n, 10000)
        u = []
        for x in l:
            if x not in u:
                u.append(x)
        sendT(T + ' = ' + (' * '.join([str(x) + '^' + str(len([1 for n in l if n == x])) for x in u]) + ' ').replace('^1 ', ' ')[:-1])

    # Hugs
    if S == ';hug':
        if private:
            sendT('Oh, ' + A + '... you want to get into this? But.. you know we can\'t...')
        else:
            sendT("*hugs " + A + "*")

    # Info
    if C == 'info' and ranked and not private:
        print(A + ' asked about ' + T)
        for m in message.channel.server.members:
            if m.name == T or m.id == T:
                send('Member ' + m.name + ', roles: ' + ', '.join([x.name.replace('@everyone', 'Default') for x in m.roles]) + ' - ID ' + m.id)
    if C == 'info' and private:
        send('Member ' + A + ' - ID ' + ID)

    # Is Prime
    if C == 'isprm':
        n = int(T)
        if n <= primes[-1]:
            k = -1
            for i in range(len(primes)):
                if n == primes[i]:
                    k = i
            if k < 0:
                send('False')
            else:
                k += 1
                s = 'th'
                if k % 10 == 1 and k != 11:
                    s = 'st'
                if k % 10 == 2 and k != 12:
                    s = 'nd'
                if k % 10 == 3 and k != 13:
                    s = 'rd'
                send('True (' + str(k) + s + ')')
        elif ranked and n <= primes[-1] ** 2:
            for p in primes:
                if n % p == 0:
                    send('False')
                    return
            send('True')
        else:
            send('Over capacity')

    # Links
    if C == 'link':
        try:
            output = arg_links[T]
            sendT('Link to ' + T + ': ' + output)
            print('Linked to ' + T + ' (' + A + ')')
        except:
            print('Exception on ' + message.content)
    if C == 'links':
        send(', '.join(arg_links.keys()))

    # Meta
    if C == 'meat':
        sendT('<@' + ID + '> `It\'s okay to mistake metadata for meat. Enjoy your meal.`')
        C = 'meta'
    if S.startswith('$meta '):
        metabot = T
    if S == 'this feature will be implemented later on' and A == 'MetaBot' and metabot != '':
        C = 'meta'
        T = metabot
        metabot = '-'
    if C == 'meta':
        try:
            mtb = metabot == '-'
            if mtb:
                metabot = ''
            tags = exifread.process_file(open(urllib.request.urlretrieve(T)[0], 'rb'))
            if len(tags):
                if mtb:
                    sendT('<@' + ID + '> `You\'re so useless and pathetic. Let me do the work for real.`')
                send('\n'.join([sfill(tag[:30], 32) + str(tags[tag])[:40] for tag in tags.keys() if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote')]))
            else:
                if mtb:
                    sendT('<@' + ID + '> `Lol you stupid, there wasn\'t even any metadata in that one!`')
                else:
                    sendT('`No metadata found.`')
        except:
            sendT('`An error occured during command execution.`')

    # XMP metadata
    if C == 'meta_xmp':
        try:
            binfile = open(urllib.request.urlretrieve(T)[0], 'rb').read()
            strfile = ''.join([chr(x) for x in binfile])
            xmp_start = strfile.find('<x:xmpmeta')
            xmp_end = strfile.find('</x:xmpmeta>')
            if xmp_start < 0:
                sendT('`No XMP metadata found.`')
            elif xmp_end < 0:
                sendT('`No XMP meta end tag found!`')
            else:
                xmp_str = binfile[xmp_start:xmp_end + 12].decode('utf-8')
                if len(xmp_str) > 1200:
                    sendT('`XMP metadata exceeds 1200 bytes. Printing first 400 and last 400 bytes.`')
                    send(xmp_str[:400])
                    send(xmp_str[-400:])
                else:
                    send(xmp_str)
        except:
            sendT('`An error occured during command execution.`')

    # No spaces
    if C == 'nospace':
        sendT('`' + T.replace(' ', '') + '`')
    if C == 'unspace' and len([0 for c in T if c == ' ']) < len(T):
        while len([0 for c in T if c == ' ']) > 0.4 * len(T):
            r = ''
            l = T[0]
            for i in range(len(T)):
                c = T[i]
                if c != ' ' or l == ' ':
                    r += c
                l = c
            T = r
        send(r)

    # Ping
    if C == 'ping':
        sendT('pong!' if private else 'Nope.')

    # Prime
    if C == 'prime':
        n = int(T)
        if n <= len(primes) and n > 0:
            send(str(primes[n - 1]))
        else:
            send('Over capacity')
    # Requests
    if C == 'request':
        print(A + ' requested ' + T)
        if Master:
            client.send_message(Master, A + ' requested ' + T)

    # Say
    if C == 'say' and ranked and not bot:
        sendT(T)

    # Length of string
    if C == 'len':
        sendT(len(T))

    # Source
    if S == ';source':
        sendT('`;; source code` https://github.com/Zeroji/semicolon')

    # ROT
    if S.startswith(';rot'):
        text = message.content[4:]
        if text[0] == ' ':
            text = text[1:]
        if text.startswith('all'):
            print(A + ' used rotall')
            r = '\n'.join(['ROT' + str(i) + ': ' + rot(text[4:], i) for i in range(1, 26)])
            if ranked:
                send(r)
            else:
                sendT('`This command was disabled due to spam. The output was sent to you via PM.`')
                pm(r)
        elif text[0] in '0123456789':
            i = text.find(' ')
            n = int(text[:i])
            print(A + ' used rot ' + str(n))
            send(rot(text[i + 1:], n))
        else:
            print(A + ' used rot')
            send(rotall(text, english))

    # Let me google that for you
    if C == "lmgtfy":
        print(A + ' googled ' + T)
        sendT("http://lmgtfy.com/?q = " + '+'.join(T.split()))

    # Text-to-speech, for ranked members only
    if C == 'tts' and ranked:
        sendT(T, True, True)

    # Conversions
    D = C.lower()
    if len(D) == 6 and D[:3] in 'ascbindechex' and D[3:] in 'ascbindechex':
        print(A + ' used ' + D)
    if D == 'bindec':
        send(str(binint(T)))
    if D == 'binhex':
        send(inthex(binint(T)))
    if D == 'decbin':
        send(intbin(int(T)))
    if D == 'dechex':
        send(inthex(int(T)))
    if D == 'hexbin':
        send(intbin(hexint(T)))
    if D == 'hexdec':
        send(str(hexint(T)))
    if D == 'ascbin':
        send((' ' if config['space'] else '').join([intbin(ord(c), 8) for c in T]))
    if D == 'aschex':
        send((' ' if config['space'] else '').join([inthex(ord(c), 2) for c in T]))
    if D == 'ascdec':
        send(' '.join([str(ord(c)) for c in T]))
    if D == 'decasc':
        send(''.join([chr(int(x)) for x in T.split()]))
    if D == 'binasc':
        send(''.join([chr(binint(x)) for x in nsplit(T.replace(' ', ''), 8)]))
    if D == 'hexasc':
        send(''.join([chr(hexint(x)) for x in nsplit(T.replace(' ', ''), 2)]))

    # B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_ = '
#
#    if C=='base64':
#        alpha = False
#        for c in T:
#            if not c in B:
#                alpha = True
#
