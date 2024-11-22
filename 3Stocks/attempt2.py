import math
import random
import numpy as np
import matplotlib.pyplot as plt

def data2Array(csvFile,n):
# Inputs:
#     csvFile :   name of .csv file with Bitcoin data in 5 min intervals
#     n       :   number of points from data (default 0 = take all datapoints)
# Outputs:
#     data    :   np.array of all data

    with open(csvFile,'r') as fp:
        data = fp.readlines()
        if n != 0:
            data = data[1:n+1]
        else:
            data = data[1:]
    return data

def postProcess(csvFile,opt,n):
# Inputs:
#     csvFile     :   input for data2Array()
#     n           :   input for data2Array()
#     opt         :   option for vector to return
#         1 = open prices of stock
#         2 = close prices of stock
#         3 = high prices of stock
#         4 = low prices of stock
#         5 = volume for each transactions
# Output:
#     rVec        :   np.array with chosen data

    priceData = data2Array(csvFile,n)
    # get data
    rVec = np.zeros(n)
    # initialize return vector

    for ii,line in zip(range(n),priceData):
        _,op,hi,lo,cl,vol = line.strip().split(',')
        if opt == 1:
            rVec[ii] = op
        elif opt == 2:
            rVec[ii] = cl
        elif opt == 3:
            rVec[ii] = hi 
        elif opt == 4:
            rVec[ii] = lo
        elif opt == 5:
            rVec[ii] = vol 
        else:
            print('error: invalid opt')
            return 0

    return rVec

def deltaMu(priceData):
# Inputs:
#     priceData   :   vector of all prices up to time t_i
# Output:
#                 :   delta mean btween time t_[i-1] & t_i
    
    ct = 0
    sum = 0
    for price in priceData:
        ct += 1
        sum += price

    mu1 = (sum-priceData[-1])/(ct-1)
    mu2 = sum/ct

    return mu1,mu2

def deltaVar(mu1,mu2,P1,P2):
# Inputs:
#     mu1,mu2     :   means at t_[i-1],t_i
#     P1,P2       :   prices at t_[i-1],t_i
# Output:
#                 :   delta var btween time t_[i-1] & t_i

    dVar = (mu2-mu1)*(mu2+mu1) + 2.*(mu1*P1-mu2*P2) + (P2-P1)*(P2+P1)
    # = (m2-S2)**2 - (m1-S1)**2
    
    return dVar

# -----------------------

n = 700
openPrices = postProcess('5min.csv',1,n)
volumes = postProcess('5min.csv',5,n)
error = np.zeros(700)

# calc next point

for ii in range(2,n-1):
    mu1,mu2 = deltaMu(openPrices[:ii+1])
    dVar = deltaVar(mu1,mu2,openPrices[ii-1],openPrices[ii])
    volFrac = volumes[ii]/volumes[ii-1]
    if ii%100 == 0:
        guess = 0
        for jj in range(10):
            guess = openPrices[ii] + (mu2-mu1)*random.uniform(0,1)*volFrac + dVar/math.sqrt(abs(dVar))*random.uniform(0,1)*volFrac
            plt.plot([1,2],[openPrices[ii],guess],'b-')
        plt.plot([1,2],[openPrices[ii],openPrices[ii+1]],'g-')
        plt.show()

# compare to actual

# update with next point

# repeat