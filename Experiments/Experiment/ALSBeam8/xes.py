'''
Created on 21 Dec 2019

@author: wvx67826
'''
from Tools import Tools
import matplotlib.pyplot as plt
import numpy as np
import os, time
from matplotlib import ticker

Rd = Tools.ReadWriteData()
Reduct = Tools.Output()
Reduct.add_clipboard_to_figures()
def read1DCCD(filename, masterStopKey):
    Rd.read_file(filename, metaStopKey = masterStopKey)
    return Rd.get_data()




lPiexel = np.array([])
lCounts = np.array([])
lEnergy = np.array([])
#6447
scanNo = 6429
date = 21

#marcroFilename = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\MapNight2.txt"
energyCalFilename = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\energycalibration_Ru.dat"
backgroundFilename = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\backgound_Flux.dat"
folderName = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\2019 12 %s\\" %date
metaFilename = folderName +"CCD Scan %i\\C_%i-AI.txt" %(scanNo,scanNo)
Rd.read_file(metaFilename, metaStopKey = str(scanNo))
metaData = Rd.get_data()

"""Rd.read_file(marcroFilename, meta = False)
macroData = Rd.get_data()
"""
Rd.read_file(energyCalFilename, meta = False)
energyCalData = Rd.get_data()
Rd.read_file(backgroundFilename, meta = False)
backgroundData = Rd.get_data()



for cter, i in enumerate (metaData["Frame #"].astype(int)):#+78+7:
    if cter == 0:
        sX = metaData["X"][cter]
        sY = metaData["Y"][cter]
        plt.figure()
    #cter = cter + 1
    
    if i<10:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-0000%i-1D.txt" %(scanNo,scanNo,i)
    elif i<100:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-000%i-1D.txt" %(scanNo,scanNo,i)
    else:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-00%i-1D.txt" %(scanNo,scanNo,i)
    data = read1DCCD(filename, masterStopKey= "ROI: 1309 526 2539 1627")    
    if (abs(sX  - metaData["X"][cter]) + abs(sY - metaData["Y"][cter]))<0.01:
        lPiexel = np.hstack((lPiexel,metaData["BL 8 Energy"][i-1]-energyCalData["energy"]))
        tempCount =  data["Counts"]/metaData["Counts"][i-1] - backgroundData["Counts (Total Flux normalized)"] 
        lCounts = np.hstack((lCounts,tempCount))
        tempEnergy = np.full((1,len(data["Counts"])),metaData["BL 8 Energy"][i-1])
        lEnergy = np.hstack((lEnergy,tempEnergy[0]))
        #plt.subplot(9,9,cter) 
        plt.xlim(-1,12)
        plt.title(metaData["BL 8 Energy"][i-1])
        plt.plot(metaData["BL 8 Energy"][i-1]-energyCalData["energy"], tempCount)
    else:
        sX = metaData["X"][cter]
        sY = metaData["Y"][cter]
        plt.figure()
        print len(lPiexel), len(lEnergy), lCounts.size
        plt.xlim(-1,12)
        plt.ylim(520,536)
        plt.tricontourf(lPiexel,lEnergy, lCounts , 30,interp = 'linear', cmap=plt.get_cmap('jet'))#locator=ticker.LogLocator(),
        plt.colorbar()
        plt.show(block = False)        
        lPiexel = np.array([])
        lCounts = np.array([])
        lEnergy = np.array([])
        plt.figure()
        lPiexel = np.hstack((lPiexel,metaData["BL 8 Energy"][i-1]-energyCalData["energy"]))
        tempCount =  data["Counts"]/metaData["Counts"][i-1] - backgroundData["Counts (Total Flux normalized)"] 
        lCounts = np.hstack((lCounts,tempCount))
        tempEnergy = np.full((1,len(data["Counts"])),metaData["BL 8 Energy"][i-1])
        lEnergy = np.hstack((lEnergy,tempEnergy[0]))
        #plt.subplot(9,9,cter) 
        plt.xlim(-1,12)
        plt.title(metaData["BL 8 Energy"][i-1])
        plt.plot(metaData["BL 8 Energy"][i-1]-energyCalData["energy"], tempCount)

    #print sX, i
plt.figure()
plt.xlim(-1,12)
plt.ylim(520,536)
plt.tricontourf(lPiexel,lEnergy, lCounts , 30,interp = 'linear', cmap=plt.get_cmap('jet'))#locator=ticker.LogLocator(),
plt.colorbar()
plt.show()    
 
