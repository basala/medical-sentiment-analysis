#!usr/bin/env python3
# -*- coding: utf-8 -*-

'lexical reduction for filterred text'


from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
import re
import time
import os
import json


stop_word_list = [w.strip() for w in open('stopwords.txt', 'r', encoding='utf8').readlines()]
username_list = list(set([w.strip() for w in open('stopwords.txt', 'r', encoding='utf8').readlines()]))


# to replace emotion symbols
pat_emotion1 = re.compile(r':\s*[-~]?\s*\)')
pat_emotion2 = re.compile(r':\s*[-~]?\s*\(')
pat_emotion3 = re.compile(r':\s*[-~]?\s*\(\s*\(')
pat_emotion4 = re.compile(r':\s*[-~]?\s*\)\s*\)')
pat_emotion5 = re.compile(r':\s*[-~]?\s*<')
pat_emotion6 = re.compile(r':\s*\$')
pat_emotion7 = re.compile(r':\s*-/')
pat_emotion8 = re.compile(r':\s*">')
pat_emotion9 = re.compile(r':\s*[Pp]')
pat_emotion10 = re.compile(r':\s*[Oo]\)?')
pat_emotion11 = re.compile(r':\s*[Dd]\)?')
pat_emotion12 = re.compile(r':\s*-\s*&')
pat_emotion13 = re.compile(r'X\s*-\s*\(')
pat_emotion14 = re.compile(r':\s*-\s*[Ss]')
pat_emotion15 = re.compile(r'\bx\s*o\b')
# to replace the escape character
pat_esc1 = re.compile(r'&quot;')
pat_esc2 = re.compile(r'&amp;')
pat_esc3 = re.compile(r'&lt;')
pat_esc4 = re.compile(r'&gt;')
pat_esc5 = re.compile(r'nbsp;')
# to replace the website to ''
pat_website = re.compile(r'(http://|https://)(\w|=|\?|\.|\/|&|-)+', re.IGNORECASE)
pat_email = re.compile(r'(email:?\s*)?([\w\-_]+(?:\.[\w\-_]+)*)@((?:[a-z0-9]+(?:-[a-zA-Z0-9]+)*)+\.[a-z]{2,6})', re.IGNORECASE)
# to find chars that are not a letter, a blank or a quotation
pat_letter = re.compile(r'[^a-zA-Z \'\d’]+')
pat_num = re.compile(r'.*\d+.*')
# to find the 's following the pronouns
pat_is = re.compile(r"(it|he|she|that|this|there|here)(['’]s)")
# to find the 's following the letters
pat_s = re.compile(r"(?<=[a-zA-Z])'s")
# to find the ' following the words ending by s
pat_s2 = re.compile(r"(?<=s)['’]s?")
# to find the abbreviation of not
pat_not = re.compile(r"(?<=can)['’]t")
pat_not1 = re.compile(r"\s+won['’]t\s+")
pat_not2 = re.compile(r"(?<=[a-zA-Z])n['’]t")
pat_not3 = re.compile(r'\s+(do|did|have|had|would|should|are|were|was)nt\s+')
pat_not4 = re.compile(r'\s+wont\s+')
# to find the abbreviation of would
pat_would = re.compile(r"(?<=[a-zA-Z])['’]d")
# to find the abbreviation of will
pat_will = re.compile(r"(?<=[a-zA-Z])['’]ll")
# to find the abbreviation of am
pat_am = re.compile(r"(?<=[I|i])['’]m")
pat_am1 = re.compile(r'\s+im\s+')
# to find the abbreviation of are
pat_are = re.compile(r"(?<=[a-zA-Z])[\’]re")
# to find the abbreviation of have
pat_ve = re.compile(r"(?<=[a-zA-Z])['’]ve")
pat_ve1 = re.compile(r'\s+ive\s+')

lemmatizer = WordNetLemmatizer()


def get_file_list(floder):
    res = []
    file_list = list(map(lambda x: os.path.join(os.path.join('source', floder), x), os.listdir(os.path.join('source', floder))))
    # print(file_list)
    for fl in file_list:
        res.append(fl)
    return res


