#coding: utf-8
__author__ = 'ssm'

import oskm_redis
import redis
import numpy as np
import Util
from Util import get_vec

#redis
r = redis.StrictRedis(host='10.2.1.7', port=6379, db=0)

#get keywords
keywords = Util.get_keywords(r)

# centroids selection based on category_!

centroids = [get_vec(u'数学分析'),
             get_vec(u'量子光学'),
             get_vec(u'硝酸'),
             get_vec(u'地震波'),
             get_vec(u'基因') ,
             get_vec(u'人格'),
             get_vec(u'土壤水分'),
             get_vec(u'血液循环'),
             get_vec(u'阿霉素'),
             get_vec(u'应用程序'),
             get_vec(u'通信协议'),
             #get_vec(u'再生能源'),
             #get_vec(u'土壤污染'),
             get_vec(u'纳米材料'),
             #get_vec(u'石油勘探'),
             #get_vec(u'冶金'),
             get_vec(u'建筑'),
             get_vec(u'刀具'),
             get_vec(u'水利工程'),
             get_vec(u'交通'),
             get_vec(u'仪器'),
             get_vec(u'宏观经济'),
             get_vec(u'人力资源'),
             #get_vec(u'政治体制'),
             #get_vec(u'司法'),
             #get_vec(u'人口统计'),
             get_vec(u'高等教育'),
             get_vec(u'文学作品'),
            ]

#centroids = [get_vec(u'细胞'),get_vec(u'教学')]

k = len(centroids)

print("start cluster..")
tagged, centroids, dist_to_centroid = oskm_redis.okm(r,k,centroids,
                                                     keywords, iter_num=25,init_a=0.5)
print(len(tagged))
for j in range(k):
    label_index = [i for i in range(len(tagged)) if tagged[i] == j]
    print(len(label_index))
    dists = [dist_to_centroid[i] for i in label_index]
    dists_sorted = sorted([(label_index[i], dists[i]) for i in range(len(dists))], key=lambda a: a[1],reverse=True)
    f = open(".\\clusters\\c_"+str(j)+".txt", "w")
    for i in label_index:
        #print(keywords[i])
        f.write(keywords[i].encode('utf-8') + '\n')
    f.close()

np.save("centroids", centroids)