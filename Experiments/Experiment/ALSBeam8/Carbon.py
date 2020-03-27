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
lPicked = np.array([])
scanNo = 6386
date = 20
picked = 0

#marcroFilename = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\MapNight2.txt"
energyCalFilename = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\energycalibration_Ru.dat"
backgroundFilename = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\backgound_Flux.dat"
folderName = "C:\\Users\\wvx67826\\Desktop\\beam8 data\\2019 12 %s\\" %date
metaFilename = folderName +"CCD Scan %i\\C_%i-AI.txt" %(scanNo,scanNo)
Rd.read_file(metaFilename, metaStopKey = str(scanNo))
metaData = Rd.get_data()
from lmfit import models
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
    if points.size>2:
        picked = [xdata[ind][0],ydata[ind][2]]
    else:
        picked = [xdata[ind],ydata[ind]]
    lPicked = np.append(lPicked, points)
    fig.canvas.mpl_disconnect(cid)
    return lPicked
    #lPicked = np.append(lPicked,points)



for i in range(1,len(metaData[0])-1):#+78+7:
    fig = plt.figure()
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
    
    plt.xlim([tempMax-10, tempMax+10]) 
    
    plt.plot(data["X"], data["Counts"], picker=2)
    cid = fig.canvas.mpl_connect('pick_event', onpick)
    plt.show()
    print picked
    params_1 = model_1.make_params(amplitude = picked[1], center = picked[0] )
    params_2 = model_2.make_params(slope = 0, intercept = np.min(data["Counts"]))
    params = params_1.update(params_2)
    params = params_1
    output = model.fit(data["Counts"][tempMax-10:tempMax+10], params, x=data["X"][tempMax-10:tempMax+10])
    fig, gridspec = output.plot(data_kws={'markersize': 1})
    print output.fit_report()   
    plt.plot(data["X"], data["Counts"], picker=2)
    plt.show(block = False)
    peakFittedCentre = output.best_values["peak_center"]

plt.plot(lEnergy, lPicked[0])
    
    