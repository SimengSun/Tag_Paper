__author__ = 'ssm'

'''
randomly get 120k word+wordvec from redis
'''
import random
import numpy as np
import Util
import datetime

wv = {}
with open("all_keywords.txt", "r") as f:
    lines = f.readlines()
    count = 0
    while count != 120000:
        # get random number
        ri = random.randint(0, len(lines)-1)
        tmp_w = lines[ri].strip('\n')
        # if word already exist, continue
        if tmp_w in wv:
            continue
        else:
            #print(tmp_w)
            if not tmp_w in Util.get_r():
                #print("{} not in r".format(tmp_w))
                #exit()
                continue
            wv[tmp_w] = Util.get_vec(tmp_w)
            count += 1
            if count % 10000 == 0:
                print("end {} {}".format(count, datetime.datetime.now()))

np.save("init_vecs", wv)