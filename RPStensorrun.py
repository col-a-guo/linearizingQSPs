#Equivalent to RPSrun but using generalized format

import generalizedNDimRun as NR

import time
start = time.process_time()

import matplotlib.pyplot as plt

changerates = {
        "0-0-0":0,
        "0-1-0":.25,
        "0-2-0":.5,
        "1-0-0":.25,
        "1-1-0":0,
        "1-2-0":.5,
        "2-0-0":.5,
        "2-1-0":0,
        "2-2-0":1,
    
        "0-0-1":1,
        "0-1-1":.375,
        "0-2-1":.5,
        "1-0-1":.375,
        "1-1-1":1,
        "1-2-1":0,
        "2-0-1":.5,
        "2-1-1":.5,
        "2-2-1":0,
    
        "0-0-2":0,
        "0-1-2":.375,
        "0-2-2":0,
        "1-0-2":.375,
        "1-1-2":0,
        "1-2-2":.5,
        "2-0-2":0,
        "2-1-2":.5,
        "2-2-2":0,
        } 

initialDist = [.33,.33,.34]
dim = 2
nState = NR.Rat(3, changerates, 100, dim, initialDist)
aThing1 = nState.average(initialDist, 40, 500, .5)


x = range(0,40)
y = aThing1
plt.xlabel("Time")
plt.ylabel("Distribution")
plt.title("Rock Paper Scissors")
plt.plot(x,[pt[0] for pt in y],label = 'Rock')
plt.plot(x,[pt[1] for pt in y],label = 'Paper')
plt.plot(x,[pt[2] for pt in y],label = 'Scissors')
plt.legend(loc='upper right')
plt.show()


stop = time.process_time()
print(str(stop-start))
