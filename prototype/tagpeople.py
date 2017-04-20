__author__ = 'ssm'

'''
generate result by tagging people, merging and giving reminders
1. if num of 1st_category < n, ignore; assume numof(left categories) == numof(real entities)
2. left categories  <---map---  people info
    1) if same people_record mapped to same categories, merge two people_records
    2) if different ... do nothing
    3) after traverse all people_record, if some categories are not mapped,
        a. if category is 1st subject, create new record for people (add new people entity)
        b. if c is 2nd subject, giving merge reminder
'''

import extract_keyword as ek
import redis
import area_score as ars

r = redis.StrictRedis(host='10.2.1.7', port=6379, db=0)

########################match people, paper###########################
def get_people_ctag(people, cvecs, dictionary, tfidf):  #get the subject
    '''
    :param people: ([p1_field], [p1_bumen], [p1_other])
    :param cvecs: [(ctag1, cvec1), (ctag2, cvec2) ..]
    :return: ctag
    '''
    centroids = list(dict(cvecs).values())
    ctags = list(dict(cvecs).keys())
    #people_field
    bow_field = dictionary.doc2bow(people[0])
    tfidf_field = tfidf[bow_field]
    sorted_tfidf_field = sorted(tfidf_field, key=lambda a: a[1], reverse=True)
    field_wvecs, field_weights, field_kw = ek.extract_kw(r, dictionary, dict(sorted_tfidf_field[:20]),
        {}, centroids, degree_diff_mode="cosine")
    field_weights = list(map(lambda a: a * 5, field_weights))

    #people_bumen
    bow_bumen = dictionary.doc2bow(people[1])
    tfidf_bumen = tfidf[bow_bumen]
    sorted_tfidf_bumen = sorted(tfidf_bumen, key=lambda a: a[1], reverse=True)
    bumen_wvecs, bumen_weights, bumen_kw = ek.extract_kw(r, dictionary, dict(sorted_tfidf_bumen[:20]),
        {}, centroids, degree_diff_mode="variance")
    bumen_weights = list(map(lambda a: a * 2, bumen_weights))

    #people_other
    bow_other = dictionary.doc2bow(people[2])
    tfidf_other = tfidf[bow_other]
    sorted_tfidf_other = sorted(tfidf_other, key=lambda a: a[1], reverse=True)
    other_wvecs, other_weights, other_kw = ek.extract_kw(r, dictionary, dict(sorted_tfidf_other[:20]),
        {}, centroids, degree_diff_mode="cosine")
    other_weights = list(map(lambda a: a * 4, other_weights))

    print("people words {}".format(people))
    print("get people keywords {}\n".format(list(zip(field_kw+bumen_kw+other_kw,
                                                   field_weights+bumen_weights+other_weights))))

    vecs_weights = list(zip(field_wvecs + bumen_wvecs + other_wvecs,
                             field_weights + bumen_weights + other_weights))
    sorted_vw = list(sorted(vecs_weights, key=lambda a: a[1], reverse=True))
    important_vecs = [a[0] for a in sorted_vw[:int(len(sorted_vw)/3)]]
    important_weights = [a[1] for a in sorted_vw[:int(len(sorted_vw)/3)]]

    #area score
    record = ars. area_score(important_vecs,
                             important_weights,
                             centroids)
    #print('record len {}'.format(len(record)))
    if len(record) == 0:
        return None
    category = record[0][0]
    ctag = ctags[category][0]
    return ctag

def match_people(cvecs, people_info, dictionary, tfidf):
    '''
    :param cvecs: [(ctag1, cvec1), (ctag2, cvec2) ..]
    :param people_info: [([p1_field], [p1_bumen], [p1_other]), ([pn_f],[pn_b],[pn_other]),..]
    :return: {ctag_1(subject): re1, ctag_2: re2,..}  (re: real entity, represent by index list or special string
            ; ctag: category tag)
    '''
    ret = {}
    for i in range(len(people_info)):
        people = people_info[i]
        ctag = get_people_ctag(people, cvecs, dictionary, tfidf)
        if ctag is None:
            continue
        if ctag in ret:
            ret[ctag].append(i)
        else:
            ret[ctag] = [i]
    # check unmapped
    ctags = list(dict(cvecs).keys())
    ad = 0
    mg = 0
    for ctag in ctags:
        if ctag in ret:
            continue
        sp_ctag = ctag.split('_')
        # if ctag is 1st subject
        if len(sp_ctag) == 1:
            ret[ctag] = 'add_record_' + str(ad) + ' ' + str(ctag)
            ad += 1
        # if ctag is 2nd subject
        if len(sp_ctag) == 2:
            ret[ctag] = 'merge_record_' + str(mg) + ' ' + str(ctag)
            mg += 1
    return ret

############################################################################


def get_categories_candidates(tagged_paper, centroids):
    '''
    :param tagged_paper: {tag1: [st1, st2, st3...], tag2: [st1, st2, ...]}
    :param centroids:  [(c1, [ch1, ch2, ch3]), (c2, [ch1, ch2,..])]
    :return: {tag1: [(ctag1, cvec1), (ctag2, cvec2) ..], tag2: [,,]...}
    '''
    ret = {}
    for tag in tagged_paper:
        tlist = tagged_paper[tag]
        # filter count < d, store candidate tag to ctlist
        ctlist = []
        for t in tlist:
            if tlist.count(t) == 0:
                continue
            ctlist.append(t)
        # parse tags and store centroids vecs
        vecs = []
        for ct in ctlist:
            tags = list(map(lambda a: int(a), ct.split('_')))
            if len(tags) == 2:
                vecs.append((ct, centroids[tags[0]][1][tags[1]]))
            else:
                vecs.append((ct, centroids[tags[0]][0]))
        ret[tag] = vecs
    return ret

