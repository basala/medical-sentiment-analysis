#!usr/bin/env python3
# -*- coding: utf-8 -*-

'get subject-score > 0.5 words from sentiwordnet'


from nltk.corpus import sentiwordnet as swn
import json


pos = {}
neg = {}
all = list(swn.all_senti_synsets())
for each in all:
    if each.pos_score() > 0.5:
        pos[each.__repr__()[13:-7]] = each.pos_score()
    if each.neg_score() > 0.5:
        neg[each.__repr__()[13:-7]] = each.neg_score()
with open('basic_pos_words.txt', 'w', encoding='utf8') as f:
    f.write(json.dumps(pos))
with open('basic_neg_words.txt', 'w', encoding='utf8') as f:
    f.write(json.dumps(neg))
print('complete.')
