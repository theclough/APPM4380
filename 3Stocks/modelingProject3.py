# Stock Analysis

import numpy as np
import matplotlib.pyplot as plt

def data2Array(csvFile,n=0):
# Inputs:
#     csvFile :   name of .csv file with Bitcoin data in 5 min intervals
#     n       :   number of points from data (default 0 = take all datapoints)
# Outputs:
#     data    :   np.array of all data

    with open('5min.csv','r') as fp:
        data = fp.readlines()
        if n != 0:
            data = data[1:n]
    return data

def postProcess(array):
# Inputs:
#     array   :   array from data2Array
# Outputs:
#     highPrices  :   np.array of high prices of stock
#     lowPrices   :   np.array of low prices of stock
#     openPrices  :   np.array of open prices of stock
#     closePrices :   np.array of close prices of stock
#     volumes     :   np.array of volume for each transactions
#     times       :   np.array of time of each transaction

    return

