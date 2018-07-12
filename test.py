# import lemma
# import re
# import json
# import codecs


# text = [w.strip() for w in codecs.open('test.csv', 'r', encoding='utf8').readlines()][0:50000]
# print('success.')
# i = 0
# data = {}
# for each in text:
#     i += 1
#     res = []
#     each = lemma.pat_esc1.sub('"', each)
#     each = lemma.pat_esc2.sub('&', each)
#     each = lemma.pat_esc3.sub('<', each)
#     each = lemma.pat_esc4.sub('>', each)
#     each = lemma.pat_esc5.sub(' ', each)
#     each = lemma.pat_website.sub('', each)
#     each = lemma.pat_email.sub('', each)
#     sentence_list = re.split(r'[\.\?!;]+', each)
#     # print(sentence_list)
#     for sentence in sentence_list:
#         # print(sentence_list[i])
#         sentence = lemma.merge_sentence(sentence)
#         # print(sentence_list[i])
#         if len(sentence.split()) == 0:
#             continue
#         res.append(sentence)
#     res = list(map(lambda x: lemma.merge_word(x), res))
#     # print(res)
#     res1 = []
#     for each in res:
#         if len(each) == 0:
#             continue
#         res1.append(each)
#     if len(res1) != 0:
#         data[i] = res1
# with open('res\\test-lemma.txt', 'w', encoding='utf8') as f:
#     f.write(json.dumps(data))


import lexicon_analysis


lexicon_analysis.polarity_analsis('test')
