import numpy as np

np.set_printoptions(precision=11)

with open('river1.txt','r') as fp:
    lines = fp.readlines()
    n = (len(lines))
    xvals = np.zeros(n-1)
    yvals = np.zeros(n-1)
    count = 0
    for line in lines[1:]:
        stuff = line.split('\t')
        xvals[count] = float(stuff[1])
        yvals[count] = float(stuff[2])
        count += 1