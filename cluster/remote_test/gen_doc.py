__author__ = 'ssm'

import os

path = "./iter_70_2nd/"


def tostring(a):
    s = ''
    for w in a:
        s += w.strip() + ' '
    s += ';'
    return s

def tostring1(a):
    a = a.replace('[', '')
    a = a.replace(']', '')
    return a.strip()

dirs = os.listdir(path)
st = ''
i = 0
for dir in dirs:
    files = os.listdir(path + dir)
    st += str(i) + '\n'
    i += 1
    for file in files:
        if file.endswith(".txt"):
            with open(path + dir + "/" + file) as f:
                lines = f.readlines()
                st += '\t-\n'
                st += '\t\t- ' + str(len(lines)) + ' ' + tostring1(lines[0]) + ' ' + tostring(lines[1:6]) + '\n'

with open("doc.txt", "w") as f:
    f.write(st)
