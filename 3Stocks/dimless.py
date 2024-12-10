import math
import pandas
import random
import numpy as np
import matplotlib.pyplot as plt

def dimless(BTCData):

    l = len(BTCData)
    volumes = np.zeros(l)
    maxVol = volumes[0]
    for ii in range(l,0,-1):
        vol = volumes[ii]
        if vol > maxVol:
            maxVol = vol
        volumes[ii] = vol/volumes[ii-1]
        

    for dataPt in BTCData:
        


# volFrac, pSlope, p2Slope, concavity
 
# time of day/month/year
# fed rate, CCI