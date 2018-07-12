#!usr/bin/env python3
# -*- coding: utf-8 -*-

'Extract medical features'


import json


floders = ['breast-cancer', 'colon-cancer', 'diabetes', 'lung-cancer']
for floder in floders:
    with open('res\\%s-lemma.txt' % floder, 'r', encoding='utf8') as f:
        files = json.loads(f.read())
    # print(file_list)
    res = {}
    for file in files:
        try:
            with open('source_map\\%s\\%s.metamap' % (floder, file[0:5]), 'r', encoding='utf8') as f:
                text = f.read().lower()
            # print(text.count('[aapp]'))
            res[file] = [text.count('[aapp]'), text.count('[acab'), text.count('[anab]'), text.count('[antb]'), text.count('[bdsy]'), text.count('[blor]'), text.count('[bmod]'), text.count('[bpoc]'), text.count('[clna]'), text.count('[clnd]'), text.count('[diap]'), text.count('[dsyn]'), text.count('[horm]'), text.count('[imft]'), text.count('[inpo]'), text.count('[lbpr]'), text.count('[lbtr]'), text.count('[neop]'), text.count('[orch]'), text.count('[patf]'), text.count('[phsu]'), text.count('[podg]'), text.count('[prog]'), text.count('[sosy]'), text.count('[topp]'), text.count('[virs]'), text.count('[vita]')]
        except:
            res[file] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # print(res)
    print(len(res))
    with open('res\\%s-metamap.txt' % floder, 'w', encoding='utf8') as f:
        f.write(json.dumps(res))
    print('floder: %s complete.' % floder)
