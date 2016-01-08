import discord
import time
from r import rot, closeTo, english
from random import randint

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

def rotall(s, lang):
    S=[(rot(s, n), n) for n in range(26)]
    p=[(closeTo(s[0], lang), s[0], s[1]) for s in S]
    p.sort()
    r='\n'.join(['ROT'+str(x[2])+': '+x[1] for x in p[:3]])
    return r

def is_here(): return True
def process(client, message):
    def sendT(text, m=True, t=False):
        client.send_message(message.channel, text, m, t)
    def send(text, m=True, t=False):
        sendT('`'*3+('\n' if '\n' in text else '')+text+'`'*3, m, t)
    ranked=False
    for r in message.author.roles:
        if r.name not in '@everyone Bots':
            ranked=True
    S=message.content
    A=message.author.name
    T=S[S.find(' ')+1:]
    C=(S[1:] if S.find(' ')<0 else S[1:S.find(' ')]) if len(S)>0 and S[0]==';' else ''
    if S==';;':
        send('''
;about                   'bout me.
;bots                    Lists bots.'''+('''
;info <member>           Gives info about member.''' if ranked else '')+'''
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
;rot all <text>          Uses ROT1-25 on <text>.
;rot <text>              Uses all ROT on text, gives top 3
''')

    # About
    if C=='about':
        send("Small bot written in Python. Does stuff. Ask Zeroji for more.")
    
    # Bot list
    if S==';bots':
        print('Reporting in, listing the herd. ('+A+')')
        r="Hi, ;; here. I do stuff. I halp. Type ;; for moar.\nI'm not alone here, you can type !bots to have more information.\nBots detected: "
        for m in message.channel.server.members:
            if 'Bots' in [x.name for x in m.roles]:
                r+=m.name+', '
        send(r[:-2])
    elif S[1:]=='bots' and A!=';;':
        print('Reporting in. ('+A+')')
        send("Hi, ;; here. I do stuff. I halp. Type ;; for moar.")

    # Cookie
    if S==';cookie': sendT(':cookie:')
    
    # Hugs
    if S==';hug': sendT("*hugs "+A+"*")

    # Info
    if C=='info' and ranked:
        print(A+' asked about '+T)
        for m in message.channel.server.members:
            if m.name==T:
                send('Member '+T+', roles: '+', '.join([x.name.replace('@everyone', 'Default') for x in m.roles])+' - ID '+m.id)
    
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
            send('\n'.join(['ROT'+str(i)+': '+rot(text[4:], i) for i in range(1,26)]))
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
