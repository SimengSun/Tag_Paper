#coding:utf-8
__author__ = 'ssm'

import jieba
import json

'''
GET PARSED AND FILTERED PEOPLE INFORMATION

with open("peoplea.json", "r") as f:
    parsed = json.load(f, strict=False)
text = []

#jieba.load_userdict("D:\\Codes\\TagPaper\\cluster\\data\\keywordrank.txt")

for it in parsed:
    tmp = it['academy'] + it['project'] + it['experience']
    tmp = filter(lambda a: a not in ',.>-:()（）!@#$%^&*~{}|；;：:"“’‘”。，《'
                                    '》？|】【、>_=/+1234567890abcdefghi'
                                    'jklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.decode(encoding='utf-8'), tmp)
    tlist = list(jieba.cut(tmp, cut_all=False))
    text.append(tlist)

with open("tmp_test.txt", "w") as f:
    for li in range(len(text)):
        if len(text[li]) == 0:
            continue
        for ii in range(len(text[li])):
            f.write(text[li][ii].encode('utf-8'))
        f.write('\n')
'''
# use ansj seg words

# statistic words
dic = {}

with open("other_seg.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        sp = line.split(" ")
        for word in sp:
            if dic.has_key(word):
                dic[word] += 1
            else:
                dic[word] = 1

sort_dict = sorted(dic.items(), key=lambda a: a[1], reverse=True)
with open("stopwords", "w") as f:
    for word in sort_dict[:1000]:
        f.write(word[0])
        f.write('\n')

'''
from gensim.corpora import Dictionary
import gensim
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

with open("tmp_test.txt", "r") as f:
    lines = f.readlines()
    slist = []
    for line in lines:
        slist.append(line.split(' '))
    dic = Dictionary(slist)
    corp = [dic.doc2bow(text) for text in slist]
    tfidf = gensim.models.TfidfModel(corpus=corp, dictionary=dic)
    #idfs = tfidf.idfs.items()
    #idfs = sorted(idfs, key=lambda a: a[1])
    with open("stopwords", "w") as sf:
        for li in range(len(idfs)*3/4):
            sf.write(dic[idfs[li][0]].encode('utf-8'))
            sf.write('\n')

'''