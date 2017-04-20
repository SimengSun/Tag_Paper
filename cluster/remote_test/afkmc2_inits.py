__author__ = 'ssm'

import numpy as np
import afk_mcmc as amc

wv = np.load("vecs.npy").item()
words = list(wv.keys())
vecs = list(wv.values())

k = 14
m = 20

cinit = wv[words[1]]
cinit_index = words.index(words[1])
C, Ci = amc.assumption_free_kmcmc(vecs, k, m, cinit=cinit, cinit_index=cinit_index)

for i in Ci:
    print(words[i])

np.save("akfmc2_init_vecs",C)