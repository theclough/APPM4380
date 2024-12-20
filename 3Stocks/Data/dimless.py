import numpy as np
import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression

'''
    for ALL slopes, numerator is in MINUTES
'''

def driver():

    times = {'min': 1, 'day': 1440, 'year': 525600}
    tInt = times['day']
    l,xVals,opens,highs,lows,closes,volumes,trades = initialize('BTCDay.csv',tInt)
    # picOfAllData(l, xVals, highs, lows, opens, closes)
    dataManip(l,tInt,opens,highs,lows,closes,volumes,trades)

    return

def initialize(filename, tInt):
    
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
    trades = np.zeros(l)
    for stuff,ii in zip(data,range(l)):
        dataPt = stuff.strip('\n').split(',')
        opens[ii] = float(dataPt[2])
        highs[ii] = float(dataPt[3])
        lows[ii] = float(dataPt[4])
        closes[ii+1] = float(dataPt[5])
        volumes[ii] = float(dataPt[6])
        trades[ii] = int(dataPt[7].split('.')[0])
    closes[0] = opens[0]
    
    return l,xVals,opens,highs,lows,closes,volumes,trades

def dataManip(l,tInt,opens,highs,lows,closes,volumes,trades):
# Inputs:
#     various np.array()s of data
# Outputs:
#     volFracs    :   size (l-1)    - volume[session]/maxVolume
#     volatilitys :   size (l)      - volatility[session] calculated as (high-low)/avg price = 2*(high-low)/(open+close)

    maxVol = -1; maxTrade = -1
    volatilitys = np.zeros(l)
    # pSlopes = np.zeros(l-1)
    # concavitys = np.zeros(l-2)
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
        #         concavitys[ii-2] = (pSlopes[ii-1]-pSlopes[ii-2])
        volatilitys[ii] = (highs[ii]-lows[ii])/avgVal
    volFracsMax = volumes/maxVol
    tradeFracsMax = trades/maxTrade
    
    # plot stuff
    # plt.plot(volFracsMax,volatilitys,'bo',markersize=1)
    # plt.show()
    # plt.semilogx(volFracsMax,volatilitys,'bo',markersize=1)
    # plt.show()
    # plt.semilogy(volFracsMax,volatilitys,'bo',markersize=1)
    # plt.show()
    plt.loglog(volFracsMax,volatilitys,'bo',markersize=2)
    plt.xlabel('volume []')
    plt.ylabel('volatility []')
    plt.savefig('dimlessVol.png')
    
    # testX = np.log(np.stack((volFracsMax,tradeFracsMax) ,axis=1))
    # print(testX.shape)
    # return

    # best so far
    # X = np.log(np.stack((volFracsMax,tradeFracsMax) ,axis=1))
    # y = np.log(volatilitys)
    # linFit = LinearRegression().fit(X,y)
    # print(linFit.score(X,y))
    # print(linFit.coef_)
    # print(linFit.intercept_)

    # testing
    # X = np.log(np.stack((volFracsMax,tradeFracsMax) ,axis=1))
    # y = np.log(volatilitys)#/volatilitys[:-1])
    # linFit = LinearRegression().fit(X,y)
    # print(linFit.score(X,y))
    # print(linFit.coef_)
    # print(linFit.intercept_) 


def volFracsTesting(volFracs,volFracsMax,volatilitys):
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