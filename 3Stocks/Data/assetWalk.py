import math
import random
import numpy as np
import matplotlib.pyplot as plt

def driver():

    times = {'min': 1, 'day': 1440, 'year': 525600}
    tInt = times['day']
    opens, closes, volumes, trades, n = initialize('BTCDay.csv',tInt)
    xVals = list(range(n-2))
    walkAverages = np.zeros(n-2)
    nSims = 10

    for sims in range(nSims):
        walk = assistedWalk(opens,closes,volumes,trades,n)
        plt.plot(xVals,walk[2:],'bo',markersize=5)
        walkAverages += walk[2:]
    walkAverages = walkAverages/nSims
    plt.plot(xVals,closes[2:],'go',markersize=3)
    plt.xlabel('t [day]')
    plt.ylabel('BTC ($)')
    # plt.title('1st '+str(num)+' Data Points')
    plt.show()
    errors = walkAverages - closes[2:]
    plt.bar(range(n-2),errors)
    plt.show()
    plt.bar(range(n-2),errors/closes[2:])
    plt.show()

    return

def dataCreator(l,opens,highs,lows,closes,volumes,trades):
# creates desired np.array()s

    maxVol = -1; maxTrade = -1
    volatilitys = np.zeros(l)
    # avgVals = np.zeros(l)
    # pSlopes = np.zeros(l-1)
    # concavitys = np.zeros(l-2)
    # volFracs = np.zeros(l-1); tradeFracs = np.zeros(l-1)
    for ii in range(l):
        vol = volumes[ii]
        trade = trades[ii]
        avgVal = 0.5*(opens[ii]+closes[ii])
        if maxVol < vol:
            maxVol = vol
        if maxTrade < trade:
            maxTrade = trade
        # if ii != 0:
        #     volFracs[ii-1] = volumes[ii]/volumes[ii-1]
        #     tradeFracs[ii-1] = trades[ii]/trades[ii-1]
        #     pAvgVal = 0.5*(opens[ii-1]+closes[ii-1])
        #     pSlopes[ii-1] = abs(avgVal - pAvgVal)
        #     if ii != 1:
        #         concavitys[ii-2] = (pSlopes[ii-1]-pSlopes[ii-2])#/tInt
        # avgVals[ii] = avgVal
        volatilitys[ii] = (highs[ii]-lows[ii])/avgVal
    volFracsMax = volumes/maxVol
    tradeFracsMax = trades/maxTrade

    return volFracsMax, tradeFracsMax

def initialize(filename, tInt):
# Inputs:
#     filename    :   .csv file with BTC data
#     tInt        :   time interval ('day','min','week')
# Outpus:
#     see dataCreator()
    '''
    labels: 
        [symbol,timestamp,open,high,low,close,volume,trade_count,vwap]
    '''
    with open(filename, 'r') as fp:
        data = fp.readlines()[1:]
    
    l = len(data)
    xVals = list(range(l))
    opens = np.zeros(l)
    highs = np.zeros(l)
    lows = np.zeros(l)
    closes = np.zeros(l)
    volumes = np.zeros(l)
    trades = np.zeros(l)
    for stuff,ii in zip(data,range(l)):
        dataPt = stuff.strip('\n').split(',')
        opens[ii] = float(dataPt[2])
        highs[ii] = float(dataPt[3])
        lows[ii] = float(dataPt[4])
        closes[ii] = float(dataPt[5])
        volumes[ii] = float(dataPt[6])
        trades[ii] = int(dataPt[7].split('.')[0])
    
    # volFracsMax, tradeFracsMax = dataCreator(l,opens,highs,lows,closes,volumes,trades)
    return opens, closes, volumes, trades, l

def deltaMu(priceData):
# Inputs:
#     priceData   :   vector of all prices up to time t_i
# Output:
#     mu1, mu2    :   mean(priceData), mean(priceData[:-1])
    
    ct = 0
    sum = 0
    for price in priceData:
        ct += 1
        sum += price

    mu2 = sum/ct
    mu1 = (sum-priceData[-1])/(ct-1)

    return mu1,mu2

def deltaVar(mu1,mu2,P1,P2):
# Inputs:
#     mu1,mu2     :   means at t_[i-1],t_i
#     P1,P2       :   closes at t_[i-1],t_i
# Output:
#     dVar        :   delta variance btween time t_[i-1] & t_i

    dVar = (mu2-mu1)*(mu2+mu1) + 2.*(mu1*P1-mu2*P2) + (P2-P1)*(P2+P1)
    # = (m2-S2)**2 - (m1-S1)**2
    
    return dVar

def volatility(vFMax,tFMax):
# Inputs:
#     vFMax   :   volFracMaxs[ii]
#     tFMax   :   tradeFracMaxs[ii]
# Output:
#     volty   :   volatility from linear regression in dimless.py

    # params from dimless.py
    a = -1.994662813486828
    b = 0.24080293
    c = 0.24266584
    return math.e**(a)*(vFMax**(b))*(tFMax**(c))

def signVal(opens,close):
# calculates sign of change for walk

    pSlope = opens[1] - close
    ppSlope = close - opens[0]
    if pSlope*ppSlope > 0:
        if pSlope < 0:
            cine = -1#abs(pSlope)/ppSlope
        cine = 1#pSlope/ppSlope
    else:
        cine = -1#abs(pSlope/ppSlope)

    return cine
        

def assistedWalk(opens,closes,volumes,trades,n):
# predicts given close prices of session
# Inputs:
#     averagePrices   :   np.array with bitcoin data pts = 0.5(open+close)
#     voFracsMax      :   np.array with volume data pts = volume[ii]/maxVolume
#     tradeFracsMax   :   np.array with volume data pts = volume[ii]/maxVolume
#     n               :   length of data (bc already have)
# Outputs:
#     walk            :   predicted values of asset using random walk
    
    walk = np.zeros(n)
    volMax = volumes[0]
    tMax = trades[0]
    for ii in range(2,n):
    # ith session = predict ith close
    # get open[ii], volumes[:ii], trades[:ii], closes[:ii]
        vol = volumes[ii-1]; trade = trades[ii-1];
        if volMax < volumes[ii]:
            volMax = vol
        if tMax < trade:
            tMax = trade
        data1 = closes[ii-2]; data2 = closes[ii-1];
        mu1,mu2 = deltaMu(closes[:ii])
        dVar = deltaVar(mu1,mu2,data1,data2)
        sigma = volatility(vol/volMax,trade/tMax)
        cine = signVal(opens[ii-1:ii+1],closes[ii-1])
        # calculates sign of change as 
        value = abs((mu2-mu1)*random.uniform(0,1) + dVar/math.sqrt(abs(dVar))*random.uniform(0,1))
        if value/opens[ii] >= sigma:
            walk[ii] = (1+sigma)*opens[ii]
        else:
            walk[ii] = opens[ii] + value*cine
    
    return walk

def dummyTest(opens,closes):

    open

    return

driver()