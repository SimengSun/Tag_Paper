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
total_words = dwords.keys()
total_vecs = dwords.values()

path = "D:\\Codes\\TagPaper\\cluster\\clusters\\filter_60_afkmcmc\\"


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
        with open("D:\\Codes\\TagPaper\\cluster\\clusters\\" + fn + "\\afk_60_" + str(i) + ".txt", "w") as f:
            a = (sum([d[1] for d in dist[:len(dist)/3]])+.0) / (len(dist)/3)
            f.write(str(a) + '\n')
            for d in dist:
                f.write(words[d[0]].encode('utf-8') + '\n')
        #save centers
        np.save("D:\\Codes\\TagPaper\\cluster\\clusters\\" + fn + "\\afk_centers", f_centers)


def ap_and_kmeans(vecs, words, k, fn):
    #start time
    st = datetime.datetime.now()

    #delete less relevant words
    dvecs, dwords = vecs[:-len(vecs)/5], words[:-len(words)/5]

    #similarity
    similarities = [[0 for i in range(len(dwords))] for j in range(len(dwords))]
    for ci in range(len(dwords)):
        for cj in range(len(dwords)):
            similarities[ci][cj] =cosine_similarity([dvecs[ci]], [dvecs[cj]])[0][0]
            similarities[cj][ci] = similarities[ci][cj]
        if ci % 1000 == 0:
            print('end {} {}'.format(ci, datetime.datetime.now()))

    #set preference = median
    pre = np.median(similarities)

    #init model and fit
    ap_model = AffinityPropagation(affinity="precomputed", preference=pre/1000)
    ap = ap_model.fit(similarities)
    centers_indices = ap.cluster_centers_indices_
    labels = ap.labels_

    #center(ap clustering result) similarity matrix (for kmeans clustering)
    c_s_m = [[0 for i in range(len(centers_indices))] for j in range(len(centers_indices))]
    for i in range(len(centers_indices)):
        for j in range(len(centers_indices)):
            c_s_m[i][j] = similarities[centers_indices[i]][centers_indices[j]]

    #store sample by cluster
    ap_clusters_indices = []
    for i in range(len(centers_indices)):
        label_index = [li for li in range(len(labels)) if labels[li] == i]
        ap_clusters_indices.append(label_index)

    #kmeans
    km_model = KMeans(n_clusters=k, precompute_distances=True)
    km = km_model.fit(c_s_m)
    f_centers = km.cluster_centers_ # final centers
    et = datetime.datetime.now()

    #calculate time
    print("{} ap consumed time {}".format(fn, et-st))

    #write 2 file
    for i in range(k):
        tmp_list = []
        for j in range(len(ap_clusters_indices)):
            if km.labels_[j] == i:
                tmp_list += ap_clusters_indices[j]
        #calculate mass means
        tmp_vecs = [dvecs[i] for i in tmp_list]
        md = np.mean(tmp_vecs, axis=0)
        #calculate distance
        dist = map(lambda a: cosine_similarity([a], [md]), tmp_vecs)
        dist = sorted(zip(tmp_list, dist), key=lambda a: a[1], reverse=True)
        with open("D:\\Codes\\TagPaper\\cluster\\clusters\\" + fn + "\\ap_" + str(i) + ".txt", "w") as f:
            # top one third mean similarities
            a = (sum([d[1] for d in dist[:len(dist)/3]])+.0) / (len(dist)/3)
            f.write(str(a) + '\n')
            for d in dist:
                f.write(dwords[d[0]].encode('utf-8') + '\n')
    #save centers
    np.save("D:\\Codes\\TagPaper\\cluster\\clusters\\" + fn + "\\ap_centers", f_centers)


#k = 7
m = 20
pick = 50

import afk_mcmc_cluster_number as afkmc2cn

def test():

    files = os.listdir(path)
    for file in files:
        with open(path+file, "r") as f:
            #prepare data
            words = f.readlines()
            words = map(lambda a: a.strip().decode('utf-8'), words[1:])
            vecs = []
            for w in words:
                vecs.append((dwords[w]+.0))

            k, _, _ = afkmc2cn.afkmc2_cluster_number_ap(vecs, [], m, pick)
            #test ap+km
            #ap_and_kmeans(vecs, words, k, file.strip(".txt"))
            #test afk_mcmc+km
            afk_mcmc_and_kmeans(vecs, words, k, m, file.strip(".txt"))


test()