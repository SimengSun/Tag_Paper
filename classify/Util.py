#coding: utf-8
__author__ = 'ssm'

from gensim import corpora
import numpy as np
import codecs
from gensim import models
import os

path = ".\\data\\"

def load_file(file):
    f = open(path + file, "r")
    lines = f.readlines()
    ret = []
    for line in lines:
        line = line.strip('\n').strip()
        sp = line.split()
        ret.append([word for word in sp if len(word) > 1 ])
    return ret

def load_data():
    #load dic
    dictionary = corpora.Dictionary.load('kejso_words.dict')
    #load model
    tfidf = models.TfidfModel.load('kejso_tfidf_model.model')

    texts, tag_list = load_texts()
    kws = load_kws()
    bow_t = [dictionary.doc2bow(text) for text in texts]
    bow_k = [dictionary.doc2bow(kw) for kw in kws]
    text_tfidf = [tfidf[bow] for bow in bow_t]
    kw_tfidf = [tfidf[bow] for bow in bow_k]
    return text_tfidf, kw_tfidf, dictionary, tag_list

def load_texts():
    t1, t3, t4, t5 = load_file("1.txt"), load_file("3.txt"), load_file("4.txt"), load_file("5.txt")
    t6, t7, t8, t9 = load_file("6.txt"), load_file("7.txt"), load_file("8.txt"), load_file("9.txt")
    t10, t11, t12, t13 = load_file("10.txt"), load_file("11.txt"), load_file("12.txt"), load_file("13.txt")
    tag_list = [0]*len(t1) + [1]*len(t3) + [2]*len(t4) + [3]*len(t5) + \
                [4]*len(t6) + [5]*len(t7) + [6]*len(t8) + [7]*len(t9) + \
                [8]*len(t10) + [9]*len(t11) + [10]*len(t12) + [11]*len(t13)
    texts = t1 + t3 + t4 + t5 + t6 + t7 + t8 + t9 + t10 + t11 + t12 + t13
    return texts, tag_list

def load_kws():
    t1, t3, t4, t5 = load_file("1_kw.txt"), load_file("3_kw.txt"), load_file("4_kw.txt"), load_file("5_kw.txt")
    t6, t7, t8, t9 = load_file("6_kw.txt"), load_file("7_kw.txt"), load_file("8_kw.txt"), load_file("9_kw.txt")
    t10, t11, t12, t13 = load_file("10_kw.txt"), load_file("11_kw.txt"), load_file("12_kw.txt"), load_file("13_kw.txt")
    kws = t1 + t3 + t4 + t5 + t6 + t7 + t8 + t9 + t10 + t11 + t12 + t13
    return kws








