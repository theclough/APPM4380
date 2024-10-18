import math
import numpy as np
import matplotlib.pyplot as plt

def driver():
# runs findCenter()

    dx = 69; mx = 55;
    dy = 6; my = 45;
    Xs = [45.65,50.54,56.87]
    Ys = [27.46,32.70,36.97]

    X1s = np.zeros(3)
    Y1s = np.zeros(3)
    
    # ct = 0
    # for x,y in zip(Xs,Ys):
    #     X1s[ct] = getDecimal(0,0,x)
    #     Y1s[ct] = getDecimal(0,0,y)
    #     ct += 1

    r,(xC,yC) = findCenter(Xs,Ys)
    print(r, (-xC,-yC))
    plt.plot(Xs + [-xC],Ys + [-yC],'ro')
    plt.show()

def getDecimal(deg,min,sec):
# returns decimal value for lat/long

    return deg + (min/60) + (sec/3600)

def findCenter(Xs,Ys, tol=10**(-6)):
# finds center of circle defined by 3 *different* points
# Inputs:
#     -Xs : array of x values
#     -Ys : array of y values
#     -tol : tolerance check for 0
# Outputs:
#     (xC,yC) : tuple of coords for center
    x0,x1,x2 = Xs
    y0,y1,y2 = Ys
    # get points

    x1 -= x0; x2 -= x0;
    y1 -= y0; y2 -= y0
    # subtract off (x0,y0)
    
    xC = 0.5*(y1*(x2**2+y2**2)-y2*(x1**2+y1**2))/(x1*y2-x2*y1)
    yC = 0.5*(x1*(x2**2+y2**2)-x2*(x1**2+y1**2))/(x2*y1-x1*y2)
    # use formula (derived by treating (x0,y0) = (0,0))
    r = math.sqrt(xC**2+yC**2)
    xC -= x0
    yC -= y0
    # - (x0,y0) to shift back into original coordinate system

    if abs(xC) < tol:
        if abs(yC) < tol:
            xC,yC = (0,0)
        else:
            xC = 0
    if abs(yC) < tol:
        yC = 0
    # check if xC and/or yC below tolerance
        
    return r,(xC,yC)
    

def test():
# test function on unit circle (center : (0,0))

    print(getDecimal(6,44,59))
    return
    
    f = lambda y,x=1: math.cos(math.pi*x/y)
    g = lambda y,x=1: math.sin(math.pi*x/y)
    
    Xs = [f(3),f(17),f(-5)]
    Ys = [g(3),g(17),g(-5)]
    tol = 10**(-10)
    
    print(findCenter(Xs,Ys,tol))

driver()