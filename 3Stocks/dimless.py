import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

'''
    for ALL slopes, numerator is in MINUTES
'''

def driver():

    l,xVals,opens,highs,lows,closes,volumes = initialize('BTCMin.csv','min')
    # picOfAllData(l, xVals, highs, lows, opens, closes)
    dataManip(l,opens,highs,lows,closes,volumes)

def initialize(filename, tInt):
    
    times = {'min': 1, 'day': 1440, 'year': 525600}
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
    closes = np.zeros(l+1)
    volumes = np.zeros(l)
    for stuff,ii in zip(data,range(l)):
        dataPt = stuff.strip('\n').split(',')
        opens[ii] = float(dataPt[2])
        highs[ii] = float(dataPt[3])
        lows[ii] = float(dataPt[4])
        closes[ii+1] = float(dataPt[5])
        volumes[ii] = float(dataPt[6])
    closes[0] = opens[0]
    
    return l,xVals,opens,highs,lows,closes,volumes

def dataManip(l,opens,highs,lows,closes,volumes):
# Inputs:
#     various np.array()s of data
# Outputs:
#     volFracs    :   size (l-1)    - volume[session]/maxVolume
#     volatilitys :   size (l)      - volatility[session] calculated as (high-low)/avg price = 2*(high-low)/(open+close)

    maxVol = -1
    volatilitys = np.zeros(l)
    volFracs = np.zeros(l-1)
    for ii in range(l):
        vol = volumes[ii]
        if maxVol < vol:
            maxVol = vol
        if ii != 0:
            volFracs[ii-1] = volumes[ii]/volumes[ii-1]
        volatilitys[ii] = 2.*(highs[ii]-lows[ii])/(opens[ii]+closes[ii])
    volFracsMax = volumes/maxVol

    # # plot stuff
    # plt.plot(volFracs,volatilitys[1:],'bo',markersize=1)
    # plt.show()
    # plt.semilogx(volFracs,volatilitys[1:],'bo',markersize=1)
    # plt.show()
    # plt.semilogy(volFracs,volatilitys[1:],'bo',markersize=1)
    # plt.show()
    # plt.loglog(volFracs,volatilitys[1:],'bo',markersize=1)
    # plt.show()

    # volFracsMax vs volatility in session
    X = np.log(volFracsMax).reshape(-1,1)
    y = np.log(volatilitys)
    linFit = LinearRegression().fit(X,y)
    print(linFit.score(X,y))
    print(linFit.coef_)
    print(linFit.intercept_)

    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

    # volFracsMax vs volatility in previous session
    X = np.log(volFracsMax[1:]).reshape(-1,1)
    y = np.log(volatilitys[:-1])
    linFit = LinearRegression().fit(X,y)
    print(linFit.score(X,y))
    print(linFit.coef_)
    print(linFit.intercept_)

    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

    # volFracs vs volatility in session
    X = np.log(volFracs).reshape(-1,1)
    y = np.log(volatilitys[1:])
    linFit = LinearRegression().fit(X,y)
    print(linFit.score(X,y))
    print(linFit.coef_)
    print(linFit.intercept_)

    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    
    # volFracs vs volatility in previous session
    X = np.log(volFracs).reshape(-1,1)
    y = np.log(volatilitys[:-1])
    linFit = LinearRegression().fit(X,y)
    print(linFit.score(X,y))
    print(linFit.coef_)
    print(linFit.intercept_)
    

    # # volFracs vs volatility in session
    # X = np.log(volFracs).reshape(-1,1)
    # linFit = LinearRegression().fit(X,np.log(volatilitys[1:]))
    # print(linFit.score(X,np.log(volatilitys[1:])))
    # print(linFit.coef_)
    # print(linFit.intercept_)     

    # reg = linFit.coef_*volFracs + linFit.intercept_
    # plt.plot(range(l),volatilitys,'go',markersize=2)
    # plt.plot(range(l),reg,'bo',markersize=1)
    # plt.show()


def picOfAllData(l,xVals,highs,lows,opens,closes):
# run to see what does

    plt.plot(xVals, highs, 'go', markersize=1)
    plt.plot(xVals, lows, 'ro', markersize=1)
    plt.plot(xVals, opens, 'b-', linewidth=1)
    plt.plot(range(l+1), closes, 'm-', linewidth=1)
    plt.show()

driver()