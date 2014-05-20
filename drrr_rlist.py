import urllib
import http.cookiejar
from bs4 import BeautifulSoup as BS
import itertools

top_url = 'http://drrr.us'
url = 'http://drrr.us/room'
raw_data = {'name': 'Insepector',
            'login': 'ENTER'}

encode = lambda d: urllib.parse.urlencode(d).encode('utf-8')
 
cookie = http.cookiejar.CookieJar()
cookie_hdr = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(cookie_hdr)

req = opener.open(top_url)
soup = BS(req.read())
tag = soup.find_all('input', attrs={'name': 'token'})[0]
raw_data['token'] = tag.get('value')

req = opener.open(top_url, encode(raw_data)) #Login

def refresh():
    req = opener.open(url) #get roomlist
    soup = BS(req.read())
    tag = soup.find_all('ul')[1:]

    L = [i.findAll('li') for i in tag]
    S = [j.contents for i in L for (index, j) in enumerate(i) if index < 3]

    I = itertools.cycle(['Room:', 'Host:', 'Load:'])

    for (i, j) in zip(I, S):
        print(i, j[0])

refresh()
while True:
    s = input('Refresh? Y/N ')
    if s.lower() == 'yes' or s.lower() == 'y':
        refresh()
    else:
        break
