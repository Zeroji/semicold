import discord
import time
from r import rot, closeTo, english
from random import randint

away   = False
config = { 'space':True, 'upper':False }
cfgtyp = { 'space':'B' , 'upper':'B' }
cfgdsc = { 'space':'Separate chunks for XXXasc conversion',
           'upper':'Uppercase hexadecimal'}

arg_links = {
    'twitter':'https://twitter.com/UGF0aWVuY2U',
    'reddit' :'https://www.reddit.com/user/1EC7',
    'bad horse':'http://www.bad.horse/',
    'ip'     :'http://104.131.44.161/',
    'map'    :'https://www.google.com/maps/d/u/0/viewer?mid=zGwDMM8I2S0g.kyAvIUnIP0dA',
    '/r'     :'https://www.reddit.com/r/7879arg/',
    'github' :'https://github.com/7879/identify',
    'book 2 runes':'http://imgur.com/ngRtrQN',
    'book 2' :'https://docs.google.com/document/d/1SSiUN0D0uzbBtKy6c5qSFBEUa4WqrCitZVChzoaEqqI/edit?pref=2&pli=1',
    'books'  :'https://docs.google.com/document/d/1zIYDEbwZVlgQ4mGlib717D6Ux7cDeevwDeCv5f3JtD0/edit?usp=sharing',
    'wiki'   :'http://wiki.databutt.com/index.php?title=Main_Page',
    'bots'   :'http://wiki.databutt.com/index.php?title=Bots',
    }

def binint(s):
    r=0
    for i in range(len(s)):
        if s[-i-1]=='1':
            r+=2**i
    return r

def decint(s): return int(s)

def hexint(s):
    s=s.lower()
    h='0123456789abcdef'
    r=0
    for i in range(len(s)):
        r+=16**i*h.find(s[-i-1])
    return r

def intbin(x, n=0):
    r=bin(x)[2:]
    if len(r)<n:
        r='0'*(n-len(r))+r
    return r

def inthex(x, n=0):
    r=hex(x)[2:]
    if config['upper']: r=r.upper()
    if len(r)<n:
        r='0'*(n-len(r))+r
    return r

def intdec(x, n=0):
    r=int(x)
    if len(r)<n:
        r='0'*(n-len(r))+r

