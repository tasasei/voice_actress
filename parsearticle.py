#!/usr/bin/python3
import json, urllib.request, re, urllib
import requests

def ParseBirth(key_str,x_str):
    b_year = re.search(('\|\s*' + key_str + '\s*=\s*[0-9]*'),x_str)
    if b_year == None and len(x_str) < 10:
        import pdb; pdb.set_trace()
        return ''
    if b_year == None:
        return ''
    return re.sub('[^0-9]','',b_year.group(0))

def ParseName(honbun_str):
    for i in honbun_str.split('\n'):
        name_m = re.search(' *\| *名前 *= *([^ ]+[^\|]*)',i)
        if name_m:
            # if '|' in name_m.group(1):
            #     import pdb; pdb.set_trace()
            return name_m.group(1)
        geimei_m = re.search(' *\| *芸名 *= *([^ ]+[^\|]*)',i)
        if geimei_m:
            return geimei_m.group(1)

def ParsePerf(honbun_str, ofile=None, ap_list=None):
    # tag_list = ['テレビアニメ','劇場アニメ','ゲーム','OVA','Webアニメ','吹き替え'] # 'ドラマCD'
    tag_list = ['テレビアニメ','ゲーム']
    lines = honbun_str.split('\n')
    perf_dic = {}
    tag = None
    year = None
    # import pdb; pdb.set_trace()
    for i in lines:
        m = re.search("^ *==* *([^ =]*) *==*", i)
        if m:
            tag = m.group(1)
            if tag in tag_list:
                perf_dic[tag] = {}
            continue
        # if '豊田 萌絵' in ap_list and 'ゲーム' in str(tag):
        #     import pdb; pdb.set_trace()

        if not tag in tag_list:
            continue
        if re.match('^}',i):
            tag = None
            year = None
            continue
        
        year_m = re.search("^ *\| *([0-9]*)年 *\| *$", i)
        if year_m:
            year = year_m.group(1)
            if year is not None:
                perf_dic[tag][year] = 0
            continue
        # film_m = re.search("^ *\* *\[\[([^]]*)\]\]", i)
        film_m = re.search("^ *\* .*", i)
        if film_m:
            # film = film_m.group(1) # 出演作品
            if year is None:
                continue
            perf_dic[tag][year] += 1
            # print(tag + ':' + year + ':' + film)
            continue

    if ofile is not None:
        for t in perf_dic.keys():
            for y in perf_dic[t]:
                if ap_list is None:
                    w_str = y + ',' + t + ',' + str(perf_dic[t][y]) + '\n'
                elif None in ap_list:
                    continue
                else:
                    w_str =','.join(ap_list) + ',' + y + ',' + t + ',' + str(perf_dic[t][y]) + '\n'
                of.write(w_str)
    return perf_dic

f = open('valist.txt','r')
pageid_str_list = [str(int(i)) for i in f.readlines()]
f.close()

# BaseUrl = 'https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&pageids={}&rvprop=content&redirects'
# https://ja.wikipedia.org/w/api.php?action=parse&pageid=2774720&format=json
UsedPage_list = []
of = open('perf.csv','w')
of.write('name,id,birthday,year,category,num\n')
for pageid_str in pageid_str_list:
    # pageid_str = str(2774720) # 雨宮天
    # pageid_str = str(2834458) # 斎藤千和
    # pageid_str = str(2826852) # 林原めぐみ
    # pageid_str = str(1053224) # 民安ともえ

    f = open('pages/'+pageid_str+'.txt')
    honbun_str = f.read()
    f.close()

    name = ParseName(honbun_str)

    b_year = ParseBirth('生年',honbun_str)
    b_mon  = ParseBirth('生月',honbun_str)
    b_day  = ParseBirth('生日',honbun_str)
    birthday_str = b_year + '-' + b_mon + '-' + b_day
    # print(name)
    # print(jobs)

    #perf = ParsePerf(honbun_str,of, id_str=pageid_str, name=name, birthday_str)
    ap_list = [name,pageid_str,birthday_str]
    perf = ParsePerf(honbun_str,of, ap_list)

of.close()
