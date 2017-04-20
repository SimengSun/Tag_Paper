__author__ = 'ssm'


from sklearn.manifold import TSNE
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

dwords = np.load("vecs.npy").item()
words = list(dwords.keys())
vecs = list(dwords.values())

def plot_clusters(emb_clusters,  count):
    cmap = cm.get_cmap('rainbow', 20)
    colors = cmap(np.linspace(0, 1, len(emb_clusters)))
    plt.figure(figsize=(18, 18))
    for i in range(len(emb_clusters)):
        for j in range(len(emb_clusters[i])):
            x, y= np.array(emb_clusters[i])[j,:]
            plt.scatter(x, y, c=colors[i])
        plt.savefig('./skm_iter_70_plot/' + str(count) + '_' + str(i) + '.png')

path = './skm_iter_70_2nd/iter_70_'
import os
tsne = TSNE(perplexity=30,n_components=2,init='pca',n_iter=5000)
import datetime

for i in range(14):
    files = os.listdir(path + str(i))
    clusters = []
    for j in range(len(files)-1):
        with open(path + str(i) + '/afk_' + str(j), "r") as f:
            lines = f.readlines()
            tmp = []
            for line in lines[1:]:
                tmp.append(dwords[line.strip()])
        low_emb = tsne.fit_transform(tmp)
        print("end pca i: {} j: {} at {}".format(i, j, datetime.datetime.now()))
        clusters.append(low_emb)
    plot_clusters(clusters,i)

