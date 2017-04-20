__author__ = 'ssm'

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import redis

'''
input : paper's [title, keywords, abstract], centroids
output: key phrases + weights

1.[title, abstract] (input:sorted by tfidf, pick top 10)
  [keywords] if available
  [title, abstract] | [keywords]

2. add weights
	-is domain words(see 3.)
		-kw
		-extracted
	-not domain words
		-kw
		-extracted

3. is w a domain word?
	variance to all centroids
	cosine similarity
'''

def get_vec(r, s):
    return np.fromstring(r.get(s),dtype=np.float32)

def cal_degree_diff(vec, centroids, degree_diff="variance"):
    '''
    degree_diff(ordinary word) < degree_diff(domain word)
    '''
    wordvec = np.array(vec)
    if degree_diff == "variance":
        vr = 0
        for c in centroids:
            vr += np.linalg.norm(np.array(c)-wordvec)**2
        return vr
    elif degree_diff == "cosine":
        trend_num = 0
        for c in centroids:
            if cosine_similarity([vec], [c]) > 0.5:
                trend_num += 1
        return len(centroids) - trend_num

def get_domainwords(sorted_degree):
    # if dd[i] > (dd[i-2] dd[i-1]  dd[i+1] dd[i+2]) then [:i] is domain words
    tmp = [] # sd[n-1] - sd[n]
    for i in range(len(sorted_degree)-1):
        tmp.append(sorted_degree[i][1] - sorted_degree[i+1][1])
    if len(sorted_degree) < 5:
        return [i for (i, d) in sorted_degree]
    t = 0
    for i in range(2, len(tmp)-2):
        if (tmp[i] > tmp[i-1]) & (tmp[i] > tmp[i-2]) & (tmp[i] > tmp[i+1])\
                & (tmp[i] > tmp[i+2]):
            t = i
            break
    if t == 0:
        return [w for (w, v) in sorted_degree]
    else:
        return [w for (w, v) in sorted_degree[:t]]

def init_data(r, dic, tfidf_text, tfidf_kw):
    '''
    :param r: redis
    :param dic: kejso dictionary
    :param tfidf_text: tfidf text(title+abstract)
    :param tfidf_kw: tfidf keywords
    :return:
    '''
    tmp_dic = {}  #{id_in_dic:vec, ..}
    kwords_index = []
    for id in tfidf_text:
        #access redis
        if r.exists(dic[id]):
            vec = get_vec(r, dic[id])
            tmp_dic[id] = vec
    for id in tfidf_kw:
        #access redis
        if r.exists(dic[id]):
            vec = get_vec(r, dic[id])
            tmp_dic[id] = vec
            kwords_index.append(id)
    return tmp_dic, kwords_index

def group_words(domain_words, total_words_index, kwords_index):
    dk = []
    d_k = []
    _dk = []
    _d_k = []
    for i in range(len(total_words_index)):
        if total_words_index[i] in domain_words:
            if total_words_index[i] in kwords_index:
                dk.append(total_words_index[i])
            else:
                d_k.append(total_words_index[i])
        else:
            if total_words_index[i] in kwords_index:
                _dk.append(total_words_index[i])
            else:
                _d_k.append(total_words_index[i])
    return dk, d_k, _dk, _d_k

def get_degree_diffs(total_words_index, total_vecs, centroids, degree_diff_mode):
    degree_diff = []
    for i in range(len(total_words_index)):
        degree_diff.append((total_words_index[i],
                            cal_degree_diff(total_vecs[i], centroids, degree_diff=degree_diff_mode)))
    return degree_diff

def get_tfidf(ttext, tkw, idlist, type=None):
    if type == "max":
        max = 0
        for id in idlist:
            tmp = 0
            if (id in tkw.keys()) and (id in ttext.keys()):
                if tkw[id] > ttext[id]:
                    tmp = tkw[id]
                else:
                    tmp = ttext[id]
            elif (id in tkw.keys()) and (id not in ttext.keys()):
                tmp = tkw[id]
            elif (id not in tkw.keys()) and (id in ttext.keys()):
                tmp = ttext[id]
            elif (id not in tkw.keys()) and (id not in ttext.keys()):
                print('exist words that not existed')
            if max < tmp:
                max = tmp
        return max
    elif type == "min":
        min = 0
        for id in idlist:
            tmp = 0
            if (id in tkw.keys()) and (id in ttext.keys()):
                if tkw[id] < ttext[id]:
                    tmp = tkw[id]
                else:
                    tmp = ttext[id]
            elif (id in tkw.keys()) and (id not in ttext.keys()):
                tmp = tkw[id]
            elif (id not in tkw.keys()) and (id in ttext.keys()):
                tmp = ttext[id]
            elif (id not in tkw.keys()) and (id not in ttext.keys()):
                print('exist words that not existed')
            if min < tmp:
                min = tmp
        return min

def get_weights(total_words_index, tfidf_text, tfidf_kw, dk, d_k, _dk, _d_k):
    ttext = dict(tfidf_text)
    tkw = dict(tfidf_kw)
    weights = []
    max_dk = get_tfidf(ttext, tkw, dk, type="max")
    min_dk = get_tfidf(ttext, tkw, dk, type="min")
    max_d_k = get_tfidf(ttext, tkw, d_k, type="max")
    min_d_k = get_tfidf(ttext, tkw, d_k, type="min")
    max__dk = get_tfidf(ttext, tkw, _dk, type="max")
    min__dk = get_tfidf(ttext, tkw, _dk, type="min")
    mint = min(min_dk, min__dk, min_d_k)
    maxt = max(max__dk, max_d_k, max_dk)
    for wid in total_words_index:
        if wid in dk:
            #weights.append(len(total_words_index) + ((tkw[wid] - min_dk)/max_dk)*0.2)
            weights.append(1 + ((tkw[wid] - min_dk)/max_dk)*0.2)
        elif wid in _dk:
            weights.append(0.6 + ((tkw[wid] - min__dk)/max__dk)*0.2)
        elif wid in d_k:
            weights.append(0.3 + ((ttext[wid] - min_d_k)/max_d_k)*0.2)
        elif wid in _d_k:
            weights.append(0.1)
    return weights


def extract_kw(r, dic, tfidf_text, tfidf_kw, centroids, degree_diff_mode=None):
    wdic, kwords_index = init_data(r, dic, tfidf_text, tfidf_kw)
    total_words_index = list(wdic.keys())
    total_vecs = list(wdic.values())
    #calculate degree_diff: variance or cosine
    #degree_diff = {(word_id, degree),...}
    degree_diff = get_degree_diffs(total_words_index, total_vecs, centroids, degree_diff_mode)
    sorted_degree = sorted(degree_diff, key=lambda a : a[1]) # [:n] are domain words
    #get domain words
    domain_words = get_domainwords(sorted_degree)
    #split words to four group: domain&keyword, domain&~keyword...
    dk, d_k, _dk, _d_k = group_words(domain_words, total_words_index, kwords_index)
    #get weights
    weights = get_weights(total_words_index, tfidf_text, tfidf_kw, dk, d_k, _dk, _d_k)

    #for debug
    kw = []
    for i in total_words_index:
        kw.append(dic[i])
    #weights = [1 for i in range(len(weights))]
    return total_vecs, weights, kw



