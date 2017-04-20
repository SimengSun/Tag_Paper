#coding: utf-8
__author__ = 'ssm'

import numpy as np
import afk_mcmc as amc

dwords = np.load("D:\\Codes\\TagPaper\\cluster\\vecs\\kejso_wv_filter_60.npy").item()
words = list(dwords.keys())
vecs = list(dwords.values())

k = 14
m = 20

cinit = dwords[u'文学']
cinit_index = words.index(u'文学')
C, Ci = amc.assumption_free_kmcmc(vecs, k, m, cinit=cinit, cinit_index=cinit_index)

with open("centroids.txt", "w") as f:
    for i in Ci:
        f.write(words[i].encode('utf-8') + "\n")
np.save("cent_vecs",C)