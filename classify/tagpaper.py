__author__ = 'ssm'

import extract_keyword as ek
import area_score as ars
import Util
import numpy as np
import redis
from sklearn.metrics import recall_score, accuracy_score, f1_score

#load paper & tfidf & kw
#dic {(1, w1),(2, w2)..}

text_tfidf, kw_tfidf, dic, tags = Util.load_data()

#redis
r = redis.StrictRedis(host='10.2.1.7', port=6379, db=0)

#load centroids
centroids = np.load('centroids.npy')
#centroids = [centroids[1]] + centroids[3:]

predicts = []
#predict each paper
for i in range(len(text_tfidf)):
    #sorted tfidf
    sorted_text_tfidf = sorted(text_tfidf[i], key=lambda a: a[1], reverse=True)
    sorted_kw_tfidf = sorted(kw_tfidf[i], key=lambda a: a[1], reverse=True)
    #extract keywords & generate weights
    wordvecs, weights, kw = ek.extract_kw(r, dic, dict(sorted_text_tfidf[:20]), dict(sorted_kw_tfidf), centroids,
                                      degree_diff_mode="variance")

    #predict class
    record = ars.area_score(wordvecs,weights,centroids)
    c_index = record[0][0]
    '''
    if (c_index != tags[i]) & (i > 1300):
        print("index {}, predict {}, actually {}".format(i, c_index, tags[i]))
        print(record)
        print("extracted keywords:{}".format(kw))
        print("keywords weight:{}".format(weights))
    '''
    predicts.append(c_index)
    if i % 100 == 0:
        print("end process {}".format(i))

#print result
for i in range(12):
    print("{}\n".format(i))
    print("predicts {}\n".format(predicts[i*100:(i+1)*100]))

#score result
acc = accuracy_score(tags, predicts)
rec = recall_score(tags, predicts, average='macro')
f1 = f1_score(tags, predicts, average='macro')
print(acc)
print(rec)
print(f1)