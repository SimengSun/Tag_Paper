#coding: utf-8
__author__ = 'ssm'

import numpy as np
import datetime
import clustering
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances
import sys

def norm_vec(v):
    return (v+.0)/np.linalg.norm(v)

def cosine_distance(v1, v2):
    return cosine_distances([v1], [v2])[0][0]
def euclidean_distance(v1, v2):
    return euclidean_distances([v1],[v2])[0][0]

dwords = np.load("vecs.npy").item()
words = list(dwords.keys())
vecs = list(dwords.values())

centroids = np.load("afkmc2_init_vecs.npy")

k = len(centroids)

tagged, centroids, dist_to_centroid = clustering.sequential_kmeans(vecs,k,centroids,iter_num=50,init_a=0.9)

for j in range(k):
    label_index = [i for i in range(len(tagged)) if tagged[i] == j]
    dists = [dist_to_centroid[i] for i in label_index]
    dists_sorted = sorted([(label_index[i], dists[i]) for i in range(len(dists))], key=lambda a: a[1],reverse=True)
    with open("./cmp_iter_50/afkmcmc_50_"+str(j)+".txt", "w") as f:
        #calculate silhouette coefficient of centroid
            # a(o)
        euclidean_a_centroid = 0
        for li in label_index:
            euclidean_a_centroid += euclidean_distance(centroids[j], vecs[li])
        euclidean_a_centroid /= len(label_index)
            # b(o)
        euclidean_b_centroid = sys.maxint
        for ki in range(k):
            if ki == j:
                continue
            li_list = [i for i in range(len(tagged)) if tagged[i] == j]
            euclidean_dist = 0
            for li_id in li_list:
                euclidean_dist += euclidean_distance(centroids[j], vecs[li_id])
            euclidean_dist /= len(li_list)
            if euclidean_dist < euclidean_b_centroid:
                euclidean_b_centroid = euclidean_dist
        euclidean_s_centroid = (euclidean_b_centroid - euclidean_a_centroid + .0)/max(euclidean_b_centroid
                                                                                      , euclidean_a_centroid)
        # my defined a
        a = (sum([d[1] for d in dists_sorted[:int(len(dists_sorted)/3)]]) + .0)/(len(dists_sorted)/3)
        f.write(str(euclidean_s_centroid) + '\t' + str(a) + '\n')
        for d in dists_sorted[:]:
            f.write(str(words[d[0]]))
            f.write('\n')

np.save("./cmp_iter_50/centroids", centroids)
