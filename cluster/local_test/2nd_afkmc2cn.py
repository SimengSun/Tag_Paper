#coding: utf-8
__author__ = 'ssm'

'''
test afkmc2_cluster_number for subject tree 2nd level
'''

import numpy as np
import datetime
import afk_mcmc_cluster_number as afkmc2cn

dwords = np.load("vecs.npy").item()
'''
words = list(dwords.keys())
vecs = list(dwords.values())

'''
words = []

with open("D:\\Codes\\TagPaper\\cluster\\clusters\\filter_60_afkmcmc"+
          "\\afkmcmc_60_2.txt") as f:
    lines = f.readlines()
    words += map(lambda a: a.strip(), lines[1: -len(lines)/3])

vecs = []
for i in words:
    vecs.append(dwords[i.decode('utf-8')])


for pick in [80]:
    time1 = datetime.datetime.now()
    k, labels, word_index = afkmc2cn.afkmc2_cluster_number_ap(vecs, [], 10, pick)
    time2 = datetime.datetime.now()
    print pick, k
    print time2 - time1
    with open("test" + str(pick) + ".txt", "w") as f:
        for li in range(len(labels)):
            ws = [word_index[i] for i in range(len(labels)) if labels[i] == li]
            #if len(ws) < 3:
            #    continue
            for wi in ws:
                f.write(words[wi] + '\n')
            f.write('\n')



