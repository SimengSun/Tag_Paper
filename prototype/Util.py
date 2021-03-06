__author__ = 'ssm'

from gensim import corpora
from gensim import  models
import codecs

def get_models():
    dictionary = corpora.Dictionary.load("kejso_words.dict")
    tfidf = models.TfidfModel.load("kejso_tfidf_model.model")
    return dictionary, tfidf


def get_paper_words(result_i, papers_i):
    '''
    :param result_i: {re1: [paper index in tagged paper],
                     re2: [paper index in tagged paper]..
                     'merge': ([merge options], [paper index in tagged paper])}
    :param papers_i: [(paper1_title, paper1_brief, paper1_keywords), (,,),]
    :return: ['re1 : hotwords', 're2 : hotwords', ...]
    '''
    ret = []
    for entity in result_i:
        tmp = str(entity) + ' : '
        paper_index = result_i[entity]
        '''
        if type(paper_index) is tuple:
            tmp += 'merge options: ' + str(paper_index[0])
            tmp += 'paper index: ' + str(paper_index[1])
            continue
            '''
        papers = [papers_i[i] for i in range(len(papers_i)) if i in paper_index]
        if len(papers) < 2:
            continue
        for p in papers:
            for word in p[1]:
                if len(word) > 1:
                    tmp += word + ' '
        tmp += '\n\n'
        ret.append(tmp)
    return ret


def printresult(result, paper):
    '''
    print result
    #format#
    [entity index of certain tag] : [list of hot words from papers]

    :param result: real_entity abbr. re
                 {tag1: {re1: [paper index in tagged paper],
                 re2: [paper index in tagged paper]..
                'merge': ([merge options], [paper index in tagged paper])}, tag2:..}
    :param paper: {tag1: [(paper1_title, paper1_brief, paper1_keywords), (,,),], tag2: [,,]...}
    :return:
    '''
    for tag in result:
        print('========[SEARCH: ' + tag + ']========\n')
        result_i = result[tag]
        papers_i = paper[tag]
        if tag == u'北京航空航天大学_张辉':
            print("entity count {}".format(len(result_i)))
            print("result {}".format(result_i))
        re = get_paper_words(result_i, papers_i)
        for line in re:
            print(line)

import random

def generate_cloud_tag_tfidf(result, tfidf_kw, dictionary, paper):
    '''
    :param result: real_entity abbr. re
                 {tag1: {re1: [paper index in tagged paper],
                 re2: [paper index in tagged paper]..
                'merge': ([merge options], [paper index in tagged paper])}, tag2:..}
    :param tfidf_kw: {tag1: [((wordindex, tfidf_value), (w, t), ..), ((w, t), (w, t),..)]}
    :param dictionary:
    :return:
    '''
    for tag in result:
        entities = result[tag]
        tfidf = tfidf_kw[tag]
        entity_count = 0
        paper_i = paper[tag]
        for entity in entities:
            word_dict = {}
            paper_indexlist = entities[entity]
            papers = [paper_i[i] for i in range(len(paper_i)) if i in paper_indexlist]
            #write to files
            if entity.__contains__('mg') or 'merge' in entity:
                with open('./cloudtags/' + tag + '_merge_' + str(entity_count) + '.txt', 'w') as f:
                    line = ''
                    for p in papers:
                        for word in p[0]:
                            line += word + ' '
                        line += '\n'
                    f.write(line)
            else:
                with open('./cloudtags/' + tag + '_' + str(entity_count) + '.txt', 'w') as f:
                    line = ''
                    for p in papers:
                        for word in p[0]:
                            line += word + ' '
                        line += '\n'
                    f.write(line)

            if len(paper_indexlist) < 2:
                continue

            for i in paper_indexlist:
                index = i
                tfidf_values = tfidf[index]
                for item in tfidf_values:
                    word = dictionary[item[0]]
                    if word in word_dict:
                        if item[1] > word_dict[word]:
                            word_dict[word] = item[1]
                    else:
                        word_dict[word] = item[1]
            sort_word_dic = list(sorted(word_dict.items(), key=lambda a:a[1], reverse=True))
            if len(sort_word_dic) == 0:
                continue
            base = - sort_word_dic[len(sort_word_dic)-1][1] + sort_word_dic[0][1]
            count = 0
            word_dict_new = {}
            for word in word_dict:
                word_dict[word]= (word_dict[word] - sort_word_dic[0][1])*15/base
                count += 1
            if count <= 7:
                continue
            #random choose 35
            count = 0
            while count != 35:
                if len(word_dict) == len(word_dict_new):
                    break
                get_key = random.choice(list(word_dict.keys()))
                if not get_key in word_dict_new:
                    word_dict_new[get_key] = word_dict[get_key]
                    count += 1
            if entity.__contains__('mg') or 'merge' in entity:
                Generate_cloud('./cloudtags/' + tag + '_merge_' + str(entity_count) + '.html', word_dict_new)
            else:
                Generate_cloud('./cloudtags/' + tag + '_' + str(entity_count) + '.html', word_dict_new)
            entity_count += 1

