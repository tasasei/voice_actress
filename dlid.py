#!/usr/bin/python3
import json, urllib.request
import requests
from tqdm import tqdm

BaseUrl = 'https://ja.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:%E6%97%A5%E6%9C%AC%E3%81%AE%E5%A5%B3%E6%80%A7%E5%A3%B0%E5%84%AA&format=json&cmlimit=500'
pageid_list = []
cmcontinue = ''

## Category:日本の女性声優
while True:
    url = BaseUrl + cmcontinue
    res = urllib.request.urlopen(url)
    d_bytes = res.read()
    d_str = d_bytes.decode()
    d = json.loads(d_str)
    
    for i in d['query']['categorymembers']:
        pageid_list += [i['pageid']]

    print(d['query']['categorymembers'][0])
    if 'continue' in d:
        cmcontinue_raw = d['continue']['cmcontinue']
        cmcontinue = '&cmcontinue=' + cmcontinue_raw
    else:
        break

pageid_set = set(pageid_list)

# BaseUrl = 'https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&pageids={}&rvprop=content&redirects'
# pageid_list = []
# for i in tqdm(pageid_set):
#     url = BaseUrl.format(i)
#     q = requests.get(url)
#     page = list(q.json()['query']['pages'].keys())[0]
#     pageid_list += [page]

f = open('pageid.dat','w')
for i in pageid_set:
    f.write(str(i)+'\n')
f.close()
