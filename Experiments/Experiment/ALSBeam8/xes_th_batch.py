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
A2Q = Tools.AngleToQ()
Reduct = Tools.Output()
Reduct.add_clipboard_to_figures()
def read1DCCD(filename, masterStopKey):
    Rd.read_file(filename, metaStopKey = masterStopKey)
    return Rd.get_data()




lPiexel = np.array([])
lCounts = np.array([])
lEnergy = np.array([])
#6447
scanNo = 6470
date = 22
ENERGY = 522.9
tth = 145.0
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
    
        #plt.figure()
    #cter = cter + 1
    
    if i<10:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-0000%i-1D.txt" %(scanNo,scanNo,i)
    elif i<100:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-000%i-1D.txt" %(scanNo,scanNo,i)
    else:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-00%i-1D.txt" %(scanNo,scanNo,i)
        
    data = read1DCCD(filename, masterStopKey= "ROI: 1309 526 2539 1627")    
    
    if cter == 0:
        sX = metaData["X"][cter]
        sY = metaData["Y"][cter]
        sTh = metaData["Top Seal"][cter]
        count = data["Counts"]/metaData["Counts"][i-1] - backgroundData["Counts (Total Flux normalized)"]
        plt.figure() 
    
    if (abs(sX  - metaData["X"][cter]) + abs(sY - metaData["Y"][cter]))<0.01 and abs(sTh - metaData["Top Seal"][cter]) <30:
        
        tempCount =  data["Counts"]/metaData["Counts"][i-1] - backgroundData["Counts (Total Flux normalized)"] 
        if abs(sTh - metaData["Top Seal"][cter])<0.5:
            count = (tempCount + count)/2.0
            print metaData["Top Seal"][cter]
        else:
            lPiexel = np.hstack((lPiexel, ENERGY - energyCalData["energy"]))
            lCounts = np.hstack((lCounts,count))
            tempEnergy = np.full((1,len(data["Counts"])),A2Q.cal_qx(tth, 90.0-metaData["Top Seal"][i-1], ENERGY))
            lEnergy = np.hstack((lEnergy,tempEnergy[0]))
            sTh = metaData["Top Seal"][cter]
            count = data["Counts"]/metaData["Counts"][i-1] - backgroundData["Counts (Total Flux normalized)"] 
            
            plt.plot(ENERGY-energyCalData["energy"],count, label = sTh)
            plt.xlim(0,7)
            plt.legend()
            plt.show(block = False)
        #plt.subplot(9,9,cter) 
        """        plt.xlim(-1,12)
        plt.title(metaData["BL 8 Energy"][i-1])
        plt.plot(metaData["BL 8 Energy"][i-1]-energyCalData["energy"], tempCount)
        """
    else:
        sX = metaData["X"][cter]
        sY = metaData["Y"][cter]
        lPiexel = np.hstack((lPiexel,ENERGY - energyCalData["energy"]))
        lCounts = np.hstack((lCounts,count))
        tempEnergy = np.full((1,len(data["Counts"])),A2Q.cal_qx(tth, 90.0- metaData["Top Seal"][i-1], ENERGY))
        lEnergy = np.hstack((lEnergy,tempEnergy[0]))
        sTh = metaData["Top Seal"][cter]
        count = data["Counts"]/metaData["Counts"][i-1] - backgroundData["Counts (Total Flux normalized)"] 
        
        plt.figure()
        print len(lPiexel), len(lEnergy), lCounts.size, cter
        plt.ylim(-1,12)
        plt.tricontourf(lEnergy,lPiexel, lCounts , 30,interp = 'linear', cmap=plt.get_cmap('jet'))#locator=ticker.LogLocator(),
        plt.colorbar()
        plt.show(block = False)        
        lPiexel = np.array([])
        lCounts = np.array([])
        lEnergy = np.array([])
        plt.figure()
        #lPiexel = np.hstack((lPiexel,ENERGY -energyCalData["energy"]))
        #tempCount =  data["Counts"]/metaData["Counts"][i-1] - backgroundData["Counts (Total Flux normalized)"] 
        #lCounts = np.hstack((lCounts,tempCount))
        #tempEnergy = np.full((1,len(data["Counts"])),metaData["Top Seal"][i-1])
        #lEnergy = np.hstack((lEnergy,tempEnergy[0]))
    
    if i == metaData["Frame #"].astype(int)[-1]:
        sX = metaData["X"][cter]
        sY = metaData["Y"][cter]
        lPiexel = np.hstack((lPiexel,ENERGY - energyCalData["energy"]))
        lCounts = np.hstack((lCounts,count))
        tempEnergy = np.full((1,len(data["Counts"])),A2Q.cal_qx(tth, 90.0-metaData["Top Seal"][i-1], ENERGY))
        lEnergy = np.hstack((lEnergy,tempEnergy[0]))
        sTh = metaData["Top Seal"][cter]
        count = data["Counts"]/metaData["Counts"][i-1] - backgroundData["Counts (Total Flux normalized)"] 
    
        plt.figure()
        print len(lPiexel), len(lEnergy), lCounts.size
        plt.ylim(-1,12)
        plt.tricontourf(lEnergy,lPiexel, lCounts , 30,interp = 'linear', cmap=plt.get_cmap('jet'))#locator=ticker.LogLocator(),
        plt.colorbar()
        plt.show()        
        
        #plt.subplot(9,9,cter) 
"""        plt.xlim(-1,12)
        plt.title(metaData["BL 8 Energy"][i-1])
        plt.plot(metaData["BL 8 Energy"][i-1]-energyCalData["energy"], tempCount)"""
   
 
