__author__ = 'ssm'

import numpy as np
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_distances

'''
input: keywords + weights + centroids
output: the possible area (index of centroids)

for each kw:
	for each centroid:
		get dist(kw, centroid)
		dist -> score
		record += weight * score
'''

def softmax_score(l):
    return np.exp(l) / np.sum(np.exp(l), axis=0)

def transform(base, d, roof, r):
    return (roof-d)/(r*base)

def calculate_scores(distances):
    r = 1#0.5
    base = distances[0][1]
    delta_list = [d-base for (i,d) in distances]
    roof = delta_list[-1]
    final = [transform(base, d, roof, r) for d in delta_list]
    #print("final {}".format(final))
    return softmax_score(final)

def get_scores(vec, centroids):
    dist = []
    for idx, c in enumerate(centroids):
        #dis = np.linalg.norm(np.array(vec)-np.array(c))
        dis  = cosine_distances([vec], [c])
        dist.append((idx, dis))
    sorted_dis = sorted(dist, key=lambda a: a[1])
    top_dis = sorted_dis[:5]
    #print("top dis {}".format(top_dis))
    scores = calculate_scores(top_dis)
    indices = [i for (i,d) in top_dis[:len(scores)]]
    #print("scores {}".format(scores))

    return list(scores), indices

def area_score(vecs, weights, centroids):
    '''
    :param vecs: keyword vecs
    :param weights: weights
    :param centroids: centroids
    :return: centroid index
    '''
    record = defaultdict(float)
    for vi in range(len(vecs)):
        #get scores of vi to nearest m centroids
        scores, indices = get_scores(vecs[vi], centroids)
        if scores is None:
            continue
        for idx in range(len(scores)):
            record[indices[idx]] += weights[vi]*scores[idx]
    sorted_record = sorted(record.items(), key=lambda a:a[1], reverse=True)
    #print("record {}".format(record))
    #print("weights {}".format(weights))
    #exit()
    return sorted_record
