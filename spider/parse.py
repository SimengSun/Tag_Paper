__author__ = 'ssm'

import json
import os

path = ".\\raw_data\\"
newpath = ".\\data\\"
files = os.listdir(path)
for file in files:
    texts = []
    kws = []
    with open(path+file, "r") as f:
        parsed = json.load(f)
        for it in parsed:
            texts.append(it['title'] + " " + it['brief'] + "\n")
            kws.append(it['keywords'] + '\n')
    with open(newpath + "\\" + file.strip('.json'), "w") as tf:
        for t in texts:
            tf.write(t.encode('utf-8'))
    with open(newpath + "\\" + file.strip('.json') + "_kw", "w") as kf:
        for kw in kws:
            kf.write(kw.encode('utf-8'))

