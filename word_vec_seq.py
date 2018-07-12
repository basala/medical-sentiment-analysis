#!usr/bin/env python3
# -*- coding: utf-8 -*-

'Convert documents to word vector sequences'


from gensim.models.keyedvectors import KeyedVectors
import numpy
import json
from sklearn import preprocessing
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


model = KeyedVectors.load_word2vec_format('model/GoogleNews-vectors-negative300.bin', binary=True)
floders = ['breast-cancer', 'colon-cancer', 'diabetes', 'lung-cancer']
res = []
emotions = []
full_wordvec = []
emoticons = {'e1': 'happy', 'e2': 'sad', 'e3': 'cry', 'e4': 'happy', 'e5': 'unhappy', 'e6': 'awkward', 'e7': 'confused', 'e8': 'happy', 'e9': 'blush', 'e10': 'shock', 'e11': 'happy', 'e12': 'ill', 'e13': 'angry', 'e14': 'anxious', 'e15': 'anxious'}


for floder in floders:
    print(len(res))
    with open('res\\%s-lemma.txt' % floder, 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    for file in data:
        word_list = []
        word_vec = []
        for sentence_list in data[file]:
            word_list.extend(sentence_list)
        emotions.append([word_list.count('e1'), word_list.count('e2'), word_list.count('e3'), word_list.count('e4'), word_list.count('e5'), word_list.count('e6'), word_list.count('e7'), word_list.count('e8'), word_list.count('e9'), word_list.count('e10'), word_list.count('e11'), word_list.count('e12'), word_list.count('e13'), word_list.count('e14'), word_list.count('e15')])
        for word in word_list:
            # if word in emoticons:
            #     word = emoticons[word]
            if word in model:
                word_vec.append(model[word])
        full_wordvec.append(word_vec)
        if len(word_vec) != 0:
            res.append(sum(numpy.array(word_vec)) / len(word_vec))
        else:
            print(file)
    print('floder: %s complete.' % floder)


x = preprocessing.scale(numpy.array(res))
pca = PCA(n_components=300)
pca.fit(x)
plt.figure(1, figsize=(4, 3))
plt.clf()
plt.axes([.2, .2, .7, .7])
plt.plot(pca.explained_variance_, linewidth=2)
plt.axis('tight')
plt.xlabel('n_components')
plt.ylabel('explained_variance_')
plt.show()
# 100


x_reduced = list(PCA(n_components=100).fit_transform(x))


for index in range(len(x_reduced)):
    # print(index)
    # print(type(x_reduced[index]))
    x_reduced[index] = list(x_reduced[index])
    # print(type(x_reduced[index]))
    x_reduced[index].extend(emotions[index])


i = 0
for floder in floders:
    res = {}
    with open('res\\%s-lemma.txt' % floder, 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    for file in data:
        res[file] = numpy.array(x_reduced[i]).tolist()
        i += 1
    with open('res\\%s-wordvec.txt' % floder, 'w', encoding='utf8') as f:
        f.write(json.dumps(res))
    print('floder: %s completed.' % floder)
    print(i)
