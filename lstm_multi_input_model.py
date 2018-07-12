#!usr/bin/env python3
# -*- coding: utf-8 -*-

'lstm multi-input model: consider emoticon features and medical domain features'

from keras.layers import Input, Embedding, LSTM, Dense
from keras.models import Model
from keras.models import load_model
import keras
import pickle
import numpy as np
from keras.preprocessing import sequence
import lstm_dict


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


def train(train_main_x, train_emoticon_x, train_metamap_x, train_y, n_symbols, embedding_weights):
    print('Building the model...')

    main_input = Input(shape=(input_length,), dtype='int32', name='main_input')
    x = Embedding(output_dim=vocab_dim, input_dim=n_symbols, mask_zero=True, weights=[embedding_weights], input_length=input_length)(main_input)
    lstm_out = LSTM(output_dim=50, activation='sigmoid', inner_activation='hard_sigmoid')(x)
    auxiliary_output = Dense(1, activation='sigmoid', name='aux_output')(lstm_out)

    emoticon_input = Input(shape=(15,), name='emoticon_input')
    x = keras.layers.concatenate([lstm_out, emoticon_input])
    x = Dense(64, activation='relu')(x)
    emoticon_output = Dense(1, activation='sigmoid', name='emoticon_output')(x)

    metamap_input = Input(shape=(27,), name='metamap_input')
    x = keras.layers.concatenate([lstm_out, emoticon_input, metamap_input])
    x = Dense(64, activation='relu')(x)
    x = Dense(64, activation='relu')(x)
    x = Dense(64, activation='relu')(x)
    metamap_output = Dense(1, activation='sigmoid', name='metamap_output')(x)

    model = Model(inputs=[main_input, emoticon_input, metamap_input], outputs=[metamap_output, auxiliary_output, emoticon_output])
    model.compile(optimizer='rmsprop', loss={'metamap_output': 'binary_crossentropy', 'aux_output': 'binary_crossentropy', 'emoticon_output': 'binary_crossentropy'}, loss_weights={'metamap_output': 1., 'aux_output': 0.2, 'emoticon_output': 0.2}, metrics=['accuracy'])

    print('Model building complete...')
    print('Start training...')

    model.fit({'main_input': train_main_x, 'emoticon_input': train_emoticon_x, 'metamap_input': train_metamap_x}, {'metamap_output': train_y, 'aux_output': train_y, 'emoticon_output': train_y}, epochs=n_epochs, batch_size=batch_size)

    print('Training completed.')

    model.save('model/lstm.h5')

    print('model has been saved.')


def evaluation(test_main, test_emoticon, test_metamap, test_y):
    model = load_model('model/lstm.h5')
    # print(test_main.shape, test_emoticon.shape, test_metamap.shape, test_y.shape)
    s1, s2, s3, s4, acc1, acc2, acc3 = model.evaluate({'main_input': test_main, 'emoticon_input': test_emoticon, 'metamap_input': test_metamap}, {'metamap_output': test_y, 'aux_output': test_y, 'emoticon_output': test_y}, batch_size=batch_size)
    # print('Test score: %s' % s1)
    print('Test accuracy: %s %s %s' % (acc2, acc3, acc1))


