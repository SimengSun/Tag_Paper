__author__ = 'ssm'

import afk_mcmc_cluster_number as afkmc2cn
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np
import time
import datetime
from sklearn.metrics.pairwise import euclidean_distances


def prepare_data(samples, feature, cluster_number):
    x, y = make_blobs(samples, feature, cluster_number)
    return x, y

def afkmc2(x, chainlen, pick):
    time1 = time.time()
    #k, labels, index = afkmc2cn.afkmc2_cluster_number_ap(x, chainlen, pick)
    sorted_dict_count = afkmc2cn.afkmc2_ap_test_iter_d(x, chainlen, pick, 100)
    time2 = time.time()
    #return k, time2-time1
    return sorted_dict_count


from sklearn.cluster import KMeans

def km(x):
    time1 = time.time()
    for k in range(2,14):
        km = KMeans(n_clusters=k)
        km_fit  =km.fit(np.array(x))
        labels = km_fit.labels_
        centers =  km_fit.cluster_centers_
        for ci in range(k):
            err = 0
            idx = [i for i in range(len(x)) if labels[i] == ci]
            for i in idx:
                err += euclidean_distances([centers[ci]], [x[i]])
        print datetime.datetime.now()
    time2 = time.time()
    return time2-time1

def test_time(samples, features, cluster_numbers, chainlen, pick):
    t_afk = []
    t_km = []

    for sample in samples:
        x, y = prepare_data(sample, features, cluster_numbers)
        k, t1 = afkmc2(x, chainlen, pick)
        t2 = km(x)
        t_afk.append(t1)
        t_km.append(t2)
    xi = range(len(samples))
    xticks = samples
    print t_afk, t_km
    plt1 = plt.plot(xi, t_afk, '-+r')
    plt2 = plt.plot(xi, t_km, '-+g')
    plt.title('Time')
    plt.legend(['AFKMC2', 'KMEANS'])
    plt.xticks(xi, xticks)
    plt.show()

def test_correctness(samples, features, cluster_numbers, chainlen, picks):
    correctness = []
    pi = 0
    for sample in samples:
        x, y = prepare_data(sample, features, cluster_numbers)
        dict_count = afkmc2(x, chainlen, picks[pi])
        #print(k)
        pi += 1
        #correct_rate = (predict_k.count(8) + .0) / len(predict_k)
        #correctness.append(correct_rate)
        #print("sample count {} crrct rate {}".format(sample, correct_rate))
        print("sampe {} dict count {}".format(sample, dict_count))





#samples = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]
samples = [2000, 5000, 7000]
feature = 2
cluster_num = 8
chainlen = 20
pick = 80
picks = [80, 100, 120]
#test_time(samples, feature, cluster_num, chainlen, pick)

test_correctness(samples, feature, cluster_num, chainlen, picks)

'''
x, y = prepare_data(10000, feature, cluster_num)

#visualize
colors = [(np.random.uniform(), np.random.uniform(), np.random.uniform()) for i in range(cluster_num)]

print("start scattering")

plt.figure(figsize=(8, 8))
for col_id in range(len(colors)):
    y_id = [i for i in range(len(y)) if y[i] == col_id]
    x_ = [x[i][0] for i in range(len(x)) if i in y_id]
    y_ = [x[i][1] for i in range(len(x)) if i in y_id]
    plt.scatter(x_, y_, c = colors[col_id], marker='o')
    print("end process {}  at {}".format(col_id, datetime.datetime.now()))

plt.show()
'''
