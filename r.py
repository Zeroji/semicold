#english = [['E', 12.02], ['T', 9.10], ['A', 8.12], ['O', 7.68], ['I', 7.31], ['N', 6.95], ['S', 6.28], ['R', 6.02], ['H', 5.92], ['D', 4.32], ['L', 3.98], ['U', 2.88], ['C', 2.71], ['M', 2.61], ['F', 2.30], ['Y', 2.11], ['W', 2.09], ['G', 2.03], ['P', 1.82], ['B', 1.49], ['V', 1.11], ['K', 0.69], ['X', 0.17], ['Q', 0.11], ['J', 0.10], ['Z', 0.07]]
english = 'ETAOINSRHDLUCMFYWGPBVKXQJZ'

def closeTo(s, lang):
    s=s.upper()
    l=[[len([c for c in s if c==d]), d] for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    l.sort(reverse=True)
    close=0
    for i in range(10):
        close+=abs(lang.find(l[i][1])-i)*(26-i)
    return close

def rot(s, n):
    r=''
    for c in s:
        x=ord(c)
        if x>64 and x<=90:
            x=(x-65+n)%26+65
        if x>96 and x<123:
            x=(x-97+n)%26+97
        r+=chr(x)
    return r

def rotall(s, lang):
    S=[(rot(s, n), n) for n in range(26)]
    p=[(closeTo(s[0], lang), s[0], s[1]) for s in S]
    p.sort()
    print(p)
