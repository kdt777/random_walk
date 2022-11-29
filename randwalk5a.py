'''
Every permutation of random walk for N steps (graph if 1 or 2 dims)
'''

import time
import numpy as np
#from sympy import *
import matplotlib.pyplot as mplt
from mpl_toolkits.mplot3d import Axes3D

nStep = 4                       # set number of steps here
aSize = nStep * 2 + 1           # size of xyz array

def mainstream():

  mplt.close('all')
  figa, ax = mplt.subplots(2, 2, figsize=(4,3)) 
  figa.suptitle("Random Walk for " + str(nStep) + " steps")
  
  AllWalks (1, ax)                 # 1 dimension
  AllWalks (2, ax)                 # 2 dimensions
  AllWalks (3, ax)                 # 3 dimensions

  mplt.show()
  
  print ("Ctrl+D to return to IDLE")
  print ("==="*18)
  return;

def AllWalks (dimen, ax):

  print ("__"*18)
  print (nStep, "steps in", dimen, "dimensions")
  
  #stime = time.clock()
  stimeWC = time.perf_counter()   # wall clock
  stimePT = time.process_time()   # processor time

  B = dimen * 2                     # Base = 2, 4 or 6
  N = B ** nStep
  print ("      ==> ", N, "permutations")
  print ("      ==> ", aSize ** dimen, "positions")

  xyzCount = np.zeros((nStep*2+1, nStep*2+1, nStep*2+1), np.int32)    #, order='F')
  print ("Type =", type(xyzCount), ";  shape =", xyzCount.shape)
  Dsum = 0.0; xList = []; yList = []; dList = []; d2List = [] 
  
  for I in range (0, N):
    #print(I)
    Istring = str_base(I,B)         # I in base 2, 4 or 6 for 1, 2 or 3 dimensions
    #print (Istring, type(Istring), len(Istring))
    for J in range (1, N):
      if len(Istring) < nStep:
        Istring = "0" + Istring     # pad with left zeros
      else:
        break

    Dist2 = AnalyseIstring(I, Istring, xyzCount, xList, yList)    # returns Distance squared
    Dist = Dist2 ** 0.5
    dList.append(Dist)
    if Dist2 not in d2List:
      d2List.append(Dist2) 
    #print ("Dist =", Dist, Dist2)
    Dsum += Dist
    
  Davg = Dsum / N
  print ("Dsum =", Dsum, "; Davg =", Davg)
  #print (" dList=", dList)
  d2List.sort() 
  print ("d2List=", d2List)
  
  #print ("xList =", xList); #print ("yList =", yList)
  xyzPlot (ax, xyzCount, dimen, Davg, xList, yList, dList, d2List)
  
  etimeWC = time.perf_counter()   # wall clock
  etimePT = time.process_time()   # processor time
  dtimeWC = etimeWC - stimeWC
  dtimePT = etimePT - stimePT  
  print ("DurationWC =", dtimeWC)
  print ("DurationPT =", dtimePT)
  
  #plt.show()

def AnalyseIstring(permutn, Istring, xyzCount, xList, yList):
  Astring = Istring.replace("0","E")
  Astring = Astring.replace("1","W")
  Astring = Astring.replace("2","N")
  Astring = Astring.replace("3","S")
  Astring = Astring.replace("4","U")
  Astring = Astring.replace("5","D")
  #print (repr(permutn).rjust(4), ":   ", Istring, Astring, end='') 
  #print (repr(permutn)) 
  X = int(Istring.count("0") - Istring.count("1"))
  Y = int(Istring.count("2") - Istring.count("3"))
  Z = int(Istring.count("4") - Istring.count("5"))
  DD = X*X + Y*Y + Z*Z
  #print ("   (X,Y,Z) =", X, Y, Z, " D^2 =",DD, "; D =", D)
  xyzCount[X + nStep, Y + nStep, Z + nStep] += 1
  if nStep < 7 or (X >= 0 and Y >= 0):
    xList.append(X)
    yList.append(Y) 
  return (DD)

