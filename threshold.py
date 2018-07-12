#!usr/bin/env python3
# -*- coding: utf-8 -*-

'determine the highest accuracy threshold'


label = [int(w.strip().split(' ')[1]) for w in open('res\\label-test.txt').readlines()[0:298]]
test = [float(w.strip().split(' ')[1]) for w in open('res\\breast-cancer-lexicon.txt').readlines()[0:298]]
test1 = [int(w.strip().split(' ')[2]) for w in open('res\\breast-cancer-lexicon.txt').readlines()[0:298]]
num = 0
for i in range(len(test)):
    if label[i] == test1[i]:
        num += 1
print(num)
# print(label)
# print(test)
accuracy = 0
temp = -1.00001
while temp < 1.00001:
    res = []
    count = 0
    for i in range(len(test)):
        if test[i] < temp:
            res.append(-1)
        else:
            res.append(1)
    for i in range(len(test)):
        if res[i] == label[i]:
            count += 1
    if count > accuracy:
        accuracy = count
        print(accuracy, temp)
        threshold = temp
    if temp > 0:
        print(accuracy, temp)
    temp += 0.00001
print(threshold)
# 179 -1.00001
# 180 -0.9999400000000003
# 181 -0.9423000000002626
# 182 -0.9156900000003837
# 183 -0.8830600000005322
# 184 -0.7499900000011378
# 185 -0.6636300000015308
# 186 -0.6479500000016022
# 187 -0.6185800000017359
# 188 -0.5624900000019911
# 189 -0.5298500000021397
# 190 -0.5186500000021906
# 191 -0.19669000000197218
# 192 -0.189510000001965
# 193 -0.18749000000196298
# 194 -0.18664000000196213
# 195 -0.02884000000191524
# 196 -0.0273400000019153
# 197 -0.026310000001915343
# -0.026310000001915343