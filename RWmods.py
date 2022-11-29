def RandomWalk (dimen, seed, numstp):

  # take a hike in 1, 2 or 3 dimensions for specified number of steps
  # returns lists of X, Y and Z integer values being the coordinates of path taken,
  #    plus distance from start at final position (and maximum distance during walk)
  
  import numpy as np
  
  X, Y, Z = 0, 0, 0
  xList = [0]; yList = [0]; zList = [0]

  if seed >= 0:
    np.random.seed(seed)
  randHi = dimen * 2
  distMax = 0.0

  for N in range (0, numstp):
    dir = np.random.randint(0, randHi)
    #print(N, dir)
    if dir == 0:    # east
      X += 1
    elif dir == 1:  # west
      X -= 1
    elif dir == 2:  # north
      Y += 1
    elif dir == 3:  # south
      Y -= 1
    elif dir == 4:  # up
      Z += 1
    elif dir == 5:  # down
      Z -= 1    
    else:           # never!
      print ("*** invalid value ***") 
    #print("   coords = (", X, Y, Z, ')' )
    xList.append(X); yList.append(Y); zList.append(Z)  
    distance = np.sqrt(X*X + Y*Y + Z*Z)
    if distance > distMax:
      distMax = distance
      stepMax = N + 1
      dmaxX=X; dmaxY=Y; dmaxZ=Z
    
  return xList, yList, zList, distance, distMax


def HistXYZ (xList, yList, zList, onlyPos=False):
  
  # analyse lists of X,Y,Z values to create histogram list for each location identified
  # returns a list of unique (X,Y,Z) tuples and a list of corresponding counts
  
  N = 0; xyzList = []; hList = []; xyzCount = 0 
  for X in xList:
    XYZtup = (xList[N], yList[N], zList[N])
    if onlyPos:
      if xList[N] < 0 or yList[N] < 0 or zList[N] < 0:
        N += 1
        continue
    idx = -1
    for M in range (0, xyzCount):
      if xyzList[M] == XYZtup:
        idx = M
        hList[idx] += 1
        break
    if idx < 0: 
        xyzList.append(XYZtup)
        hList.append(1) 
        xyzCount += 1
        
    N += 1
    
  return xyzList, hList  
  
def RandomWalkDist (dimen, seed, dist):

  # take a hike in 1, 2 or 3 dimensions for until a given distance is reached
  # returns lists of X, Y and Z integer values being the coordinates of path taken,
  #    plus number of steps to attain the distance specified
  
  import numpy as np
  
  X, Y, Z = 0, 0, 0
  xList = [0]; yList = [0]; zList = [0]

  if seed >= 0:
    np.random.seed(seed)
  randHi = dimen * 2

  for N in range (0, 10000):
    dir = np.random.randint(0, randHi)
    #print(N, dir)
    if dir == 0:    # east
      X += 1
    elif dir == 1:  # west
      X -= 1
    elif dir == 2:  # north
      Y += 1
    elif dir == 3:  # south
      Y -= 1
    elif dir == 4:  # up
      Z += 1
    elif dir == 5:  # down
      Z -= 1    
    else:           # never!
      print ("*** invalid value ***") 
    #print("   coords = (", X, Y, Z, ')' )
    xList.append(X); yList.append(Y); zList.append(Z)  
    distance = np.sqrt(X*X + Y*Y + Z*Z)
    if distance >= dist:
      stepCt = N + 1
      break

  print ("...", dist, distance, N, stepCt)
  
  return xList, yList, zList, stepCt

def RandomWalk2NO (seed, numstp, radGran):

  # non-orthoganal random walk in 2 dimensions for specified number of steps,
  #     allowing specified number of compass points (radial granuality)
  # returns lists of X and Y values being the coordinates of path taken,
  #     plus distance from start at final position (and maximum distance during walk)
  
  import numpy as np  

  X, Y = 0.0, 0.0
  xList = [0.0]; yList = [0.0]                # non-integers
  #xfList = [0.0]; yfList = [0.0]              # floats
  
  if seed >= 0:
    np.random.seed(seed)
  randHi = 4  # dimen * 2
  distMax = 0.0; plotAdj = np.sqrt(numstp) / 400.0

  for N in range (0, numstp):
    dirN = np.random.randint(0, radGran)   # randHi
    dirA = 2.0 * np.pi * dirN / radGran
    #print("   N, dirN/A =", N, dirN, dirA)
    X = X + np.cos(dirA)
    Y = Y + np.sin(dirA) 
    #print("      coords = (", X, Y, ')' )
    xList.append(X); yList.append(Y)
    
    '''if numstp < 100:
      modN = N%6 - 3.0 + 0.5  # => -2.5 ~ 2.5 by 1.0
      pltAdj = plotAdj * modN
      #print("modN/pltAdj =", modN, pltAdj)
      #plotAdj *= -1
      xfList.append(X); yfList.append(Y)
      xfList.append(X + pltAdj); yfList.append(Y + pltAdj)'''
    distance = np.sqrt(X*X + Y*Y)
    if distance > distMax:
      distMax = distance
      stepMax = N + 1
      dmaxX=X; dmaxY=Y

  return xList, yList, distance, distMax, dmaxX, dmaxY 
