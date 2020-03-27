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
sampleName = np.array([])
#6447
counts = 0
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



for cter, i in enumerate (metaData["BL 8 Energy"]):#+78+7:
    if cter == 0:
        sX = metaData["X"][cter]
        sY = metaData["Y"][cter]
        sampleName = np.append(sampleName,"Energy")
        sampleName = np.append(sampleName, sY)
        pixel = energyCalData["energy"]
        plt.figure()
        firstpass = True
    #cter = cter + 1
    print cter
    if cter<9:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-0000%s-1D.txt" %(scanNo,scanNo,cter+1)
    elif cter<99:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-000%s-1D.txt" %(scanNo,scanNo,cter+1)
    else:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-00%s-1D.txt" %(scanNo,scanNo,cter+1)
    data = read1DCCD(filename, masterStopKey= "ROI: 1309 526 2539 1627")    
    
    if (abs(sX  - metaData["X"][cter]) + abs(sY - metaData["Y"][cter]))<0.01:
        if i>550:
            print i, 
            tempCount =  data["Counts"]/metaData["Counts"][cter-1] - backgroundData["Counts (Total Flux normalized)"] 
            counts = (counts + tempCount)/2.0

    else:
        sX = metaData["X"][cter]
        sY = metaData["Y"][cter]
        if firstpass:
            lCounts = counts
            firstpass = False
        else:
            lCounts = np.vstack((lCounts, counts))
        sampleName = np.append(sampleName,sY)
        plt.plot(pixel, counts)

    if cter == metaData["BL 8 Energy"].size -1:
        print pixel.size, lCounts.size
        lCounts = np.vstack((lCounts, counts))
        outputData = np.vstack((pixel, lCounts))
        plt.plot(pixel, counts)
        Rd.write_ascii("data\\%ieV_%i_XES.dat" %(i,scanNo), sampleName, outputData)

plt.show()
 