def xyzPlot(ax, xyzCount, Dim, DistAvg, xList, yList, dList, d2List):
  #print ("Dim/xList =", Dim, xList)
  N=aSize
  for Z in range (0, N):
    if Dim > 2 or Z == (aSize - 1) / 2:
      print ("For Z =", Z)
      for Y in range (0, N):
        if Dim > 1 or Y == (aSize - 1) / 2:
          print ("   xyzCount:", xyzCount[0:N,Y,Z])

  Base = Dim * 2                       # Base = 2, 4 or 6
  Npmu = Base ** nStep                 # number of permutations

  NZC = np.count_nonzero(xyzCount)
  MaxV = np.max(xyzCount)
   
  print("NZC =", NZC)                  # number of occupied bins
  print("max =", MaxV)                 # maximum value

  endBin = nStep + 1.5
  if nStep < 6:
    startBin = -nStep - 0.5
  else:
    startBin = -0.5
                   
  if Dim == 1:                # histogram of 1 dim walk
    #mplt.subplot(121)
    ax[0,0].set_title('1 Dimension: ' + str(Npmu) + ' permutations')
    bins = np.arange(startBin, endBin, 1)          
    #Hn, Hbins, Hpatches = mplt.hist(xList, bins, align='mid')    # , 50, normed=1, facecolor='green', alpha=0.75)
    Hn, Hbins, Hpatches = ax[0,0].hist(xList, bins, align='mid', color='w', edgecolor='b', hatch='/')
    print ("         N =", Hn)
    print ("      Bins =", Hbins)
    #print ("   Patches =", Hpatches)
    mplt.xticks(range(-nStep, nStep + 1))
    #mplt.xlabel("Mean distance = " + str(round(DistAvg,3)))
    ax[0,0].text(nStep, MaxV, str(nStep) + ' steps', ha="right", style='italic')
    ax[0,0].text(nStep, MaxV * 0.9, str(NZC) + ' locns', ha='right', style='italic')
    ax[0,0].set_xlabel("Mean distance = " + str(round(DistAvg,3)))

    bins = np.arange(-0.5, endBin, 1)
    Hn, Hbins, Hpatches = ax[1,0].hist(dList, bins, align='mid', rwidth=0.25, color='cyan')
    print ("        dN =", Hn)
    print ("     dBins =", Hbins)
    DistCt = np.count_nonzero(Hn) 
    ax[1,0].text(nStep, max(Hn) * 0.9, str(DistCt) + ' distances', ha='right', style='italic')
    #ax[1,0].set_xticks([])    
    ax[1,0].grid(axis='y')
    
  if Dim == 2:                # histogram of 2 dim walk
    ax[0,1].set_title('2 Dimensions: ' + str(Npmu) + ' permutations')
    ax[0,1].set_aspect("equal")
    ax[0,1].patch.set_facecolor('lightgrey')
    bins = np.arange(startBin, endBin, 1)
    my_cmap = mplt.cm.plasma_r      #.GnBu      #.plasma_r   #.jet
    hist2, xbins2, ybins2, im2 = ax[0,1].hist2d(xList, yList, bins, cmin=1, cmap=my_cmap) 
    print ("      Bins =", bins)
    #print ("      Hist =", hist2)
    print ("        im =", im2)
    for i in range(len(bins)-1):
      for j in range(len(bins)-1):
        #print ("      ", i, j, hist2[i,j], "  float = ", is_numbr(hist2[i,j])) 
        if is_numbr(hist2[i,j]):
          #print (i, j, hist2[i,j], bins[i]+0.5, bins[j]+0.5)
          LocnCt = int(hist2[i,j])
          if LocnCt < 100:
            fSize = 10
          elif LocnCt < 1000:
            fSize = 8
          else:
            fSize = 7
          ax[0,1].text(bins[j]+0.5, bins[i]+0.5, LocnCt,         
                       color="w", ha="center", va="center", fontweight="bold", fontsize=fSize, style='italic')        
    ax[0,1].text(nStep, nStep, str(nStep) + ' steps', ha="right", style='italic')      
    ax[0,1].text(nStep, nStep * 0.9, str(NZC) + ' locns', ha="right", style='italic')
    ax[0,1].set_xlabel("Mean distance = " + str(round(DistAvg,3)))

    bins = "auto"     #np.arange(-binw/2, max(dList)+binw, binw) 
    Hn, Hbins, Hpatches = ax[1,1].hist(dList, bins, align='mid', rwidth=0.5, log=True, color='g')
    print ("     dBins =", Hbins)
    print ("        dN =", Hn)
    DistCt = np.count_nonzero(Hn)
    #LabelPos = np.sqrt(max(Hn)); LabelAdj = LabelPos / 2.0
    LabelPos = 3.0; LabelAdj = 1.5
    ax[1,1].text(nStep * 0.9, max(Hn) * 0.9, str(DistCt) + ' distances', ha='right', style='italic')
    for idx, D2 in enumerate(d2List):
      print ("idx, D2 =", idx, D2)      # d2Ct[idx]) 
      D = np.sqrt(D2)
      LabelAdj *= -1
      if int(D) * int(D) == D2:
        ax[1,1].text(D*0.98, (LabelPos+LabelAdj), str(int(D)), ha='left', size=6, weight='bold') 
        #ax[1,1].text(D*0.95, d2Ct[idx]*0.5 - 3.0, str(D), ha='left', style='italic')
      else:
        #ax[1,1].text(D*0.95, (LabelPos+LabelAdj), "\x2F" + str(D2), ha='left', style='italic')   # sqrt sign
        rawRoot = r"$\sqrt{" + str(D2) + "}$"
        ax[1,1].text(D*0.95, (LabelPos+LabelAdj), rawRoot, ha='left', size=6, style='italic')
    ax[1,1].set_xticks([])  
    ax[1,1].grid(axis='y')   #b=None, which='major', axis='y')
    #ax[1,1].yscale('log')
    #ax[1,1].text(1.5, 1.5, 'hello world: $\int_0^\infty e^x dx$', size=24, ha='center', va='center')
    ''' 
    ax2.text(0, 0, "here is 0,0", color="w", ha="center", va="center", fontweight="bold")
    ax2.text(-1.0, -1.0, "here is 1,1", color="k", ha="center", va="center", fontweight="bold")
    ax2.text(2, 2.2, "here is 2,2", color="r", ha="center", va="center", fontweight="bold")
    '''
  #ax[2].set_title('3 Dimensional')

def is_numbr(val):
    try:
      int(val)
    except ValueError:
      return False
    else:
      #print("          val =", val, int(val*val))
      return True    

def digit_to_char(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('a') + digit - 10)

def str_base(number,base):
    if number < 0:
        return '-' + str_base(-number, base)
    (d, m) = divmod(number, base)
    #print ("d, m =", d, m) 
    if d > 0:
        return str_base(d, base) + digit_to_char(m)
    return digit_to_char(m)
  
mainstream()
