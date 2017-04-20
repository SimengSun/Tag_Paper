__author__ = 'ssm'


w=[]
w.append('abc')
w.append('abd')
w.append('abe')
w.append('abw')


with open("test.txt", "w") as f:
    f.writelines(w)