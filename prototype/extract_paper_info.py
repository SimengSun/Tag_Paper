#coding:utf-8
__author__ = 'ssm'

import json

def get_items(plist, field_list):
    ret = []
    for it in plist:
        tmp = ''
        for field in field_list:
            tmp += it[field]
        ret.append(tmp)
    return ret


def get_paper_raw_info():
    with open("prototype_paper.json", "r") as f:
        paper = json.load(f, strict=False)

    text = get_items(paper, ['title_cn_ais', 'abstract_cn_ais'])
    kw = get_items(paper, ['keyword_cn_ais'])
    tags = get_items(paper, ['tag'])

    #write file
    with open("text.txt", "w") as f:
        for t in text:
            f.write(t.replace('\n', '').encode('utf-8') + '\n')
    with open("kw.txt", "w") as f:
        for k in kw:
            f.write(k.encode('utf-8') + '\n')
    return tags

#get_paper_raw_info()
#seg paper using ansj get: text_seg.txt + kw_seg.txt

def get_paper_info(tags):
    '''
    :param tags:
    :return: {tag1:([title1], [kw1]), tag2:([title2], [kw2]), ...}
    '''
    with open("text_seg.txt", "r") as f:
        lines = f.readlines()
        texts = []
        for line in lines:
            sp = line.strip().split(' ')
            texts.append(sp)
    with open("kw_seg.txt", "r") as f:
        lines = f.readlines()
        kws = []
        for line in lines:
            sp = line.strip().split(' ')
            kws.append(sp)
    if len(kws) != len(texts):
        print('error!')
        exit()
    values = list(zip(texts, kws))
    ret = {}
    for i in range(len(tags)):
        if tags[i] in ret:
            ret[tags[i]].append(values[i])
        else:
            ret[tags[i]] = [values[i]]
    return ret

#tags = get_paper_raw_info()
#ret = get_paper_info(tags)
#print ret.items()[:1]