#coding: utf-8
__author__ = 'ssm'

import numpy as np
import datetime
import random

def norm_vec(v):
    return (v+.0)/np.linalg.norm(v)


from sklearn.manifold import TSNE
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def plot_clusters(emb_clusters, word_clusters, annotate=False):
    cmap = cm.get_cmap('rainbow', 20)
    colors = cmap(np.linspace(0, 1, len(emb_clusters)))
    plt.figure(figsize=(18, 18))
    for i in range(len(emb_clusters)):
        for j, label in enumerate(word_clusters[i]):
            x, y= np.array(emb_clusters[i])[j,:]
            plt.scatter(x, y, c=colors[i])
            if annotate == True:
                plt.annotate(label,
                    xy=(x, y),
                    xytext=(5, 2),
                    textcoords='offset points',
                    ha='right',
                    va='bottom')
            plt.savefig('.\\clutsers\\test_' + str(i) + '.png')

def plot_with_labels(low_dim_embs, labels, filename='tsne.png'):
    assert low_dim_embs.shape[0] >= len(labels), "More labels than embeddings"
    plt.figure(figsize=(18, 18))  #in inches
    for i, label in enumerate(labels):
        x, y = low_dim_embs[i,:]
        plt.scatter(x, y)
        plt.annotate(label,
                 xy=(x, y),
                 xytext=(5, 2),
                 textcoords='offset points',
                 ha='right',
                 va='bottom')

    plt.savefig(filename)


dwords = np.load("D:\\Codes\\TagPaper\\cluster\\vecs\\kejso_wv_filter_400.npy").item()
words = dwords.keys()
vecs = dwords.values()

index = random.sample(range(len(words)),800)
words_f = [words[i] for i in index]
#vecs_f = [vecs[i] for i in index]

with open(".\\local_version\\centroids.txt", "r") as f:
    lines = f.readlines()
    words = map(lambda a: a.strip().decode('utf-8'), lines)

words_f += words
vecs_f = []
for word in words_f:
    vecs_f.append(dwords[word])


tsne = TSNE(perplexity=30,n_components=2,init='pca',n_iter=2000)
low_dim_embs = tsne.fit_transform(vecs_f)

#plot_with_labels(low_dim_embs,words_f)



plot_with_labels(low_dim_embs[-len(words):],words_f[-len(words):], filename='centers_50')
plot_with_labels(low_dim_embs[-500:],words_f[-500:], filename='total')

