import random
import numpy as np
import matplotlib.pyplot as plt

mu = 1.
fig, axes = plt.subplots(3,1)#,figsize=(10,10))
for num,ax in zip([10,100,1000],axes.flat):
    rWalk = np.zeros(num)
    for ii in range(15):
        for jj in range(1,num):
            rWalk[jj] = rWalk[jj-1] + (mu + random.uniform(-1,1))/num
        ax.plot(np.linspace(0,1,num),rWalk)
    ax.plot([0,1],[0,1],'k-',linewidth=2)
    ax.set_ylim(0,1)
plt.savefig('walkWDrift.png')