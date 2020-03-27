'''
Created on 21 Dec 2019

@author: wvx67826
'''
from Tools import Tools
import matplotlib.pyplot as plt
import numpy as np
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

scanNo = 6388
countTime = 900

marcroFilename = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\2019 12 20\\CCD Scan %i\\C_%i-AI.txt" %(scanNo,scanNo)
folderName = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\2019 12 20\\"

Rd.read_file(marcroFilename, meta = True, metaStopKey = str(scanNo) )
macroData = Rd.get_data()

#print np.full((1,50),macroData["BL 8 Energy"][0])
plt.figure(1)
for i in range(1,2):#+78+7:
    
    if i<10:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-0000%i-1D.txt" %(scanNo,scanNo,i)
    elif i<100:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-000%i-1D.txt" %(scanNo,scanNo,i)
    else:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-00%i-1D.txt" %(scanNo,scanNo,i)

    data = read1DCCD(filename, masterStopKey= "ROI: 1309 526 2539 1627")    
    if i ==1:
        lCounts = np.zeros(data["Counts"].size)
    lPiexel = np.hstack((lPiexel,data["X"])) 
    print macroData["Counts"][i-1]
    lCounts = np.vstack((lCounts,data["Counts"]/countTime))
    tempEnergy = np.full((1,len(data["Counts"])),macroData["Beam Current"][i-1])
    lEnergy = np.hstack((lEnergy,tempEnergy[0])) 
    plt.plot(data["X"], data["Counts"]/countTime)
    plt.show()
blackgoundSum =  np.average(lCounts[1:],axis = 0)
plt.plot(data["X"], blackgoundSum)
blackgoundSum = np.vstack((data["X"],blackgoundSum))
"""for i in lCounts:
    background = 
"""
"""plt.tricontourf(lPiexel,lEnergy, lCounts , 30,interp = 'linear', cmap=plt.get_cmap('jet'))#locator=ticker.LogLocator(),
plt.colorbar()"""
names = ["pixel", "Counts (Total Flux normalized)"]
Rd.write_ascii("C:\\All my tools\\java-mars\\pyworkspace\\Experiments\\Experiment\\ALSBeam8\\data\\backgound_Flux_ZnFe20x.dat", names, blackgoundSum)
