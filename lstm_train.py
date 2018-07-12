#!usr/bin/env python3
# -*- coding: utf-8 -*-

'lstm train'


import numpy as np
import pickle
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Dropout, Activation
import lstm_dict


np.random.seed(1337)


sentence, label, length, emoticons, metamap = lstm_dict.get_exper_corpora()
maxlen = 0
for sen in sentence:
    if len(sen) > maxlen:
        maxlen = len(sen)


vocab_dim = 100
batch_size = 32
n_epoch = 5
input_length = maxlen


def text_to_index_array(p_new_dic, p_sen):
    new_sentences = []
    for sen in p_sen:
        new_sen = []
        for word in sen:
            try:
                new_sen.append(p_new_dic[word])
            except:
                new_sen.append(0)
        new_sentences.append(new_sen)
    return np.array(new_sentences)


def train_lstm(p_n_symbols, p_embedding_weights, p_X_train, p_y_train, X_test1, y_test1, X_test2, y_test2, X_test3, y_test3, X_test4, y_test4):
    model = Sequential()
    model.add(Embedding(output_dim=vocab_dim, input_dim=p_n_symbols, mask_zero=True, weights=[p_embedding_weights], input_length=input_length))
    model.add(LSTM(output_dim=50, activation='sigmoid', inner_activation='hard_sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(p_X_train, p_y_train, batch_size=batch_size, nb_epoch=n_epoch)
    print('train completed...')
    score1, acc1 = model.evaluate(X_test1, y_test1, batch_size=batch_size)
    score2, acc2 = model.evaluate(X_test2, y_test2, batch_size=batch_size)
    score3, acc3 = model.evaluate(X_test3, y_test3, batch_size=batch_size)
    score4, acc4 = model.evaluate(X_test4, y_test4, batch_size=batch_size)
    print('Test score1: %s' % score1)
    print('Test accuracy1: %s' % acc1)
    print('Test score2: %s' % score2)
    print('Test accuracy2: %s' % acc2)
    print('Test score3: %s' % score3)
    print('Test accuracy3: %s' % acc3)
    print('Test score4: %s' % score4)
    print('Test accuracy4: %s' % acc4)


def sequence_to_np(array):
    temp = []
    for each in array:
        temp.append(np.array(each))
    return np.array(temp)


if __name__ == '__main__':
    with open('model/lstm_data.pkl', 'rb') as f:
        index_dict = pickle.load(f)
        word_vectors = pickle.load(f)
    print('load data complete.')
    new_dic = index_dict
    n_symbols = len(index_dict) + 1
    embedding_weights = np.zeros((n_symbols, 100))
    for w, index in index_dict.items():
        embedding_weights[index, :] = word_vectors[w]

    train_test = {}
    train_test['x_train'] = []
    train_test['y_train'] = []
    train_test['x_test1'] = []
    train_test['y_test1'] = []
    train_test['x_test2'] = []
    train_test['y_test2'] = []
    train_test['x_test3'] = []
    train_test['y_test3'] = []
    train_test['x_test4'] = []
    train_test['y_test4'] = []
    i = 0
    j = 0
    for l in length:
        i += 1
        temp = j + l - 200
        train_test['x_train'].extend(sentence[j:temp])
        train_test['y_train'].extend(label[j:temp])
        train_test['x_test%s' % i].extend(sentence[temp:(l+j)])
        train_test['y_test%s' % i].extend(label[temp:(l+j)])
        j += l

    X_train = text_to_index_array(new_dic, train_test['x_train'])
    X_test1 = text_to_index_array(new_dic, train_test['x_test1'])
    X_test2 = text_to_index_array(new_dic, train_test['x_test2'])
    X_test3 = text_to_index_array(new_dic, train_test['x_test3'])
    X_test4 = text_to_index_array(new_dic, train_test['x_test4'])

    y_train = np.array(train_test['y_train'])
    y_test1 = np.array(train_test['y_test1'])
    y_test2 = np.array(train_test['y_test2'])
    y_test3 = np.array(train_test['y_test3'])
    y_test4 = np.array(train_test['y_test4'])

    X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
    X_test1 = sequence.pad_sequences(X_test1, maxlen=maxlen)
    X_test2 = sequence.pad_sequences(X_test1, maxlen=maxlen)
    X_test3 = sequence.pad_sequences(X_test1, maxlen=maxlen)
    X_test4 = sequence.pad_sequences(X_test1, maxlen=maxlen)

    print('lstm start....')
    train_lstm(n_symbols, embedding_weights, X_train, y_train, X_test1, y_test1, X_test2, y_test2, X_test3, y_test3, X_test4, y_test4)


# Test accuracy1: 0.25
# Test score2: -0.034968414306640626
# Test accuracy2: 0.21
# Test score3: 0.34251659393310546
# Test accuracy3: 0.19
# Test score4: 0.6963114404678344
# Test accuracy4: 0.205