def generate_cloud_tag(result, paper_wordweights):
    '''
    :param result:
                real_entity abbr. re
                 {tag1: {re1: [paper index in tagged paper],
                 re2: [paper index in tagged paper]..
                'merge': ([merge options], [paper index in tagged paper])}, tag2:..}
    :param paper_wordweights: keywords and its weights of tagged papers
                {tag1: [((word1,weight1),(word2,weight2),..), ((word1,weight1),..)], tag2:[]}
    :return: generate cloud tags for each entities
    '''
    for tag in result:
        entities = result[tag]
        papers_words = paper_wordweights[tag]
        i = 0
        for entity in entities:
            word_dic = {} # word dic for certain entity
            paper_indexlist = entities[entity]
            if entity.__contains__('merge_record_'):
                continue
            #print("entity {}".format(entity))
            #print("entities {}".format(entities))
            #print("paper_indexlist {}".format(paper_indexlist))
            for i in paper_indexlist:
                index = i
                #print("index {}".format(index))
                #print("entity paper list {}".format(entities[entity]))
                paper_i_words = papers_words[index]
                for item in paper_i_words[:]:
                    if item[0] in word_dic:
                        if item[1] > word_dic[item[0]]:
                            word_dic[item[0]] = item[1]
                    else:
                        word_dic[item[0]] = item[1]

            sort_word_dic = list(sorted(word_dic.items(), key=lambda a:a[1], reverse=True))
            if len(sort_word_dic) == 0:
                continue
            base = - sort_word_dic[len(sort_word_dic)-1][1] + sort_word_dic[0][1]

            count = 0
            for word in word_dic:
                if count == 35:
                    break
                word_dic[word]= (word_dic[word] - 3*sort_word_dic[0][1]/2)*20/base
            Generate_cloud('./cloudtags/' + tag + '_' + str(i) + '.html', word_dic)
            i += 1




# input is a dict {'word':weight,...}
def Generate_cloud(file_name,words_dict):
    file = codecs.open(file_name, "w",encoding='utf-8')
    file.write('<!DOCTYPE html>'+'\n')
    file.write('<html><head><title>jQCloud Example</title>'+'\n')
    file.write('<link rel="stylesheet" type="text/css" href="jqcloud.css" />'+'\n')
    file.write('<script type="text/javascript" src="jquery-2.1.1.js"></script>'+'\n')
    file.write('<script type="text/javascript" src="jqcloud-1.0.4.js"></script>'+'\n')
    file.write('<script type="text/javascript">'+'\n')
    file.write(' var word_array = [')
    # write words
    cloud_str = ''
    for word,weight in words_dict.items():
        temp = '{text: "'+word+'", weight: '+str(weight)+'},'
        cloud_str += temp
    file.write(cloud_str+'\n')
    file.write('];'+'\n')
    file.write('$(function() {$("#example").jQCloud(word_array);});</script>'+'\n')
    file.write('</head><body><div id="example" style="width: 550px; height: 350px;"></div></body></html>'+'\n')
    file.close()