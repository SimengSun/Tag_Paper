#coding:utf-8
__author__ = 'ssm'

'''
1. on the first run, just run the get raw people info function, not entire program
   it will produce people raw information files:
    research filed, bumen, paper and so on
2. then should seg these raw files by ansj(java), produce segmented files
3. on the second run, deal with the segmented files
'''

import json

def get_items(plist, field_list):
    ret = []
    for it in plist:
        tmp = ''
        for field in field_list:
            tmp += it[field]
        ret.append(tmp)
    return ret

def get_people_raw_info():
    with open("prototype_people.json", "r") as f:
        people = json.load(f, strict=False)

    research_field = get_items(people, ['researchfield_ais'])
    bumen = get_items(people, ['bumen_s'])
    other = get_items(people, ['paper_ais', 'project_ais', 'experience_ais'])
    tags = get_items(people, ['tag'])

    #reg bumen
    bumen_stopwords = [u'学院', u'系', u'院',u'专业',u'所',u'大学', u'科学']
    bumen_new = []
    for w in bumen:
        for sw in bumen_stopwords:
            if sw == u'院' and w.__contains__(u'医院'):
                continue
            w = w.replace(sw, '')
        bumen_new.append(w)

    # write to files
    with open("researchfield.txt", "w") as f:
        for t in research_field:
            f.write(t.replace('\n', '') + '\n')
    with open("bumen.txt", "w") as f:
        for t in bumen_new:
            f.write(t.replace('\n', '') + '\n')
    with open("other.txt", "w") as f:
        for t in other:
            f.write(t.replace('\n', '') + '\n')
    return tags

#get_people_raw_info()

def get_people_info(tags):
    print("!!getting people info!!")
    with open("stopwords.list", "r") as f:
        lines = f.readlines()
        stopwords = list(map(lambda a: a.strip(), lines))

    with open("researchfield_seg.txt", "r") as f:
        lines = f.readlines()
        fields = []
        for line in lines:
            sp = line.strip().split(' ')
            del_list = []
            for i in range(len(sp)):
                for word in stopwords:
                    if word in sp[i]:
                        del_list.append(sp[i])
            for i in del_list:
                if i in sp:
                    sp.remove(i)
            fields.append(sp)

    with open("bumen_seg.txt", "r") as f:
        lines = f.readlines()
        bumen = []
        for line in lines:
            sp = line.strip().split(' ')
            del_list = []
            for i in range(len(sp)):
                for word in stopwords:
                    if word in sp[i]:
                        del_list.append(sp[i])
            for i in del_list:
                if i in sp:
                    sp.remove(i)
            bumen.append(sp)

    with open("other_seg.txt", "r") as f:
        lines = f.readlines()
        other = []
        for line in lines:
            sp = line.strip().split(' ')
            del_list = []
            for i in range(len(sp)):
                for word in stopwords:
                    if word in sp[i]:
                        del_list.append(sp[i])
            for i in del_list:
                if i in sp:
                    sp.remove(i)
            other.append(sp)

    if len(other) != len(bumen) or len(other) != len(fields) \
        or len(bumen) != len(fields):
        print('error!')
        exit()
    ret = {}
    for i in range(len(tags)):
        if tags[i] in ret:
            ret[tags[i]].append((fields[i], bumen[i], other[i]))
        else:
            ret[tags[i]] = [(fields[i], bumen[i], other[i])]
    return ret





