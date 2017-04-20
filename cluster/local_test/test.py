from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import numpy as np


import  time
t1 = time.time()
for i in range(1000):
    a = i ** 2
t2 = time.time()
print t1
print t2
print t2-t1