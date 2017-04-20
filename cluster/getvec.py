
__author__ = 'ssm'

import numpy as np

'''
#redis
r = redis.StrictRedis(host='10.2.1.7', port=6379, db=0)

kws = Util.get_keywords(r)
vecs = {}
i = 0
for w in kws:
    if r.exists(w):
        vecs[w] = Util.get_vec(w)
    if i % 10000 == 0:
        print("end process {}".format(i))
    i += 1

np.save("kejso_wv", vecs)
'''


def load_words():
    all_keywords = {}
    with open("all_keywords.txt", "r") as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            all_keywords[line.strip()] = 1
            i += 1
            if i % 10000 == 0:
                print("end process {}".format(i))
    keywords_rank = {}
    with open("keywordrank.txt", "r") as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            sp = line.split()
            if len(sp) != 2:
                continue
            elif int(sp[1]) > 850:
                keywords_rank[sp[0]] = 1
            i += 1
            if i % 10000 == 0:
                print("end process {}".format(i))
    return all_keywords, keywords_rank

def filter_words(ak, kr):
    re = []
    for a in kr.keys():
        if ak.has_key(a):
            re.append(a)
    return re

ak, kr = load_words()
re = filter_words(ak, kr)

print(len(re))

with open("filter_words.txt", "w") as f:
    for r in re:
        f.write(r + "\n")

vecs = np.load("kejso_wv_filter_400.npy").item()

def get_new_dic(vecs, re):
    result = {}
    i = 0
    for r in re:
        if vecs.has_key(r.decode('utf-8')):
            result[r.decode('utf-8')] = vecs[r.decode('utf-8')]
        i += 1
        if i % 10000 == 0:
            print("end process {}".format(i))
    return result

result = get_new_dic(vecs, re)
np.save("kejso_wv_filter_850", result)