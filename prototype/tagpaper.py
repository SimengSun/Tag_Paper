__author__ = 'ssm'

'''
tag paper with 1st/2nd subject
'''


import extract_keyword as ek
import redis
import area_score as ars
import datetime



#redis
r = redis.StrictRedis(host='10.2.1.7', port=6379, db=0)


def get_2nd_category(record):
    if record[0][1] - record[1][1] > 0.6 and record[0][1] > 1:
        return '_' + str(record[0][0])
    else:
        return ''

def tagpaper(centroids, papers, dictionary, tfidf):
    '''
    :param centroids: [(c1, [ch1, ch2, ch3]), (c2, [ch1, ch2,..])]
    :param paper: {tag1: [(paper1_text, paper1_keywords), (,,),], tag2: [,,]...}
    :return: tagged_paper {tag1: [st1, st2, st3...]}
             paper_wordweight {tag1: [((word1,weight1),(word2,weight2),..), ((word1,weight1),..)], tag2:[]}
    '''
    #get 1st category
    centroids_1 = {}
    for i in range(len(centroids)):
        centroids_1[i] = centroids[i][0]

    keys = list(papers.keys())
    ret = {}
    paper_wordweight = {}
    tfidf_kw_ret = {}

    debug_i = 0

    for key in keys:
        paper_info = papers[key]
        ret[key] = []
        paper_wordweight[key] = []
        tfidf_kw_ret[key] = []
        for paper in paper_info:
            #get tfidf for each paper and sort
            bow_text = dictionary.doc2bow(paper[0])
            bow_kw = dictionary.doc2bow(paper[1])
            tfidf_text = tfidf[bow_text]
            tfidf_kw = tfidf[bow_kw]
            sorted_tfidf_text = sorted(tfidf_text, key=lambda a: a[1], reverse=True)
            sorted_tfidf_kw = sorted(tfidf_kw, key=lambda a: a[1], reverse=True)

            tfidf_kw_ret[key].append(list(sorted_tfidf_kw))

            category = ''
            #1st match
            wordvecs, weights, kw = ek.extract_kw(r, dictionary, dict(sorted_tfidf_text[:20]), dict(sorted_tfidf_kw),
                                                 list(centroids_1.values()) , degree_diff_mode="variance")
            record = ars.area_score(wordvecs,weights,list(centroids_1.values()))
            category += str(record[0][0])
            #########debug#######
            if key == u'北京航空航天大学_张辉' and debug_i in [1, 11, 12, 16, 32]:
                print("=============people tag {}, index {}================".format(key, debug_i))
                #print("[tfidf]\n {}\n{}\n".format(sorted_tfidf_kw, sorted_tfidf_text[:20]))
                tfidf_dic = []
                tfidf_values = []
                for si in sorted_tfidf_kw:
                    tfidf_dic.append(dictionary[si[0]])
                    tfidf_values.append(si[1])
                for sj in sorted_tfidf_text[:20]:
                    tfidf_dic.append(dictionary[sj[0]])
                    tfidf_values.append(sj[1])
                #print("[tfidf word] {}\n".format(tfidf_dic))
                print("[zipped tfidf word {}]\n".format(list(zip(tfidf_dic, tfidf_values))))
                print("[predicted category] {}\n".format(record))
                print("[extracted keywords+weights] {}\n\n".format(list(zip(kw, weights))))
                #print("[extracted keywords]:{}\n".format(kw))
                #print("[keywords weight]: {}\n\n".format(weights))
            debug_i += 1
            #####################

            words_weights = list(zip(kw, weights))
            s_words_weights = list(sorted(words_weights, key=lambda a: a[1], reverse=True))
            paper_wordweight[key].append(s_words_weights)

            #2nd match
            centroids_2 = centroids[int(category)][1]
            wordvecs, weights, kw = ek.extract_kw(r, dictionary, dict(sorted_tfidf_text[:20]), dict(sorted_tfidf_kw),
                                                 list(centroids_2) , degree_diff_mode="variance")
            record = ars.area_score(wordvecs,weights,list(centroids_2))
            category += get_2nd_category(record)

            #tag paper with subject
            ret[key].append(category)


        print("end tag peper {} {}".format(key, datetime.datetime.now()))
    return ret, paper_wordweight, tfidf_kw_ret

