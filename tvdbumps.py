# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 08:19:31 2020

@author: r2d2go
"""

#Compares error to likely source of error: Number of "bumps", i.e. times where player count becomes negative and must be adjusted

import newRun as NR

import time
start = time.process_time()
import random
import matplotlib.pyplot as plt


def genRates(n):
    #randomly generate movement rates
    winrates = []
    loserates = []
    counterrates = []
    initialDist = []
    for i in range (n):
        winrates.append([])
        loserates.append([])
        counterrates.append([])
        initialDist.append(0)
        for j in range (n):
            winrates[i].append(0)
            loserates[i].append(0)
            counterrates[i].append(0)
    totalDist = 0
    for i in range (n):
        for j in range (n):
            winrates[i][j] = random.uniform(0,1)
            winrates[j][i] = 1-winrates[i][j]
        winrates[n-1][i] = 0
        winrates[i][n-1] = 1
        totallose = 0
        totalcounter = 0
        for j in range (n-1):
            loserates[i][j] = random.normalvariate(float(1/n),.1/n)
            totallose += loserates[i][j]
            counterrates[i][j] = random.normalvariate(float(1/n),.1/n)
            totalcounter += counterrates[i][j]  
        loserates[i][n-1] = 1-totallose
        counterrates[i][n-1] = 1-totalcounter
        initialDist[i] = i*random.normalvariate(2.0/(n**2-n),0.2/(n**2-n))
        totalDist += initialDist[i]
    totalDist -= initialDist[0]
    initialDist[0] = 1-totalDist
    return([winrates,loserates,counterrates,initialDist])


listOfRates = genRates(10)

winrates = listOfRates[0]
loserates = listOfRates[1]
counterrates = listOfRates[2]
initialDist = listOfRates[3]

#High player count games for purposes of comparison
nState = NR.Rat(10, winrates, loserates, counterrates, 50, initialDist)
aThingA = nState.average(initialDist, 40, 25200, .5)

totalAve = [0,0,0,0,0,0,0,0,0,0]
for j in range(10):
    for i in range(5):
        totalAve[j] += aThingA[len(aThingA)-i-1][j]
    totalAve[j] = totalAve[j]/5

bumplist = []
thingList = []
#Generate further low-player games and track number of "bump" errors
for bleh in range(1):
    for i in (range(1,2)):
        nState = NR.Rat(10, winrates, loserates, counterrates, 20, initialDist)
        aThing = nState.average(initialDist, 40, int(25200/i), .5)
        TVD = 0
        ave = [0,0,0,0,0,0,0,0,0,0]
        for j in range(10):
            for ind in range(5):
                ave[j] += aThing[len(aThing)-ind-1][j]
            ave[j] = ave[j]/5
        for ind in range(5):
            TVD += abs(ave[ind]-totalAve[ind])
        thingList.append(TVD/2)
        bumplist.append(nState.bumps)

y = bumplist
x = thingList
plt.ylabel("Number of Corrections")
plt.xlabel("Final Total Variation Distance from High Accuracy Run (t=40)")
plt.title("Corrections vs TVD (deck count 10, player count 10+3n, 0 < n < 11, 10*504000 runs each)")
plt.scatter(x,y)
plt.show()

stop = time.process_time()
print(str(stop-start))
