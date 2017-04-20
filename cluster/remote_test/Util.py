#coding: utf-8
__author__ = 'ssm'

import redis
import numpy as np

#redis
r = redis.StrictRedis(host='10.2.1.7', port=6379, db=0)

def get_r():
    return r

def get_vec(s):
    return np.fromstring(r.get(s),dtype=np.float32)

def get_keywords(r):
    re = []
    with open("all_keywords.txt", "r") as f:
        i = 0
        while True:
            line = f.readline().strip()
            if r.exists(line):
                re.append(line)
            i += 1
            if i % 10000 == 0:
                print("end iter {}".format(i))
            if i == 567397:
                break
    return re

def cluster_2nd_load_1st_words(file):
    words = []
    with open(file, "r") as f:
        lines = f.readlines()
        for w in lines[:-len(lines)/2]:
            w = w.strip()
            words.append(w.decode('utf-8'))
    return words

def cluster_2nd_load_1st_vecs(r, words):
    vecs = []
    for w in words:
        vecs.append(get_vec(w))
    return vecs