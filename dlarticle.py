#!/usr/bin/python3
import json, urllib.request, re, urllib, os
import requests
from tqdm import tqdm

f = open('pageid.dat','r')
pageid_str_list = [str(int(i)) for i in f.readlines()]
f.close()

BaseUrl = 'https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&pageids={}&rvprop=content&redirects'
# https://ja.wikipedia.org/w/api.php?action=parse&pageid=2774720&format=json
UsedPage_list = []

os.mkdir('pages/')

for pageid_str in tqdm(pageid_str_list):
    # pageid_str = str(2774720) # 雨宮天
    # pageid_str = str(2834458) # 斎藤千和
    # pageid_str = str(2826852) # 林原めぐみ
    # pageid_str = str(1053224) # 民安ともえ
    url = BaseUrl.format(pageid_str)
    
    try:
        q = requests.get(url)
    except:
        print('Download Failed:' + pageid_str)
        continue
    
    page = list(q.json()['query']['pages'].keys())[0]

    if page in UsedPage_list:
        continue
    UsedPage_list += [page]

    honbun_str = q.json()['query']['pages'][page]['revisions'][0]['*']

    f = open('pages/'+str(page)+'.txt','w')
    f.write(honbun_str)
    f.close()
