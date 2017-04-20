__author__ = 'ssm'

'''
test 2nd level clustering
1. afk_mcmc + k_means
2. ap + k_means

record (time, accuracy(distance to centroid))
'''

import numpy as np
import datetime
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AffinityPropagation, KMeans
import afk_mcmc as afkmc2


dwords = np.load("vecs.npy").item()
total_words = list(dwords.keys())
total_vecs = list(dwords.values())

path = "./iter_70/"


def afk_mcmc_and_kmeans(vecs, words, k, m, fn):
    #start time
    st = datetime.datetime.now()

    #afk mcmc
    centers, center_index = afkmc2.assumption_free_kmcmc(vecs, k, m)
    km_model = KMeans(n_clusters=k, init="k-means++")
    km = km_model.fit(vecs)
    f_centers = km.cluster_centers_
    labels = km.labels_

    #end time
    et = datetime.datetime.now()

    #calculate time
    print("{} afkmcm  time {}".format(fn, et-st))

    #write to files
    for i in range(k):
        tmp_label = [li for li in range(len(labels)) if labels[li] == i]
        dist = [cosine_similarity([vecs[vi]], [f_centers[i]]) for vi in tmp_label]
        dist = sorted(zip(tmp_label, dist), key=lambda a: a[1], reverse=True)
        if not os.path.exists("./iter_70_2nd/iter_70_" + fn):
            os.mkdir("./iter_70_2nd/iter_70_" + fn)
        with open("./iter_70_2nd/iter_70_" + fn + "/afk_60_" + str(i) + ".txt", "w") as f:
            a = (sum([d[1] for d in dist[:int(len(dist)/3)]])+.0) / (len(dist)/3)
            f.write(str(a) + '\n')
            for d in dist:
                f.write(words[d[0]] + '\n')
        #save centers
        np.save("./iter_70_2nd/iter_70_" + fn + "/afk_centers", f_centers)

#k = 7
m = 25
pick = 55

import afk_mcmc_cluster_number as afkmc2cn

def test():

    files = os.listdir(path)
    for file in files:
        with open(path+file, "r") as f:
            #prepare data
            words = f.readlines()
            words = list(map(lambda a: a.strip(), words[1:]))
            vecs = []
            for w in words:
                vecs.append((dwords[w]+.0))

            k, _, _ = afkmc2cn.afkmc2_cluster_number_ap(vecs, m, pick)
            #test ap+km
            #ap_and_kmeans(vecs, words, k, file.strip(".txt"))
            #test afk_mcmc+km
            afk_mcmc_and_kmeans(vecs, words, k, m, file.strip(".txt"))


test()