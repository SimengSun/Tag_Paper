#coding: utf-8
__author__ = 'ssm'

import numpy as np
import datetime
from sklearn.cluster import AffinityPropagation, KMeans
from sklearn.metrics.pairwise import cosine_similarity
import Util
import redis

#redis
r = redis.StrictRedis(host='10.2.1.7', port=6379, db=0)


#get 1st subject words
words = Util.cluster_2nd_load_1st_words("")
#get vecs
vecs = Util.cluster_2nd_load_1st_vecs(r, words)

print len(vecs)

def test_ap_clustering(wrds):
    words = wrds[:-len(wrds)/5]
        #get similarities
    similarities = [[0 for i in range(len(words))] for j in range(len(words))]
    for ci in range(len(words)):
        for cj in range(ci, len(words)):
            similarities[ci][cj] = cosine_similarity([vecs[ci]], [vecs[cj]])[0][0]
            similarities[cj][ci] = similarities[ci][cj]
        if ci % 100 == 0:
            print 'end ', ci, ' ', datetime.datetime.now()
        #get preference
    pre = np.median(similarities)
    print 'end inits ', datetime.datetime.now()
    apmodel = AffinityPropagation(affinity="precomputed", preference=pre/1000)
    ap = apmodel.fit(similarities)
    print 'end fit ', datetime.datetime.now()
    centers_indices = ap.cluster_centers_indices_
    labels = ap.labels_
    centers_similarity_mat = [[0 for i in range(len(centers_indices))] for j in range(len(centers_indices))]
    for i in range(len(centers_indices)):
        for j in range(len(centers_indices)):
            centers_similarity_mat[i][j] = similarities[centers_indices[i]][centers_indices[j]]

    cluster_num = len(centers_indices)
    clusters_index = []
    for i in range(cluster_num):
        label_index = [li for li in range(len(labels)) if labels[li] == i]
        clusters_index.append(label_index)
        with open(".\\clusters\\subject_name\\ap_" + str(i) + ".txt", "w") as f:
            for j in label_index:
                f.write(words[j].encode('utf-8') + '\n')

    return centers_indices, labels, clusters_index, centers_similarity_mat

#kmeans + ap clustering
def test_km(words, centers_indices, clusters_index, center_s_mat):
    km = KMeans(n_clusters=3, precompute_distances=True)
    centers = [vecs[i] for i in centers_indices]
    #km_f = km.fit(center_s_mat)
    km_f = km.fit(centers)
    new_centers = km_f.cluster_centers_

    for i in range(3):
        tmp_list = []
        for j in range(len(clusters_index)):
            if km_f.labels_[j] == i:
                tmp_list.append(clusters_index[j])
        with open(".\\clusters\\subject_name\\ap_km_"+str(i)+".txt", "w") as f:
            for wlist in tmp_list:
                for w in wlist:
                    f.write(words[w].encode('utf-8') + '\n')
        print 'end ', i, ' ', datetime.datetime.now()
    np.save(".\\clusters\\subject_name\\centers", new_centers)


center_indices, labels, clusters_index, c_s_mat = test_ap_clustering(words)