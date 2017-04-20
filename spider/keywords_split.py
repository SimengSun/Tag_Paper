__author__ = 'ssm'
import os

def process(file):
    ret = []
    with open(file) as f:
        lines = f.readlines()
        for line in lines[1:]:
            tmp = line.replace("\"", "")
            tmp = tmp.replace("||", " ")
            tmp = tmp.replace("|", " ")
            ret.append(tmp)
    return ret

def kw():
    files = os.listdir("keywords")
    kw = []
    for file in files:
        kw += process(".\\keywords\\" + file)
    with open("keywords_addition.txt", "w") as f:
        f.writelines(kw)

kw()