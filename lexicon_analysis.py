#!usr/bin/env python3
# -*- coding: utf-8 -*-

'base on subjective lexicon analysis'


import json
from math import log


basic_neg_word = json.loads(open('basic_neg_words.txt', 'r', encoding='utf8').read())
basic_pos_word = json.loads(open('basic_pos_words.txt', 'r', encoding='utf8').read())


emoticons = {'e1': 'happy', 'e2': 'sad', 'e3': 'cry', 'e4': 'happy', 'e5': 'unhappy', 'e6': 'awkward', 'e7': 'confused', 'e8': 'happy', 'e9': 'blush', 'e10': 'shock', 'e11': 'happy', 'e12': 'ill', 'e13': 'angry', 'e14': 'anxious', 'e15': 'anxious'}
reverse_word = ['not', 'no', 'little', 'less', 'few', 'without', 'hardly', 'seldom', 'never', 'rarely', 'barely']


def polarity_analsis(fl):
    print('start merge file: %s' % fl)
    # time.sleep(5)
    pos = 0
    neg = 0
    with open('res\\%s-lemma.txt' % fl, 'r', encoding='utf8') as f:
        file_list = json.loads(f.read())
    for file in file_list:
        res = {}
        res['file'] = file
        sentence_list = file_list[file]
        res['score'] = round(compute_score(sentence_list), 6)
        print(file, res['score'])
        if res['score'] < -0.02631:
            res['label'] = -1
            neg += 1
        else:
            res['label'] = 1
            pos += 1
        save(fl, res)
    with open('res\\%s-lexicon.txt' % fl, 'a', encoding='utf8') as f:
        f.write('pos: %s\nneg: %s' % (pos, neg))
    print('file: %s completed.' % fl)
    # time.sleep(5)


def compute_score(sl):
    # print(sl)
    sentence_list = []
    for sentence in sl:
        temp = []
        for word in sentence:
            if word in emoticons:
                word = emoticons[word]
            temp.append(word)
        sentence_list.append(temp)
    # print(sentence_list)
    score = 0
    word_list = []
    pos_word_list = []
    neg_word_list = []
    obj_word_list = []
    for sentence in sentence_list:
        word_list.extend(sentence)
    sentence_length = len(word_list)
    word_count = count(word_list)
    # print(word_count)
    for word in word_list:
        if word in basic_neg_word:
            neg_word_list.append(word)
        else:
            if word in basic_pos_word:
                pos_word_list.append(word)
            else:
                obj_word_list.append(word)
    # print(pos_word_list)
    pos_word_list = list(set(pos_word_list))
    neg_word_list = list(set(neg_word_list))
    obj_word_list = list(set(obj_word_list))
    # print(pos_word_list, neg_word_list, obj_word_list)
    for word in obj_word_list:
        frequency_wp = 1
        frequency_wn = 1
        frequency_p = 1
        frequency_n = 1
        for pos in pos_word_list:
            temp = count_word_pair(word, pos, sentence_list)
            frequency_wp *= temp if temp != 0 else 1
            frequency_p *= word_count[pos][0] if temp != 0 else 1
        for neg in neg_word_list:
            temp = count_word_pair(word, neg, sentence_list)
            frequency_wn *= temp if temp != 0 else 1
            frequency_p *= word_count[neg][0] if temp != 0 else 1
        so_pmi = log((frequency_wp * frequency_n) / (frequency_wn * frequency_p), 2)
        word_count[word].append(so_pmi * word_count[word][0])
    # print(word_count)
    for word in pos_word_list:
        num = 0
        for reverse in reverse_word:
            num += count_reverse_word_pair(word, reverse, sentence_list)
        word_count[word].append(basic_pos_word[word] * (word_count[word][0] - num * 2))
    for word in neg_word_list:
        if word in reverse_word:
            word_count[word].append(basic_neg_word[word] * word_count[word][0] * -1)
            continue
        num = 0
        for reverse in reverse_word:
            num += count_reverse_word_pair(word, reverse, sentence_list)
        word_count[word].append(basic_neg_word[word] * (word_count[word][0] - num * 2) * -1)
    # print(word_count)
    for word in word_count:
        score += word_count[word][1]
    score /= sentence_length
    # print(score)
    return score


def count(word_list):
    res = {}
    for word in word_list:
        if word in res:
            res[word][0] += 1
        else:
            res[word] = [1]
    return res


def count_word_pair(word, refer, sentence_list):
    count = 0
    for sentence in sentence_list:
        if word in sentence and refer in sentence:
            count += 1
    return count


def count_reverse_word_pair(word, refer, sentence_list):
    count = 0
    for sentence in sentence_list:
        reverse_num = 0
        for w in sentence:
            if w in reverse_word:
                reverse_num += 1
        if word in sentence and reverse_num % 2 == 1:
            count += sentence.count(word)
    return count


def save(fl, res):
    with open('res\\%s-lexicon.txt' % fl, 'a', encoding='utf8') as f:
        f.write('%s %s %s\n' % (res['file'], res['score'], res['label']))


if __name__ == '__main__':
    floders = ['breast-cancer', 'colon-cancer', 'diabetes', 'lung-cancer']
    # floders = ['breast-cancer']
    for fl in floders:
        polarity_analsis(fl)