if __name__ == '__main__':
    sentence, label, length, emoticons, metamap = lstm_dict.get_exper_corpora()
    maxlen = 0
    for sen in sentence:
        if len(sen) > maxlen:
            maxlen = len(sen)

    vocab_dim = 100
    batch_size = 32
    n_epochs = 50
    input_length = maxlen

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
    train_test['x_train_main'] = []
    train_test['x_train_emoticon'] = []
    train_test['x_train_metamap'] = []
    train_test['y_train'] = []
    train_test['x_test_main1'] = []
    train_test['x_test_emoticon1'] = []
    train_test['x_test_metamap1'] = []
    train_test['y_test1'] = []
    train_test['x_test_main2'] = []
    train_test['x_test_emoticon2'] = []
    train_test['x_test_metamap2'] = []
    train_test['y_test2'] = []
    train_test['x_test_main3'] = []
    train_test['x_test_emoticon3'] = []
    train_test['x_test_metamap3'] = []
    train_test['y_test3'] = []
    train_test['x_test_main4'] = []
    train_test['x_test_emoticon4'] = []
    train_test['x_test_metamap4'] = []
    train_test['y_test4'] = []
    i = 0
    j = 0
    for l in length:
        i += 1
        temp = j + int(l * 0.8)
        train_test['x_train_main'].extend(sentence[j:temp])
        train_test['x_train_emoticon'].extend(emoticons[j:temp])
        train_test['x_train_metamap'].extend(metamap[j:temp])
        train_test['y_train'].extend(label[j:temp])
        train_test['x_test_main%s' % i].extend(sentence[temp:(l+j)])
        train_test['x_test_emoticon%s' % i].extend(emoticons[temp:(l+j)])
        train_test['x_test_metamap%s' % i].extend(metamap[temp:(l+j)])
        train_test['y_test%s' % i].extend(label[temp:(l+j)])
        j += l

    X_train_main = text_to_index_array(new_dic, train_test['x_train_main'])
    X_test_main1 = text_to_index_array(new_dic, train_test['x_test_main1'])
    X_test_main2 = text_to_index_array(new_dic, train_test['x_test_main2'])
    X_test_main3 = text_to_index_array(new_dic, train_test['x_test_main3'])
    X_test_main4 = text_to_index_array(new_dic, train_test['x_test_main4'])

    # print(X_train_main.shape, X_test_main1.shape, X_test_main2.shape, X_test_main3.shape, X_test_main4.shape)

    X_train_emoticon = np.array(train_test['x_train_emoticon'])
    X_test_emoticon1 = np.array(train_test['x_test_emoticon1'])
    X_test_emoticon2 = np.array(train_test['x_test_emoticon2'])
    X_test_emoticon3 = np.array(train_test['x_test_emoticon3'])
    X_test_emoticon4 = np.array(train_test['x_test_emoticon4'])

    X_train_metamap = np.array(train_test['x_train_metamap'])
    X_test_metamap1 = np.array(train_test['x_test_metamap1'])
    X_test_metamap2 = np.array(train_test['x_test_metamap2'])
    X_test_metamap3 = np.array(train_test['x_test_metamap3'])
    X_test_metamap4 = np.array(train_test['x_test_metamap4'])

    y_train = np.array(train_test['y_train'])
    y_test1 = np.array(train_test['y_test1'])
    y_test2 = np.array(train_test['y_test2'])
    y_test3 = np.array(train_test['y_test3'])
    y_test4 = np.array(train_test['y_test4'])

    X_train_main = sequence.pad_sequences(X_train_main, maxlen=maxlen)
    X_test_main1 = sequence.pad_sequences(X_test_main1, maxlen=maxlen)
    X_test_main2 = sequence.pad_sequences(X_test_main2, maxlen=maxlen)
    X_test_main3 = sequence.pad_sequences(X_test_main3, maxlen=maxlen)
    X_test_main4 = sequence.pad_sequences(X_test_main4, maxlen=maxlen)

    # train(X_train_main, X_train_emoticon, X_train_metamap, y_train, n_symbols, embedding_weights)

    print('Breast-cancer-test:')
    evaluation(X_test_main1, X_test_emoticon1, X_test_metamap1, y_test1)
    print('Colon-cancer-test:')
    evaluation(X_test_main2, X_test_emoticon2, X_test_metamap2, y_test2)
    print('Diabetes-test:')
    evaluation(X_test_main3, X_test_emoticon3, X_test_metamap3, y_test3)
    print('Lung-cancer-test:')
    evaluation(X_test_main4, X_test_emoticon4, X_test_metamap4, y_test4)

# Breast-cancer-test:
# 238/238 [==============================] - 1s 3ms/step
# Test accuracy: 0.16386554696980646 0.1974789923479577 0.18067226965888208
# Colon-cancer-test:
# 214/214 [==============================] - 1s 3ms/step
# Test accuracy: 0.2336448602308737 0.2570093462121821 0.2476635518196587
# Diabetes-test:
# 432/432 [==============================] - 1s 2ms/step
# Test accuracy: 0.20833333333333334 0.25462962962962965 0.23842592592592593
# Lung-cancer-test:
# 176/176 [==============================] - 1s 4ms/step
# Test accuracy: 0.2784090909090909 0.3068181818181818 0.30113636363636365
