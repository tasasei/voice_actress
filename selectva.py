#!/usr/bin/python3
import json, urllib.request, re, urllib, glob, os
import requests

def ParseBirth(key_str,x_str):
    b_year = re.search(('\|\s*' + key_str + '\s*=\s*[0-9]*'),x_str)
    if b_year == None and len(x_str) < 10:
        import pdb; pdb.set_trace()
        return ''
    if b_year == None:
        return ''
    return re.sub('[^0-9]','',b_year.group(0))

def ParseFormat(honbun_str):
    lines = honbun_str.split('\n')
    for i in lines:
        m = re.search('\{\{([^}\|　< ]*)[^}]*$',i)
        if m and m.group(1) in ['告知','複数の問題']:
            continue
        if m:
            # print(m.group(1))
            return m.group(1)
        
def ParseJob(honbun_str):
    job_m = re.search(r' *\| *職業 *=.*',honbun_str)
    if job_m:
        return re.findall('\[\[([^[]*)\]\]',job_m.group())
    genre_m = re.search(r' *\| *ジャンル *=.*',honbun_str)
    if genre_m:
        return re.findall('\[\[([^[]*)\]\]',genre_m.group())

def ParseName(honbun_str):
    name_m = re.search(' *\| *名前 *= *(.*)',honbun_str)
    # import pdb; pdb.set_trace()
    if name_m:
        return name_m.group(1)
    geimei_m = re.search(' *\| *芸名 *= *(.*)',honbun_str)
    if geimei_m:
        return geimei_m.group(1)

def ParsePerf(honbun_str, ofile=None, ap_list=None):
    # tag_list = ['テレビアニメ','劇場アニメ','ゲーム','OVA','Webアニメ','吹き替え'] # 'ドラマCD'
    tag_list = ['テレビアニメ']
    lines = honbun_str.split('\n')
    perf_dic = {}
    tag = None
    year = None
    # import pdb; pdb.set_trace()
    for i in lines:
        m = re.search("^ *==* *([^ ]*) *==*", i)
        if m:
            tag = m.group(1)
            if tag in tag_list:
                perf_dic[tag] = {}
            continue
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
        film_m = re.search("^ *\* *\[\[([^]]*)\]\]", i)
        if film_m:
            film = film_m.group(1) # 出演作品
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

f = open('pageid.dat','r')
f_va = open('valist.txt','w')

for f_str in glob.glob('pages/*'):
    pageid_str = os.path.basename(f_str)
    pageid_str, ext = os.path.splitext(pageid_str)

    f = open(f_str,'r')
    honbun_str = f.read()
    f.close()
    
    name = ParseName(honbun_str)
    wikiform = ParseFormat(honbun_str)
    jobs = ParseJob(honbun_str)
    if name == None:
        # print('A:'+f_str)
        continue
    if jobs == None and wikiform == None:
        # print(name)
        continue
    if jobs == None:
        # print(name+',form:'+wikiform)
        continue
    if wikiform == None:
        # print(name+',jobs:'+','.join(jobs))
        continue
    if not '声優' in jobs:
        # print(name+',jobs:'+','.join(jobs)+',form:'+wikiform)
        continue

    if not wikiform in ["声優","ActorActress"]:
        # print(name+',jobs:'+','.join(jobs)+',form:'+wikiform)
        continue

    f_va.write(pageid_str+'\n')
    # b_year = ParseBirth('生年',honbun_str)
    # b_mon  = ParseBirth('生月',honbun_str)
    # b_day  = ParseBirth('生日',honbun_str)
    # birthday_str = b_year + '/' + b_mon + '/' + b_day
    # print(name)
    # print(jobs)

    #perf = ParsePerf(honbun_str,of, id_str=pageid_str, name=name, birthday_str)
    # ap_list = [name,pageid_str,birthday_str]
    # perf = ParsePerf(honbun_str,of, ap_list)

f_va.close()
