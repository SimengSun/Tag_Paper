#coding: utf-8
__author__ = 'ssm'

import numpy as np
import datetime
import okm_local

from sklearn.manifold import TSNE
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def norm_vec(v):
    return (v+.0)/np.linalg.norm(v)

dwords = np.load("kejso_wv_filter_60.npy", encoding="latin1").item()
words = list(dwords.keys())
vecs = list(dwords.values())

#tsne = TSNE(perplexity=30,n_components=2,init='pca',n_iter=1000)


'''
centroids = [dwords[u'常微分方程'],
             dwords[u'原子'],
             dwords[u'硝酸'],
             #dwords[u'地震波'],
             dwords[u'进化'] ,
             dwords[u'人格'],
             dwords[u'土壤水分'],
             dwords[u'血液循环'],
             #dwords[u'阿霉素'],
             dwords[u'应用程序'],
             dwords[u'无线电'],
             dwords[u'城市污水'],
             #dwords[u'土壤污染'],
             dwords[u'纳米材料'],
             dwords[u'房屋建筑'],
             dwords[u'宏观经济'],
             dwords[u'重大事件'],
             #dwords[u'政治体制'],
             #dwords[u'司法'],
             #dwords[u'人口统计'],
             dwords[u'高等教育'],
             dwords[u'小说'],
             #dwords[u'文明史'],
             #dwords[u'图书资料']
             ]
'''

'''
centroids = [dwords[u'重金属离子'],  #化学、化学工艺与材料
             dwords[u'刚度'],   #工程技术相关
             dwords[u'变频'],   #电子
             dwords[u'机器学习'], #计算机
             dwords[u'经济效益'], #经济
             dwords[u'管理'],    #政治相关
             dwords[u'高等教育'], #教育
             dwords[u'软组织损伤'], #医学
             dwords[u'麝香保心丸'], #药
             dwords[u'城市污水'], #地理地质、种植、环境
             dwords[u'组织培养'], #生物
             dwords[u'微分方程'], #理论学科
             dwords[u'文化']  # 人文学科
             ]
'''

centroids = np.load("cent_vecs.npy")

k = len(centroids)

tagged, centroids, dist_to_centroid = okm_local.oskm_constrained(vecs,k,centroids,[],[],
                                              iter_num=35,init_a=0.5)

emb_clusters = []
word_clusters = []
select_vecs = []

for j in range(k):
    label_index = [i for i in range(len(tagged)) if tagged[i] == j]
    dists = [dist_to_centroid[i] for i in label_index]
    dists_sorted = sorted([(label_index[i], dists[i]) for i in range(len(dists))], key=lambda a: a[1],reverse=True)
    with open("afkmcmc_60_"+str(j)+".txt", "w") as f:
        a = (sum([d[1] for d in dists_sorted[:int(len(dists_sorted)/3)]]) + .0)/(len(dists_sorted)/3)
        f.write(str(a) + '\n')
        for d in dists_sorted[:]:
            f.write(str(words[d[0]]))
            f.write('\n')
    # for visualize
    labels = [words[d[0]] for d in dists_sorted[:int(len(label_index)/2)]]
    #low_emb = [embeddings[d[0]] for d in dists_sorted[:len(label_index)/2]]
    select_vecs.append([vecs[i] for i in label_index[:int(len(label_index))]])
    word_clusters.append(labels)
'''
new_vecs = []
for vec in select_vecs:
    new_vecs += vec
embeddings = tsne.fit_transform(new_vecs)
l = 0
for i in range(len(select_vecs)):
    emb_clusters.append([embeddings[j] for j in range(l, l + len(select_vecs[i]))])
    l += len(select_vecs[i])


plotvecs.plot_clusters(emb_clusters, word_clusters, annotate=False)
'''
np.save("centroids", centroids)
