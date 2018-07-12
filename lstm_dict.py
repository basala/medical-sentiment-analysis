#!usr/bin/env python3
# -*- coding: utf-8 -*-

'get word vec & dict'


from gensim.models.keyedvectors import KeyedVectors
import pickle
import numpy as np
from gensim.corpora.dictionary import Dictionary
import json


np.random.seed(1337)  # For Reproducibility


def get_exper_corpora():
    floders = ['breast-cancer', 'colon-cancer', 'diabetes', 'lung-cancer']
    sentence = []
    length = []
    label = []
    emoticons = []
    metamap = []
    for floder in floders:
        with open('res/%s-lemma.txt' % floder, 'r', encoding='utf8') as f:
            data = json.loads(f.read())
        with open('res\\%s-lexicon.txt' % floder, 'r', encoding='utf8') as f:
            label.extend([int(w.strip().split(' ')[2]) for w in f.readlines()[0:-2]])
        with open('res\\%s-metamap.txt' % floder, 'r', encoding='utf8') as f:
            metamap_data = json.loads(f.read())
            for each in metamap_data:
                metamap.append(metamap_data[each])
        with open('res/%s-wordvec.txt' % floder, 'r', encoding='utf8') as f:
            emoticon_data = json.loads(f.read())
            for each in emoticon_data:
                emoticons.append(emoticon_data[each][-15:])
        length.append(len(data))
        for file in data:
            temp = []
            for sen in data[file]:
                temp.extend(sen)
            sentence.append(temp)
        print('floder: %s completed' % floder)
    return sentence, label, length, emoticons, metamap


def create_dictionaries(sentence):
    print('loading model....')
    model = KeyedVectors.load_word2vec_format('model/GoogleNews-vectors-negative300.bin', binary=True)
    print('loading completed.')
    temp = []
    for sen in sentence:
        tem = []
        for word in sen:
            if word in model:
                tem.append(word)
        temp.append(tem)
    gensim_dict = Dictionary(temp)
    w2indx = {v: k + 1 for k, v in gensim_dict.items()}
    w2vec = {word: model[word][0:100] for word in w2indx.keys()}
    return w2indx, w2vec


if __name__ == '__main__':
    sentence, label, length, emoticons, metamap = get_exper_corpora()
    index_dict, word_vectors = create_dictionaries(sentence)
    with open('model/lstm_data.pkl', 'wb') as f:
        pickle.dump(index_dict, f)
        pickle.dump(word_vectors, f)
