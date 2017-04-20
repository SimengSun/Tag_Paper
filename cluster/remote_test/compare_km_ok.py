__author__ = 'ssm'

import os

files = os.listdir(".\\km+50\\")
ff = open(".\\cmp_km_ok.txt", "w")

for file in files:
    with open(".\\km+50\\" + file, "r") as f:
        lines = f.readlines()
        ff.write(file + '\t' + lines[0].strip() + '\t' + lines[1].strip()
                 + '\t' + lines[2].strip() + '\t' + lines[3].strip() + '\n')

ff.close()
