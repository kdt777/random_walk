'''
Perform many random (non-orthagonal) walks of N steps in 2 dims 
and average the distances
'''

import time, os
import numpy as np
import matplotlib.pyplot as mplt
import RWmods

nStep = 10                      # set number of steps here
radPts = 8                      # number of radial directions (compass points)
nWalk =  3  #* nStep             # set number of walks here
#nDims = 3                        # set to 1/2/3 dimensions

sSeed = 0                        # start seed value
#aSize = nStep * 2 + 1           # size of xyz array

def mainstream():

  mplt.close('all')
  figa, ax = mplt.subplots(1, 2, figsize=(4,3)) 
  figa.suptitle(str(nWalk) + "2-D Random Walks for " +
                str(nStep) + " steps -- " + str(radPts) + " pts")
  
  xList = []; yList = []; dList = [] 
  
  for Seed in range (sSeed, sSeed + nWalk):
    #print("  Seed =", Seed) 
    xLst, yLst, Dist, Dmax, dmaxX, dmaxY = RWmods.RandomWalk2NO(Seed, nStep, radPts)
    #print("    Posn =", xLst[nStep], yLst[nStep], zLst[nStep], end="")
    #print("    Dist =", Dist, "    Dmax =", Dmax)
    xList.append(xLst[nStep]); yList.append(yLst[nStep])
    dList.append(Dist)
    #if Dist > 14:
    print("  D =", Dist, "  at:", xLst[nStep], yLst[nStep]) 
    
  #print(" X values:", xList); print(" Y values:", yList); print(" Z values:", zList); print("Distances:", dList)

  #xyzHist (ax, nDims, xList, yList, zList, dList)
    
  mplt.show()
  
  print ("Ctrl+D to return to IDLE")
  print ("==="*18)
  return;

def xyzHist(ax, Dim, xList, yList, zList, dList):

  print(nStep, "steps; ", Dim, "dims; ", nWalk, "walks.")
  DistAvg = np.mean(dList)
  print("   Mean distance =", DistAvg)
  DistMax = int(max(dList) + 1) 
  print("    Max distance =", DistMax)
  print("      coord list =", str(len(xList)))
  print("       dist list =", str(len(dList)))
  print("_"*12) 

  if nWalk > 100000:
    return                    # break out without plotting

  endBin = DistMax + 1.5      # nStep + 1.5
  startBin = -DistMax - 0.5   # -nStep - 0.5
  
  if nStep > 6:
    logYscale = True
  else:
    logYscale = False 
                   
  if Dim == 1:                # histogram of 1 dim walk
    ax[0].set_title('1 Dimension: ' + str(nWalk) + ' walks')
    bins = np.arange(startBin, endBin, 1)          
    Hn, Hbins, Hpatches = ax[0].hist(xList, bins, align='mid', log=logYscale,
                                     color='w', edgecolor='b', hatch='/')
    #print ("         N =", Hn)
    #print ("      Bins =", Hbins)
    #print ("   Patches =", Hpatches)
    mplt.xticks(range(-nStep, nStep + 1))
    #mplt.xticks(range(-DistMax, DistMax + 1))
    mplt.xlabel("Mean distance = " + str(round(DistAvg,3)))
    #ax[0,0].text(nStep, MaxV, str(nStep) + ' steps', ha="right", style='italic')
    #ax[0,0].text(nStep, MaxV * 0.9, str(NZC) + ' locns', ha='right', style='italic')
    ax[0].set_xlabel("Mean distance = " + str(round(DistAvg,3)))
    
  if Dim == 2:                # histogram of 2 dim walk
    ax[0].set_title('2 Dimensions: ' + str(nWalk) + ' walks')
    ax[0].set_aspect("equal")
    ax[0].patch.set_facecolor('lightgrey')
    bins = np.arange(startBin, endBin, 1)
    my_cmap = mplt.cm.plasma_r      #.GnBu      #.plasma_r   #.jet
    hist2, xbins2, ybins2, im2 = ax[0].hist2d(xList, yList, bins, cmin=1, cmap=my_cmap) 
    #print ("      Bins =", bins)
    #print ("      Hist =", hist2)
    print ("        im =", im2)
    ax[0].text(nStep, nStep, str(nStep) + ' steps', ha="right", style='italic')      
    #ax[0,1].text(nStep, nStep * 0.9, str(NZC) + ' locns', ha="right", style='italic')
    ax[0].set_xlabel("Mean distance = " + str(round(DistAvg,3)))

  if Dim == 3:                # histogram of 3 dim walk
    xyzList, histList = RWmods.HistXYZ(xList, yList, zList, onlyPos=True)       # my histogrm function
    print("3D list lengths:", str(len(xyzList)) , "/", str(len(histList)))
    if len(xyzList) < 20:
      print(xyzList) 
      print(histList)
    xHist, yHist, zHist, sList = [], [], [], []
    for XYZtup in xyzList:
      #print("XYZ =", XYZtup)
      xHist.append(XYZtup[0])  
      yHist.append(XYZtup[1])
      zHist.append(XYZtup[2])
    for histVal in histList:
      hSize = 10 + histVal * 5
      sList.append(hSize)
    #print("X hist:", xHist); print("Y hist:", yHist); print("Z hist:", zHist); print("S list:", sList)
    ax[0].scatter(xHist, yHist, zHist, s=sList, c="blue", marker="o")
    #ax[0].text(0.05, 0.95, str(len(histList)) + " positions")  #, transform=ax.transAxes)
    #ax[0].set_title(str(len(histList)) + " positions")

  print("_"*12)
  print("      dLen =", str(len(dList)))
  #print(dList) 
  bins = "auto" 
  Hn, Hbins, Hpatches = ax[1].hist(dList, bins, align='mid', rwidth=0.25, log=logYscale, color='g')
  #print ("     dBins =", Hbins)
  #print ("        dN =", Hn)
  #print("Max =", max(Hbins)) 
  DistCt = np.count_nonzero(Hn)
  LabelPos = 3.0; LabelAdj = 1.5
  #ax[1].text(nStep**0.5 * 2.0, max(Hn) * 0.9, str(DistCt) + ' distances', ha='left', style='italic')
  ax[1].text(max(Hbins), max(Hn) * 0.9, str(DistCt) + ' distances', ha='right', style='italic') 
  ax[1].set_xlabel("Mean distance = " + str(round(DistAvg,3)))
  ax[1].grid(axis='y')
    
def is_numbr(val):
    try:
      int(val)
    except ValueError:
      return False
    else:
      #print("          val =", val, int(val*val))
      return True        
  
mainstream()

