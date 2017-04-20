__author__ = 'ssm'

import numpy as np

path = './iter_40_2nd/iter_40_afkmcmc_60_'

centroids = []

s1 = np.load("iter_40_centroids.npy")
for i in range(14):
    s2 = np.load(path + str(i) + '/afk_centers.npy')
    centroids.append((s1[i], s2))
np.save("subject_tree", centroids)