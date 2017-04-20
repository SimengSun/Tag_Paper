#coding:utf-8
__author__ = 'ssm'


import jieba
import Util

'''
ordered by importance:
research field
bumen
other(paper, project, experience) : filter words not related to education(stopwords)
'''

#jieba.load_userdict("D:\\Codes\\TagPaper\\cluster\\data\\keywordrank.txt")

with open("stopwords", "r") as f:
    stopwords = f.readlines()
    stopwords = map(lambda a: a.strip(), stopwords)

#load tfidf model
dictionary, tfidf = Util.get_models()


def reg(s):
    return ''.join(list(filter(lambda a: a not in ',.>-:()（）!@#$%^&*~{}|；;：:"“’‘”。，《'
                                    '》？|】【、>_=/+1234567890abcdefghi'
                                    'jklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ ', s)))


def stopword(wlist):
    ret = []
    for word in wlist:
        flag = True
        for w in stopwords:
            if w.__contains__(word) or w == word or word.__contains__(w):
                flag = False
                break
        if flag:
            ret.append(word)
    return ret

def get_field(item):
    reg_field = item['researchfield_ais']
    reg_field = reg(reg_field)
    field = jieba.cut(reg_field, cut_all=False)
    return list(filter(lambda a: len(a) > 1, list(field)))

bumen_stopwords = ['系','学院','院','专业','所','大学']
def get_bumen(item):
    bumen = item['bumen_s'] + item['academy_is']
    reg_bumen = reg(bumen)
    bumen = list(jieba.cut(reg_bumen, cut_all=False))
    ret = []
    for w in bumen:
        ret.append(''.join(list(filter(lambda a: a not in bumen_stopwords, w))))
    return list(filter(lambda a : len(a) > 1, ret))

def get_other(item):
    '''
    first merge, then filter special char, then segmentation, then filter stop words
    '''
    other = item['paper_ais'] + item['project_ais'] + item['experience_ais']
    f = open("test.txt", "w")
    reg_other = reg(other)
    f.write(reg_other)
    f.write('\n')
    other = list(jieba.cut(reg_other, cut_all=False))
    for w in other:
        f.write(w + ' ')
    f.write('\n')
    other = stopword(other)
    for w in other:
        f.write(w + ' ')

    bow = dictionary.doc2bow(other)
    tf_idf = tfidf[bow]
    sort_tfidf = sorted(tf_idf, key=lambda a: a[1], reverse=True)
    ret = []
    for i in range(int(len(sort_tfidf)/3)):
        ret.append(dictionary[sort_tfidf[i][0]])
    return list(filter(lambda a: len(a) > 1, ret))

def extract_people_info(people_it):
    return [get_field(people_it), get_bumen(people_it), get_other(people_it)]


'''
import json
with open("prototype_people.json", "r") as f:
    parsed = json.load(f, strict=False)

re = extract_people_info(parsed[7])
for i in range(3):
    for j in range(len(re[i])):
        print re[i][j]

'''




'''
dropped plan

# segmentation (add user dictionary)

# filter words not in keywordrank

# paper: top 5 tfidf (high weights)

# academy/project/experience: eliminate education related words

# research field: eliminate education related words(high weights)

# overall, return paper_words, extra_words, field_words

'''

