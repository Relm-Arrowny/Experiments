'''
Created on 21 Dec 2019

@author: wvx67826
'''
from Tools import Tools
import matplotlib.pyplot as plt
import numpy as np
from lmfit import models
from scipy import signal
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
lPicked = np.array([])
lPeakPosition = np.array([])
scanNo = 6407
date = 20
picked = 0

folderName = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\2019 12 %s\\" %date
metaFilename = folderName +"CCD Scan %i\\C_%i-AI.txt" %(scanNo,scanNo)
Rd.read_file(metaFilename, metaStopKey = str(scanNo))
metaData = Rd.get_data()

model_1 = models.GaussianModel(prefix='peak_')
model_2 = models.LinearModel(prefix='background_')
model = model_1 + model_2 


#print np.full((1,50),macroData["BL 8 Energy"][0])

def onpick(event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    points = np.array([xdata[ind]])
    global lPicked
    global picked
    print(points)
    picked = [xdata[ind],ydata[ind]]
    lPicked = np.append(lPicked, points)
    fig.canvas.mpl_disconnect(cid)
    return lPicked
    #lPicked = np.append(lPicked,points)



for i in metaData["Frame #"].astype(int):#+78+7:
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
    lCounts = np.vstack((lCounts,data["Counts"]))
    tempEnergy = np.full((1,len(data["Counts"])),metaData["Beam Current"][i-1])
    lEnergy = np.append(lEnergy,metaData["BL 8 Energy"][i-1])
    tempMax = np.argmax(data["Counts"])
    tempMaxVal = np.max(data["Counts"])
    
    plt.xlim([tempMax-100, tempMax+100]) 
    
    peaks, _ = signal.find_peaks(data["Counts"] ,  height = 41000)
    if peaks.size>1:
        peaks = peaks[0]
    params_1 = model_1.make_params(amplitude = tempMaxVal, center = peaks )
    params_2 = model_2.make_params(slope = 0, intercept = np.min(data["Counts"]))
    params = params_1.update(params_2)
    params = params_1
    output = model.fit(data["Counts"][tempMax-10:tempMax+10], params, x=data["X"][tempMax-10:tempMax+10])
    fig, gridspec = output.plot(data_kws={'markersize': 1})
    print output.fit_report()   
    peakFittedCentre = output.best_values["peak_center"]
    lPeakPosition = np.append(lPeakPosition, peakFittedCentre)
plt.figure()
plt.plot(metaData["BL 8 Energy"], lPeakPosition)
outputData = np.vstack((metaData["BL 8 Energy"], lPeakPosition))

Rd.write_ascii("data\\%ieV_%i_Cal.dat" %(metaData["BL 8 Energy"][0],scanNo), ["Energy", "Pixel"], outputData)

plt.show()
    
    