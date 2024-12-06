# functions for BitCoin price modeling

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
        _,_,op,hi,lo,cl,vol,_,_ = line.strip().split(',')
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

def prevSlope(price1,price2,t_i):
# calcs slope of line between price for interval (t_[i-1],t_i)
    
    return (price2 - price1)/t_i

def mean(priceData):
# Inputs:
#     priceData   :   vector of all prices up to time t_i
# Output:
#     mu          :   mean of data
    
    ct = 0
    sum = 0
    for price in priceData:
        ct += 1
        sum += price

    return sum/ct

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


def sigma(mu_i,S_i):
# Inputs:
#     mu_i      :   mean of prices up to time t_i
#     S_i       :   stock price at time t_i
# Output:
#     sigma     :   variance at time t_i

    return (S_i - mu_i)**2

def deltaVar(mu1,mu2,P1,P2):
# Inputs:
#     mu1,mu2     :   means at t_[i-1],t_i
#     P1,P2       :   prices at t_[i-1],t_i
# Output:
#                 :   delta var btween time t_[i-1] & t_i

    dVar = (mu2-mu1)*(mu2+mu1) + 2.*(mu1*P1-mu2*P2) + (P2-P1)*(P2+P1)
    # = (m2-S2)**2 - (m1-S1)**2
    
    return dVar

def assetWalk(data,n,deltaT,vData):
# assumes uniform time intervals
# Inputs:
#     data    :   np.array with desired bitcoin data
#     n       :   len(data), passed bc already have in driver()
#     deltaT  :   length of time interval
# Outputs:
#     walk    :   predicted values of asset using random walk

# initaalize stock as S0
    walk = np.zeros(n)
    price0 = data[0]
    walk[0] = price0
    walk[1] = data[1]
    walk[2] = data[2]
    correction = 0

# walk accodring to formula
#   calc mu, sigma
#   take step
    for ii in range(2,n-1):
        # mu = mean(data[:ii])
        # var = sigma(mu,data[ii])
        # drft = drift(data[ii-1],data[ii],ii*5)
        # walk[ii+1] = walk[ii] + drft*deltaT + math.sqrt(var*deltaT)*random.uniform(-1,1)
        data1 = data[ii-1]; data2 = data[ii];
        mu1,mu2 = deltaMu(data[:ii])
        dVar = deltaVar(mu1,mu2,data1,data2)
        volFrac = vData[ii]/vData[ii-1]
        pSlope = prevSlope(data1,data2,deltaT)
        # walk[ii+1] = walk[ii] + (mu2-mu1)*random.uniform(0,pSlope) + dVar/math.sqrt(abs(dVar))*random.uniform(0,volFrac)
        walk[ii+1] = walk[ii] + (mu2-mu1)*pSlope*random.uniform(0,1) + dVar/math.sqrt(abs(dVar))*volFrac*random.uniform(0,1)
        # walk[ii+1] = walk[ii] + (mu2-mu1) + dVar/math.sqrt(abs(dVar))*random.uniform(0,volFrac)
        # walk[ii+1] = walk[ii] + (mu2-mu1) + dVar/math.sqrt(abs(dVar))*random.uniform(0,volFrac)
    
    return walk

def sign(num):
# returns sign of number

    return num/abs(num)

    
def driver():
    n = 700
    deltaT = 5
    times = np.array(range(0,n*5,5))
    # units [min]
    filename = "BTCDailyData.csv"
    openPrices = postProcess(filename,1,n)
    volumes = postProcess(filename,5,n)
    for num in [100,250,500,700]:
        for sims in range(10):
            walk = assetWalk(openPrices,num,deltaT,volumes)
            # if sims == 0:
            # # initialize walkMin
            #     best = walk
            # else:
            #     if best[-1] > walk[-1]:
            #         best = walk
            plt.plot(times[:num],walk,'b-')
        plt.plot(times[:num],openPrices[:num],'g-')
        plt.xlabel('t [min]')
        plt.ylabel('BTC ($)')
        plt.title('1st '+str(num)+' Data Points')
        plt.show()

driver()