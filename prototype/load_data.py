__author__ = 'ssm'

'''
prepare data
'''


import numpy as np
import jieba
import json
import extract_people_info_new as epi
import extract_paper_info as epai

def load_paper():
    '''
    :return: {tag1: [(paper1_title, paper1_brief, paper1_keywords), (,,),], tag2: [,,]...}
    '''
    tags = epai.get_paper_raw_info()
    return epai.get_paper_info(tags)

def load_people():
    '''
    :return: {tag1: [([p1_field], [p1_bumen], [p1_other]), ([pn_f],[pn_b],[pn_other])], tag2: ([p2_field],..), ..}
    '''
    # extract people info
    tags = epi.get_people_raw_info()
    return epi.get_people_info(tags)

def load_centroids():
    return np.load("subject_tree.npy", encoding='latin1')


def load_data():
    '''
    :return: centroids(subject tree), [(c1, [ch1, ch2, ch3]), (c2, [ch1, ch2,..])]
             people(keywords extracted from :
                {tag1: [([p1_field], [p1_bumen], [p1_other]), ([pn_f],[pn_b],[pn_other])], tag2: ([p2_field],..), ..}),
             paper(keywords extracted from:
                {tag1: [(paper1_title, paper1_brief, paper1_keywords), (,,),], tag2: [,,]...})
    '''
    #load centroids
    centroids = load_centroids()
    print('end loading centroids')

    #load people
    people = load_people()
    print('end loading people info')

    #load paper
    paper = load_paper()
    print('end loading paper info')

    return centroids, people, paper
