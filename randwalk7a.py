'''
Random walk until distance D reached, in 1/2/3 dimensions 
'''

import time
import numpy as np
#from graphics import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import RWmods
PlotMe =  True 

def mainstream():
  #print ("Clock =", time.clock())
  plt.close('all')

  rDist = 7                 # set distance here
  rSeed = -1                 # random number seed

  print ("Distance =", rDist, "; seed =", rSeed)

  #RandomWalk (1, rSeed, rDist)        # 1 dimension
  #RandomWalk (2, rSeed, rDist)        # 2 dimensions
  RandomWalk (3, rSeed, rDist)         # 3 dimensions
  
  print ("Ctrl+D to return to IDLE")

  print ("==="*18)
  return;



def RandomWalk (dimen, seed, dist):
  #stime = time.clock()
  stimeWC = time.perf_counter()   # wall clock
  stimePT = time.process_time()   # processor time
  print ("---"*18)
  
  #xList = [0]; yList = [0]; zList = [0]
  xList, yList, zList, nSteps = RWmods.RandomWalkDist(dimen, seed, dist)
  print ("Step count =", nSteps)
  '''
  for S in range (0, nSteps + 1):
    print (S, xList[S], yList[S], zList[S])
    if S > 100: break
  '''  
  fig = plt.figure()
  fig.suptitle("Random walk to D = " + str(dist) + " (seed = " + str(seed) + ")  ~ Steps = " + str(nSteps)) 
  #ax = fig.gca(projection='3d')  deprecated - use next line
  ax = fig.add_subplot(111, projection='3d')

  '''
  print("Dims =", dimen, ";  X,Y,Z = (", X, Y, Z, ')' )
  print("            Distance =", distance)
  print("    [max dist", distMax, "@ (", dmaxX, dmaxY, dmaxZ, ") on step", stepMax, "]")
  '''
  print("xList =", xList)
  print("yList =", yList)
  print("zList =", zList)

  X = xList[nSteps]; Y = yList[nSteps]; Z = zList[nSteps]
  distance = np.sqrt(X*X + Y*Y + Z*Z) 
  ax.plot(xList, yList, zList, linewidth=0.8, label="Path")
  ax.legend()
  xList = [0, X]; yList = [0,Y]; zList = [0,Z]
  ax.plot(xList, yList, zList, '--', linewidth=1, color="brown")
  plt.plot([0], [0], [0], marker='o', markersize=5, color="blue")
  msize =6
  if X < 0: msize -= 1
  else: msize += 2
  if Y > 0: msize -= 1
  else: msize += 2
  if Z < 0: msize -= 1
  else: msize += 1
  print("msize =", msize)
  plt.plot([X], [Y], [Z], marker='*', markersize=msize, color="red")
  coordStr = " (" + str(X) + "," + str(Y) + "," + str(Z) + ")"
  ax.text(X, Y, Z, coordStr, color='red')   #   "," + str(Z) + ")"
  distStr = " dist=" + str(round(distance,2))
  ax.text(X/2, Y/2, Z/2, distStr, color='brown')
  '''
  xList = [0, dmaxX]; yList = [0,dmaxY]; zList = [0,dmaxZ]
  ax.plot(xList, yList, zList, '--', linewidth=1, color="magenta")
  plt.plot([dmaxX], [dmaxY], [dmaxZ], marker='^', markersize=5, color="magenta")
  coordStr = " (" + str(dmaxX) + "," + str(dmaxY) + "," + str(dmaxZ) + ")"
  ax.text(dmaxX, dmaxY, dmaxZ, coordStr, color='magenta')
  distStr = " dmax=" + str(round(distMax,2))
  ax.text(dmaxX/1.5, dmaxY/1.5, dmaxZ/1.5, distStr, color='magenta')
  '''

  #etime = time.clock()
  etimeWC = time.perf_counter()   # wall clock
  etimePT = time.process_time()   # processor time
  dtimeWC = etimeWC - stimeWC
  dtimePT = etimePT - stimePT  
  print ("DurationWC =", dtimeWC)
  print ("DurationPT =", dtimePT)
  
  if PlotMe: plt.show()
  
mainstream()
