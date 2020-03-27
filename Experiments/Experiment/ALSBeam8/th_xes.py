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

marcroFilename = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\thscan2.txt"
folderName = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\2019 12 21\\"
scanNo = 6444
Rd.read_file(marcroFilename, meta = False)
macroData = Rd.get_data()
#print np.full((1,50),macroData["BL 8 Energy"][0])
plt.figure(1)
for i in range(1,11):#+78+7:
    
    if i<10:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-0000%i-1D.txt" %(scanNo,scanNo,i)
    elif i<100:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-000%i-1D.txt" %(scanNo,scanNo,i)
    else:
        filename =folderName +"CCD Scan %i\\Andor 20039\\C_%i-00%i-1D.txt" %(scanNo,scanNo,i)
    data = read1DCCD(filename, masterStopKey= "ROI: 1309 526 2539 1627")    
    lPiexel = np.hstack((lPiexel,data["X"])) 
    lCounts = np.hstack((lCounts,data["Counts"]) )
    tempEnergy = np.full((1,len(data["Counts"])),macroData["Top Seal"][i-1])
    lEnergy = np.hstack((lEnergy,tempEnergy[0])) 
    plt.plot(data["X"], data["Counts"])
plt.figure(2)
plt.tricontourf(lPiexel,lEnergy, lCounts , 30,interp = 'linear', cmap=plt.get_cmap('jet'), vmax = 110000)#locator=ticker.LogLocator(),
plt.colorbar()
plt.show()