#!usr/bin/env python3
# -*- coding: utf-8 -*-

'svm train'


import numpy as np
from sklearn import svm
import json
from sklearn.externals import joblib


floders = ['breast-cancer', 'colon-cancer', 'diabetes', 'lung-cancer']
i = 0
res = {}
res['x_train'] = []
res['y_train'] = []
res['x_train1'] = []
res['y_train1'] = []
res['x_train2'] = []
res['y_train2'] = []
res['x_train3'] = []
res['y_train3'] = []
res['x_train4'] = []
res['y_train4'] = []
for floder in floders:
    i += 1
    with open('res\\%s-wordvec.txt' % floder, 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    with open('res\\%s-lexicon.txt' % floder, 'r', encoding='utf8') as f:
        label = [int(w.strip().split(' ')[2]) for w in f.readlines()[0:-2]]
    with open('res\\%s-metamap.txt' % floder, 'r', encoding='utf8') as f:
        metamap = json.loads(f.read())
    # print(len(data), len(label))
    count = 0
    threshold = int(len(data) * 0.8)
    # print(threshold)
    for file in data:
        if count <= threshold:
            data[file].extend(metamap[file])
            res['x_train'].append(data[file])
            res['y_train'].append(label[count])
        else:
            data[file].extend(metamap[file])
            res['x_train%s' % i].append(data[file])
            res['y_train%s' % i].append(label[count])
        count += 1
    print('floder: %s completed.' % floder)
res['x_train'] = np.array(res['x_train'])
res['y_train'] = np.array(res['y_train'])
res['x_train1'] = np.array(res['x_train1'])
res['y_train1'] = np.array(res['y_train1'])
res['x_train2'] = np.array(res['x_train2'])
res['y_train2'] = np.array(res['y_train2'])
res['x_train3'] = np.array(res['x_train3'])
res['y_train3'] = np.array(res['y_train3'])
res['x_train4'] = np.array(res['x_train4'])
res['y_train4'] = np.array(res['y_train4'])


print('training...')
clf = svm.SVC(C=2, probability=True, kernel='linear')
clf.fit(res['x_train'], res['y_train'])
print('training completd.')
joblib.dump(clf, 'model/svm.pkl')


clf = joblib.load('model/svm.pkl')
print('test accuracy: %.5f' % clf.score(res['x_train1'], res['y_train1']))
print('test accuracy: %.5f' % clf.score(res['x_train2'], res['y_train2']))
print('test accuracy: %.5f' % clf.score(res['x_train3'], res['y_train3']))
print('test accuracy: %.5f' % clf.score(res['x_train4'], res['y_train4']))


# [0:100]
# test accuracy: 0.66667
# test accuracy: 0.60094
# test accuracy: 0.64501
# test accuracy: 0.62286
#
#
# [0:115]
# test accuracy: 0.69620
# test accuracy: 0.61502
# test accuracy: 0.64965
# test accuracy: 0.64571
#
#
# [0:145]
# test accuracy: 0.70464
# test accuracy: 0.65258
# test accuracy: 0.67517
# test accuracy: 0.70286


print("test:")
print(clf.predict(res['x_train1']))
print("value:")
print(res['y_train1'])




# test accuracy: 0.70464
# test accuracy: 0.61502
# test accuracy: 0.64965
# test accuracy: 0.62286

# test accuracy: 0.69620
# test accuracy: 0.60094
# test accuracy: 0.64501
# test accuracy: 0.64571

# test accuracy: 0.66667
# test accuracy: 0.65258
# test accuracy: 0.67517
# test accuracy: 0.70286