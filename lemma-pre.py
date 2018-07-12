#!usr/bin/env python3
# -*- coding: utf-8 -*-

'download the data for lemma'


import nltk

nltk.download("wordnet")
print('wordnet download complete.')
nltk.download('sentiwordnet')
print('sentiwordnet download complete.')
nltk.download("averaged_perceptron_tagger")
print('averaged_perceptron_tagger download complete.')
nltk.download("punkt")
print('punkt download complete.')
nltk.download("maxnet_treebank_pos_tagger")
print('maxnet_treebank_pos_tagger download complete.')