import datetime

def _tagpeople(centroids, tagged_paper, people, dictionary, tfidf):
    '''
    :param centroids: [(c1, [ch1, ch2, ch3]), (c2, [ch1, ch2,..])]
    :param tagged_paper: {tag1(paper tag): [(paper's subject)st1, st2, st3...], tag2: [st1, ...]}
    :param people: {tag1: [([p1_field], [p1_bumen], [p1_other]),
                    ([pn_f],[pn_b],[pn_other])], tag2: ([p2_field],..), ..}
    :return: real_entity abbr. re
            {tag1: {re1: [paper index in tagged paper],
            re2: [paper index in tagged paper]..
            merge: ([merge options], [paper index in tagged paper])}, tag2:..}
    '''

    # get categories candidates for each tag (ignore # < d)
    ctag_vecs = get_categories_candidates(tagged_paper, centroids)

    # for each tag, map people info to categories_candidates
    ret = {}
    for tag in people:
        papers = tagged_paper[tag]
        #{ctag_1: re1, ctag_2: re2,..}

        #print("==================\ntagged paper {}\n".format(tagged_paper))
        #print("====extract people {}====".format(tag))
        tagged_people = match_people(ctag_vecs[tag], people[tag], dictionary, tfidf)
        #print("====tagged people======\n{}".format(tagged_people))
        ctags = list(dict(tagged_people).keys())
        entities = list(dict(tagged_people).values())
        tmp = {}
        for i, entity in enumerate(entities): # entity is a list of people index of people[tag] or string
            subject = ctags[i]
            paper_index = [i for i in range(len(papers)) if papers[i] == subject]
            if 'record' in entity:
                tmp[entity] = paper_index
            else:
                tmp[tuple(entity)] = paper_index
        ret[tag] = tmp
        print("end tag {} {}".format(tag, datetime.datetime.now()))
    return ret

def tagpeople(centroids, tagged_paper, people, dictionary, tfidf):
    '''
    :param centroids: [(c1, [ch1, ch2, ch3]), (c2, [ch1, ch2,..])]
    :param tagged_paper: {tag1(paper tag): [(paper's subject)st1, st2, st3...], tag2: [st1, ...]}
    :param people: {tag1: [([p1_field], [p1_bumen], [p1_other]),
                    ([pn_f],[pn_b],[pn_other])], tag2: ([p2_field],..), ..}
    :return: real_entity abbr. re
            {tag1: {re1: [paper index in tagged paper],
            re2: [paper index in tagged paper]..
            merge: ([merge options], [paper index in tagged paper])}, tag2:..}
    '''

    # get categories candidates for each tag (ignore # < d)
    ctag_vecs = get_categories_candidates(tagged_paper, centroids)

    # for each tag, map people info to categories_candidates
    ret = {}
    for tag in people:

        papers = tagged_paper[tag]
        #{ctag_1: re1, ctag_2: re2,..}
        #print("==================\ntagged paper {}\n".format(tagged_paper))
        #print("====extract people {}====".format(tag))
        tagged_people = match_people(ctag_vecs[tag], people[tag], dictionary, tfidf)
        #print("====tagged people======\n{}".format(tagged_people))
        ctags = list(dict(tagged_people).keys())
        entities = list(dict(tagged_people).values())
        tmp = {}
        len_list = []
        for i, entity in enumerate(entities): # entity is a list of people index of people[tag] or string
            if entity.__contains__('merge_record_'):
                '''
                # merge x : tuple(entity_1), tuple(entity_2).. <= possible merging options
                # pick the 1st part, all tags including 1st part can be considered as merge options
                #continue
                subject = ctags[i]
                c = subject.split('_')
                merge_options = []
                for tmp_tag in ctags:
                    if tmp_tag.__contains__(c[0]) and not tagged_people[tmp_tag].__contains__('merge'):
                        merge_options.append(tagged_people[tmp_tag])
                paper_index = [i for i in range(len(papers)) if papers[i] == subject]
                #tmp[entity] = (merge_options, paper_index)
                tmp[entity] = paper_index
                '''
            else:
                #entity [pi, pj,..], records assigned to same category
                subject = ctags[i]
                paper_index = [i for i in range(len(papers)) if papers[i] == subject]
                if entity.__contains__('add_record_'):
                    tmp[entity] = paper_index
                else:
                    tmp[tuple(entity)] = paper_index
                len_list.append(len(paper_index))
        # deal with merge options
        # merge papers to other 1st subject (same 1st subject with this merge record)
        len_list = list(sorted(len_list, reverse=True))
        for i, entity in enumerate(entities):
            if entity.__contains__('merge_record_'):
                subject = ctags[i]
                c = subject.split('_')
                paper_index = [i for i in range(len(papers)) if papers[i] == subject]
                if len(paper_index) > min(len_list[:int(len(len_list)/3)]):
                    #entity = entity.replace('merge', 'add')
                    tmp[entity] = paper_index
                    continue
                isadded = False
                #add merge paperindex to added record
                for tmp_tag in ctags:
                    sp_tmp_tag = tmp_tag.split('_')
                    if c[0] == sp_tmp_tag[0] and not 'merge' in tagged_people[tmp_tag]:
                        isadded = True
                        if 'add' in tagged_people[tmp_tag]:
                            tmp[tagged_people[tmp_tag]] += paper_index
                        else:
                            tmp[(tuple(tagged_people[tmp_tag]))] += paper_index
                if isadded == False:
                    tmp['mg_to_add ' + subject] = paper_index
                    #ctags.append('mg_to_add ' + subject)

        ret[tag] = tmp
        print("end tag {} {}".format(tag, datetime.datetime.now()))
    return ret
