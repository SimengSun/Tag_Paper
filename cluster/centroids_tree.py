__author__ = 'ssm'

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


centroids = []
s1 = np.load(".\\clusters\\centroids.npy")
for i in range(14):
    s2 = np.load(".\\clusters\\afkmcmc_60_" + str(i) + "\\afk_centers.npy")
    centroids.append((s1[i], s2))
np.save("subject_tree", centroids)