def nsplit(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

def sfill(s, n):
    return s+' '*(n-len(s))

def rotall(s, lang):
    S=[(rot(s, n), n) for n in range(26)]
    p=[(closeTo(s[0], lang), s[0], s[1]) for s in S]
    p.sort()
    r='\n'.join(['ROT'+str(x[2])+': '+x[1] for x in p[:3]])
    return r

def is_here(): return True
def process(client, message):
    global away
    def sendT(text, m=True, t=False):
        client.send_message(message.channel, text, m, t)
    def send(text, m=True, t=False):
        sendT('`'*3+('\n' if '\n' in text else '')+text+'`'*3, m, t)
    def pm(text):
        client.send_message(message.author, '`'*3+('\n' if '\n' in text else '')+text+'`'*3)
        
    S=message.content
    A=message.author.name
    T=S[S.find(' ')+1:]
    C=(S[1:] if S.find(' ')<0 else S[1:S.find(' ')]) if len(S)>0 and S[0]==';' else ''
    
    ranked, private, bot=False, True, False
    master=message.author.id=='111100569845784576'
    if type(message.channel)==discord.channel.PrivateChannel: ranked=True
    else:
        private=False
        for r in message.author.roles:
            if r.name not in '@everyone Bots':
                ranked=True
            if r.name=='Bots':
                bot=True
    
    if not away and not private and master and S=='<@'+client.user.id+'> please keep an eye on them ~':
        sendT('Will do!! \\*-\\*')
        away=True
        return
    if away and not private and master and S=='<@'+client.user.id+'> I\'m back ~':
        sendT('Yay!! \\*-\\*')
        away=False
        return
    if not private and '<@111100569845784576>' in S and away and not bot:
        sendT('<@'+message.author.id+'> `Master Zeroji is busy. You can PM him for personal information or use ;request <text> if you would like him to improve my features.`')
    
    if S==';;':
        send('''
;about                   'bout me.'''+('''
;bots                    Lists bots.''' if not private else '')+('''
;config [<var> <value>]  Bot configuration''' if (ranked and not private) or master else '')+('''
;info <member>           Gives info about member.''' if ranked and not private else '')+'''
;link <text>             Links useful things.
;links                   List of available links
;lmgtfy <text>           Googles <text> for you.
;request <text>          Want to add a feature? It's here.'''+('''
;say <text>              Prints <text> (debug purposes)
;tts <text>              Text-to-speech''' if ranked else '')+'''
;;;                      Lists all ciphering commands''')

    if S==';;;':
        send('''
;rot <N> <text>          Uses ROT<N> on <text>.
;rot all <text>          Uses ROT1-25 on <text>.'''+(' Output via PM.' if not ranked else '')+'''
;rot <text>              Uses all ROT on text, gives top 3
;<in><out> <text>        Converts ASCii, BINary, DECimal, HEXadecimal
''')
    
    #
    if '<@'+client.user.id+'>' in S:
        send("Hi, ;; here! Type ;; to get a list of my commands. PM also works.")
    
    # About
    if C=='about':
        if private:
            send("Small bot in Python. Does stuff. Here. In private. Just the two of you.")
        else:
            send("Small bot in Python. Does stuff. Type ;source or ask Zeroji for more.")
    
    # Bot list
    if S==';bots' and not private:
        print('Reporting in, listing the herd. ('+A+')')
        r="Hi, ;; here. I do stuff. I halp. Type ;; for moar. PM also works.\nI'm not alone here, you can type !bots to have more information.\nBots detected: "
        for m in message.channel.server.members:
            if 'Bots' in [x.name for x in m.roles]:
                r+=m.name+', '
        send(r[:-2])
    elif S[1:]=='bots' and A!=';;':
        print('Reporting in. ('+A+')')
        send("Hi, ;; here. I do stuff. I halp. Type ;; for moar. PM also works.")

    # Config
    if S==';config' and ((ranked and not private) or master):
        send('\n'.join([cfgtyp[k]+':'+sfill(k,8)+sfill(str(config[k]), 8)+cfgdsc[k] for k in config.keys()]))
    elif C=='config' and ((ranked and not private) or master):
        p=T.split()
        k,v=p[0], p[1]
        if k not in config.keys():
            send("Invalid variable name")
        elif len(p)!=2:
            send("Usage: ;config <var> <value>")
        else:
            r=None
            if cfgtyp[k]=='B': r=v in 'TrueTRUEtrue1'
            if cfgtyp[k]=='I': r=int(v)
            if cfgtyp[k]=='S': r=s
            config[k]=r
            print(A+' changed '+k+' to '+v)
            
    
    # Cookie
    if S==';cookie': sendT(':cookie:')
    
    # Hugs
    if S==';hug':
        if private: sendT('Oh, '+A+'... you want to get into this? But.. you know we can\'t...')
        else: sendT("*hugs "+A+"*")

    # Info
    if C=='info' and ranked and not private:
        print(A+' asked about '+T)
        for m in message.channel.server.members:
            if m.name==T:
                send('Member '+T+', roles: '+', '.join([x.name.replace('@everyone', 'Default') for x in m.roles])+' - ID '+m.id)
    if C=='info' and private:
        send('Member '+A+' - ID '+message.author.id)
    
    # Links
    if C=='link':
        try:
            output = arg_links[T]
            sendT('Link to '+T+': '+output)
            print('Linked to '+T+' ('+A+')')
        except:
            print('Exception on '+message.content)
    if C=='links':
        send(', '.join(arg_links.keys()))
    
    # Ping
    if C=='ping': sendT('Nope.')
    
    # Requests
    if C=='request': print(A+' requested '+T)

    # Say
    if C=='say' and ranked: sendT(T)

    # Source
    if S==';source' and ranked: sendT('`;; source code` https://github.com/Zeroji/semicolon')
    
    # ROT
    if S.startswith(';rot'):
        text=message.content[4:]
        if text[0]==' ': text=text[1:]
        if text.startswith('all'):
            print(A+' used rotall')
            r='\n'.join(['ROT'+str(i)+': '+rot(text[4:], i) for i in range(1,26)])
            if ranked:
                send(r)
            else:
                sendT('`This command was disabled due to spam. The output was sent to you via PM.`')
                pm(r)
        elif text[0] in '0123456789':
            i=text.find(' ')
            n=int(text[:i])
            print(A+' used rot '+str(n))
            send(rot(text[i+1:], n))
        else:
            print(A+' used rot')
            send(rotall(text, english))

    # Let me google that for you
    if C=="lmgtfy":
        print(A+' googled '+T)
        sendT("http://lmgtfy.com/?q="+'+'.join(T.split()))

    # Text-to-speech, for ranked members only
    if C=='tts' and ranked:
        sendT(T, True, True)

    # Conversions
    D=C.lower()
    if len(D)==6 and D[:3] in 'ascbindechex' and D[3:] in 'ascbindechex': print(A+' used '+D)
    if D=='bindec': send(str(binint(T)))
    if D=='binhex': send(inthex(binint(T)))
    if D=='decbin': send(intbin(int(T)))
    if D=='dechex': send(inthex(int(T)))
    if D=='hexbin': send(intbin(hexint(T)))
    if D=='hexdec': send(str(hexint(T)))
    if D=='ascbin': send((' ' if config['space'] else '').join([intbin(ord(c), 8) for c in T]))
    if D=='aschex': send((' ' if config['space'] else '').join([inthex(ord(c), 2) for c in T]))
    if D=='ascdec': send((' ' if config['space'] else '').join([str(ord(c)) for c in T]))
    if D=='decasc': send(''.join([chr(int(x)) for x in T.split()]))
    if D=='binasc': send(''.join([chr(binint(x)) for x in nsplit(T.replace(' ', ''), 8)]))
    if D=='hexasc': send(''.join([chr(hexint(x)) for x in nsplit(T.replace(' ', ''), 2)]))
