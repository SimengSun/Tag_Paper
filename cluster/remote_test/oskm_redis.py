__author__ = 'ssm'

from sklearn.metrics.pairwise import cosine_similarity
import datetime
import numpy as np

def okm(r, k, k_inits, words, iter_num=None, init_a=None):
    '''
    :param r: redis
    :param k: k
    :param k_inits: set init centroids (based on background knowledge)
    :param words: words used for clustering (must in redis)
    :param iter_num: default 10
    :param init_a: default 0.3
    :return: tagged_data, k centroids
    '''
    # assigned centroid index
    size = len(words)
    tagged_data = [0 for i in range(size)]
    # distance from assigned centroid last time
    data_last_dist = [-2 for i in range(size)]
    if iter_num is None:
        iter_num = 10
    if init_a is None:
        init_a = 0.3
    centroids = k_inits
    mn = iter_num*(size) # for update a
    flat_a = 0.05  # flat learning rate

    # iter begin
    t = 0 # 0 < t < mn
    count_cent = [0 for i in range(k)] # points assigned to each centroid
    remote_k = [1 for i in range(k)] # the remotest k (avoid empty cluster)
    remote_k_index = [0 for i in range(k)]
    for m in range(iter_num):
        #for n in range(size):
        n = 0
        for key in words:
            vec = np.fromstring(r.get(key),dtype=np.float32)
            # get closest centroid
            last = data_last_dist[n]
            index = tagged_data[n]
            for i in range(len(centroids)):
                tmp = cosine_similarity([vec], [centroids[i]])
                if tmp > last:
                    last = tmp
                    index = i
            # add remote point and its index
            if last < max(remote_k):
                i = remote_k.index(max(remote_k))
                remote_k.pop(i)
                remote_k_index.pop(i)
                remote_k.insert(i,last)
                remote_k_index.insert(i, n)
            tagged_data[n] = index
            data_last_dist[n] = last
            count_cent[index] += 1

            # update learning rate (exponentially decrease)
            a = init_a * ( ((flat_a + .0)/init_a)**((t+.0)/mn) )

            # update centroid
            '''
            if cosine_similarity([vec], [centroids[index]]) > 0.8:
                    centroids[index] = centroids[index] + a*(vec-centroids[index])
            else:
                    centroids[index] = centroids[index] + a*(vec-centroids[index])
            '''
            '''
            if cosine_similarity([centroids[index]],[k_inits[index]]) < 0.8: # add constraints to centroid
                centroids[index] = k_inits[index]
            '''
            centroids[index] = centroids[index] + a*(data[n]-centroids[index])
            n += 1
            t += 1
            if n % 100000 == 0:
                print('end {} {}'.format(n, datetime.datetime.now()))

        #avoid empty cluster
        for i in range(k):
            if count_cent[i] == 0:
                if len(remote_k) != 0:
                    index = remote_k.index(min(remote_k)) # get remotest distance index
                    centroids[i] = np.fromstring(r.get(words[remote_k_index[index]], dtype=np.float32))
                    tagged_data[remote_k_index[index]] = i
                    data_last_dist[remote_k_index[index]] = 0.
                    remote_k.pop(index)
                    remote_k_index.pop(index)

        print('end iter {}'.format(m))
    return tagged_data, centroids, data_last_dist
