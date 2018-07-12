#!usr/bin/env python3
# -*- coding: utf-8 -*-

'Probabilistic simulation'


import random


files = ['breast-cancer', 'colon-cancer', 'diabetes', 'lung-cancer']
# files = ['breast-cancer']
for file in files:
    with open('res\\%s-lexicon.txt' % file, 'r', encoding='utf8') as f:
        file_list = [{'file': w.strip().split(' ')[0], 'score': float(w.strip().split(' ')[1]), 'label': int(w.strip().split(' ')[2])} for w in f.readlines()[0:-2]]
    res = []
    for fl in file_list:
        randnum = random.randint(0, 100000)
        res.append({'file': fl['file'], 'label': fl['label'] * -1} if randnum > 66107 else {'file': fl['file'], 'label': fl['label']})
    # print(res)
    count = 0
    pos = 0
    neg = 0
    for i in range(len(file_list)):
        if res[i]['label'] == -1:
            neg += 1
        else:
            pos += 1
        temp = -1 if file_list[i]['score'] < 0 else 1
        if res[i]['label'] == temp:
            count += 1
    print(count, len(file_list), count / len(file_list))
    with open('res\\%s-label.txt' % file, 'a', encoding='utf8') as f:
        for fl in res:
            f.write('%s %s\n' % (fl['file'], fl['label']))
        f.write('pos: %s\nneg: %s' % (pos, neg))


# 755 1190 0.634453781512605
# 711 1069 0.6651075771749299
# 1350 2160 0.625
# 577 879 0.6564277588168373
