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
scanNo = 6390
date = 20
countTime = 900.0 
#marcroFilename = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\MapNight2.txt"
energyCalFilename = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\energycalibration_Power_first.dat"
backgroundFilename = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\backgound_Flux_ZnFe20x.dat"
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


plt.figure(1)
for cter, i in enumerate (metaData["Frame #"]):#+78+7:
    if cter == 0:
        sX = metaData["Z"][cter]
        sY = metaData["Y"][cter]
        sampleName = np.append(sampleName,"Energy")
        sampleName = np.append(sampleName, sY)
        pixel = energyCalData["energy"]
        
        firstpass = True
    #cter = cter + 1
    #print cter
    if cter<9:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-0000%s-1D.txt" %(scanNo,scanNo,cter+1)
    elif cter<99:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-000%s-1D.txt" %(scanNo,scanNo,cter+1)
    else:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-00%s-1D.txt" %(scanNo,scanNo,cter+1)
    data = read1DCCD(filename, masterStopKey= "ROI: 1309 526 2539 1627")    
    

    sX = metaData["Z"][cter]
    sY = metaData["Y"][cter]
    tempCount =  data["Counts"]/countTime - backgroundData["Counts (Total Flux normalized)"] 
    counts = tempCount
    if cter == 0:
        lCounts = counts
    else:
        lCounts = np.vstack((lCounts, counts))
         
    
    sampleName = np.append(sampleName,sY)
    print pixel.size, counts.size
    plt.plot(pixel, counts)
        

    if cter == metaData["Beam Current"].size -1:
        #lCounts = np.vstack((lCounts, counts))
        outputData = np.vstack((pixel, lCounts))
        #plt.plot(pixel, counts)
        Rd.write_ascii("data\\%ieV_%i_XES.dat" %(i,scanNo), sampleName, outputData)

plt.show()
 