def lexical_reduction(fl):
    global index
    print('Start lexical reduction...')
    print('Loading file list...')
    file_list = get_file_list(fl)
    # file_list = ['source\\breast-cancer\\00205.txt']
    # time.sleep(3)
    print('Loading completed...')
    # print(file_list, len(file_list))
    data = {}
    for file in file_list:
        index += 1
        print('Dealing with NO.%d document...' % index)
        print('file name: %s' % file)
        res = []
        # test_file = 'anxiety\\00006-can chamomile tea cause anxiety#.txt'
        # test_file = 'test.txt'
        with open(file, 'r', encoding='utf8') as f:
            text = f.readlines()
        for line in text:
            line = pat_esc1.sub('"', line)
            line = pat_esc2.sub('&', line)
            line = pat_esc3.sub('<', line)
            line = pat_esc4.sub('>', line)
            line = pat_esc5.sub(' ', line)
            line = pat_website.sub('', line)
            line = pat_email.sub('', line)
            sentence_list = re.split(r'[\.\?!;]+', line.strip())
            # print(sentence_list)
            for sentence in sentence_list:
                # print(sentence_list[i])
                sentence = merge_sentence(sentence)
                # print(sentence_list[i])
                if len(sentence.split()) == 0:
                    continue
                res.append(sentence)
        # print(res)
        res = list(map(lambda x: merge_word(x), res))
        # print(res)
        res1 = []
        for each in res:
            if len(each) == 0:
                continue
            res1.append(each)
        if len(res1) != 0:
            data[file.split('\\')[-1]] = res1
        # print(res)
        # break
        print('NO.%d document completed.' % index)
    # print(data)
    # return
    save(fl, data)
    print('floder %s all completed.' % fl)


def merge_sentence(str):
    # print(str)
    res = str.strip().lower()
    res = pat_emotion1.sub('e1', res)
    res = pat_emotion2.sub('e2', res)
    res = pat_emotion3.sub('e3', res)
    res = pat_emotion4.sub('e4', res)
    res = pat_emotion5.sub('e5', res)
    res = pat_emotion6.sub('e6', res)
    res = pat_emotion7.sub('e7', res)
    res = pat_emotion8.sub('e8', res)
    res = pat_emotion9.sub('e9', res)
    res = pat_emotion10.sub('e10', res)
    res = pat_emotion11.sub('e11', res)
    res = pat_emotion12.sub('e12', res)
    res = pat_emotion13.sub('e13', res)
    res = pat_emotion14.sub('e14', res)
    res = pat_emotion15.sub('e15', res)
    res = pat_letter.sub(' ', res)
    # res = pat_num.sub(' ', res)
    res = pat_is.sub(r"\1 is", res)
    res = pat_s.sub("", res)
    res = pat_s2.sub("", res)
    res = pat_not.sub(" not", res)
    res = pat_not1.sub(" will not ", res)
    res = pat_not2.sub(" not", res)
    res = pat_not3.sub(r" \1 not ", res)
    res = pat_not4.sub(r" will not ", res)
    res = pat_not.sub(" not", res)
    res = pat_would.sub(" would", res)
    res = pat_will.sub(" will", res)
    res = pat_am.sub(" am", res)
    res = pat_am1.sub(" i am ", res)
    res = pat_are.sub(" are", res)
    res = pat_ve.sub(" have", res)
    res = pat_ve1.sub(" i have ", res)
    res = res.replace('\'', ' ')
    return res


def merge_word(sentence):
    # print(wordnet.NOUN)
    # print(lemmatizer.lemmatize('is', pos=wordnet.NOUN))
    res = []
    for word, pos in pos_tag(word_tokenize(sentence)):
        if word in stop_word_list:
            continue
        if word in username_list:
            continue
        if pat_num.match(word) and word not in ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13', 'e14', 'e15']:
            continue
        wordnet_pos = get_wordnet_pos(pos) or wordnet.NOUN
        res.append(lemmatizer.lemmatize(word, pos=wordnet_pos))
    return res


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def save(fl, res):
    # data = {}
    # data['filename'] = file
    # data['word-vector'] = res
    # data['polarity-label'] = 0
    with open('res\\%s-lemma.txt' % fl, 'a', encoding='utf8') as f:
        f.write(json.dumps(res))


if __name__ == '__main__':
    start = time.clock()
    floder_list = ['breast-cancer', 'colon-cancer', 'diabetes', 'lung-cancer']
    # floder = 'colon-cancer'
    # floder = 'diabetes'
    # floder = 'lung-cancer'
    index = 0
    for floder in floder_list:
        lexical_reduction(floder)
        # break
    end = time.clock()
    print('All files completed. %d in total. Cost time: %s' % (index, end - start))
