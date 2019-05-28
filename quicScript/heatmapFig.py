# coding = utf-8
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import random
import matplotlib as mpl
from matplotlib import cm
#import importlib
#importlib.import_module('mpl_toolkits.mplot3d').Axes3D
from mpl_toolkits.mplot3d import Axes3D

File = "small"

OutFigName = "avgPLT.pdf"
OutMetricFigName = "metrics.pdf"
OutMetricRatioFigName = "metricsRatio.pdf"
OutRatioFigName = "ratio.pdf"
figLength = 18
if File == "small":
    xloss = [0.001,0.05,0.1,0.5,1,2]
    figLength = 20
else:
    xloss = [0,0.001,0.05,0.1,0.5,1,2]
    figLength = 25

ydelay = [0,50,100,200]#20,

    
def heatmap(figPath,ztime1,ztime2,ztime3,ztime11,ztime22,ztime33,str1,str2,maxt,maxt2,maxt3,mint,mint2,mint3,methods):
    shink = 0.85
    size = 25
    labelsize = 20
    color = "Blues"
    normColor = "RdBu"

    global figLength
    global xloss
    global ydelay

    fig = plt.figure(figsize=(figLength,8))
    ax = fig.add_subplot(231)
    im = ax.imshow(ztime1, interpolation='nearest', vmin=mint-1000, vmax=maxt+100, cmap=plt.get_cmap(color))
    plt.colorbar(im,shrink=shink)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(xloss)))
    ax.set_yticks(np.arange(len(ydelay)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(xloss,fontsize=labelsize-5)
    ax.set_yticklabels(ydelay,fontsize=labelsize-5)
    ax.set_xlabel("Loss(%)",fontsize=labelsize)
    ax.set_ylabel(str1+"Delay(ms)",fontsize=labelsize)

    # Rotate the tick labels and set their alignment.
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(xloss)):
        for j in range(len(ydelay)):
            text = ax.text(i, j, ztime1[j, i],
                           ha="center", va="center", color="w")
    ax.set_title(methods[0],fontsize=size)


    ax = fig.add_subplot(232)
    im = ax.imshow(ztime2, interpolation='nearest', vmin=mint-1000, vmax=maxt+100, cmap=plt.get_cmap(color))
    plt.colorbar(im,shrink=shink)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(xloss)))
    ax.set_yticks(np.arange(len(ydelay)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(xloss,fontsize=labelsize-5)
    ax.set_yticklabels(ydelay,fontsize=labelsize-5)
    ax.set_xlabel("Loss(%)",fontsize=labelsize)
    ax.set_ylabel("Delay(ms)",fontsize=labelsize)

    # Rotate the tick labels and set their alignment.
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(xloss)):
        for j in range(len(ydelay)):
            text = ax.text(i, j, ztime2[j, i],
                           ha="center", va="center", color="w")
    ax.set_title(methods[1],fontsize=size)


    ax = fig.add_subplot(233)
    im = ax.imshow(ztime3, interpolation='nearest', vmin=mint3-0.1, vmax=maxt3+0.1, cmap=plt.get_cmap(normColor))
    plt.colorbar(im,shrink=shink)
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(xloss)))
    ax.set_yticks(np.arange(len(ydelay)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(xloss,fontsize=labelsize-5)
    ax.set_yticklabels(ydelay,fontsize=labelsize-5)
    ax.set_xlabel("Loss(%)",fontsize=labelsize)
    ax.set_ylabel("Delay(ms)",fontsize=labelsize)
    # Rotate the tick labels and set their alignment.
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(xloss)):
        for j in range(len(ydelay)):
            text = ax.text(i, j, ztime3[j, i],
                           ha="center", va="center", color="w")
    ax.set_title(methods[2],fontsize=size)


    ax = fig.add_subplot(234)
    im = ax.imshow(ztime11, interpolation='nearest', vmin=mint2-1000, vmax=maxt2+100, cmap=plt.get_cmap(color))
    plt.colorbar(im,shrink=shink)
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(xloss)))
    ax.set_yticks(np.arange(len(ydelay)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(xloss,fontsize=labelsize-5)
    ax.set_yticklabels(ydelay,fontsize=labelsize-5)
    ax.set_xlabel("Loss(%)",fontsize=labelsize)
    ax.set_ylabel(str2+"Delay(ms)",fontsize=labelsize)
    # Rotate the tick labels and set their alignment.
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(xloss)):
        for j in range(len(ydelay)):
            text = ax.text(i, j, ztime11[j, i],
                           ha="center", va="center", color="w")


    ax = fig.add_subplot(235)
    im = ax.imshow(ztime22, interpolation='nearest', vmin=mint2-1000, vmax=maxt2+100, cmap=plt.get_cmap(color))
    plt.colorbar(im,shrink=shink)
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(xloss)))
    ax.set_yticks(np.arange(len(ydelay)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(xloss,fontsize=labelsize-5)
    ax.set_yticklabels(ydelay,fontsize=labelsize-5)
    ax.set_xlabel("Loss(%)",fontsize=labelsize)
    ax.set_ylabel("Delay(ms)",fontsize=labelsize)
    # Rotate the tick labels and set their alignment.
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(xloss)):
        for j in range(len(ydelay)):
            text = ax.text(i, j, ztime22[j, i],
                           ha="center", va="center", color="w")


    ax = fig.add_subplot(236)
    im = ax.imshow(ztime33, interpolation='nearest', vmin=mint3-0.1, vmax=maxt3+0.1, cmap=plt.get_cmap(normColor))
    plt.colorbar(im,shrink=shink)
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(xloss)))
    ax.set_yticks(np.arange(len(ydelay)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(xloss,fontsize=labelsize-5)
    ax.set_yticklabels(ydelay,fontsize=labelsize-5)
    ax.set_xlabel("Loss(%)",fontsize=labelsize)
    ax.set_ylabel("Delay(ms)",fontsize=labelsize)
    # Rotate the tick labels and set their alignment.
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(xloss)):
        for j in range(len(ydelay)):
            text = ax.text(i, j, ztime33[j, i],
                           ha="center", va="center", color="w")
    #plt.text(-10, -4.9, "First connection", fontsize=size, ha='left', rotation=90)
    #plt.text(-10, .9, "Subsequent connection", fontsize=size, ha='left', rotation=90)
    fig.tight_layout()
    #plt.show()
    plt.savefig(figPath)
    plt.close()


    
def heatmapratio(figPath,ztime3,ztime33,str1,str2,maxt1,maxt2,methods):
    shink = 0.9
    size = 25
    labelsize = 20
    color = "Blues"
    normColor = "RdBu"

    global figLength
    global xloss
    global ydelay

    fig = plt.figure(figsize=(figLength-5,4.5))

    ax = fig.add_subplot(121)
    im = ax.imshow(ztime3, interpolation='nearest', vmin=-maxt1-0.1, vmax=maxt1+0.1, cmap=plt.get_cmap(normColor))
    plt.colorbar(im,shrink=shink)
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(xloss)))
    ax.set_yticks(np.arange(len(ydelay)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(xloss,fontsize=labelsize-5)
    ax.set_yticklabels(ydelay,fontsize=labelsize)
    ax.set_xlabel("Loss(%)",fontsize=labelsize)
    ax.set_ylabel("Delay(ms)",fontsize=labelsize)
    # Rotate the tick labels and set their alignment.
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(xloss)):
        for j in range(len(ydelay)):
            text = ax.text(i, j, ztime3[j, i],fontsize=labelsize,
                           ha="center", va="center", color="w")
    ax.set_title(methods[0],fontsize=size)

    ax = fig.add_subplot(122)
    im = ax.imshow(ztime33, interpolation='nearest', vmin=-maxt2-0.1, vmax=maxt2+0.1, cmap=plt.get_cmap(normColor))
    plt.colorbar(im,shrink=shink)
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(xloss)))
    ax.set_yticks(np.arange(len(ydelay)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(xloss,fontsize=labelsize-5)
    ax.set_yticklabels(ydelay,fontsize=labelsize)
    ax.set_xlabel("Loss(%)",fontsize=labelsize)
    ax.set_ylabel("Delay(ms)",fontsize=labelsize)
    # Rotate the tick labels and set their alignment.
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(xloss)):
        for j in range(len(ydelay)):
            text = ax.text(i, j, ztime33[j, i],fontsize=labelsize,
                           ha="center", va="center", color="w")
    ax.set_title(methods[1],fontsize=size)
    #plt.text(-10, -4.9, "First connection", fontsize=size, ha='left', rotation=90)
    #plt.text(-10, .9, "Subsequent connection", fontsize=size, ha='left', rotation=90)
    fig.tight_layout()
    #plt.show()
    plt.savefig(figPath)
    plt.close()

def plotAvgPLT(path, avgPLT, keys):
    figPath = os.path.join(path, OutFigName)
    print figPath

    loss = pd.to_numeric(avgPLT['loss'], errors='coerce')
    delay = pd.to_numeric(avgPLT['delay'], errors='coerce')

    time1 = pd.to_numeric(avgPLT['firstConn_0'], errors='coerce')
    time2 = pd.to_numeric(avgPLT['firstConn_1'], errors='coerce') 
    time11 = pd.to_numeric(avgPLT['subsequentConn_0'], errors='coerce')
    time22 = pd.to_numeric(avgPLT['subsequentConn_1'], errors='coerce') 

    maxt = max(max(time1),max(time2),max(time11),max(time22))
    mint = min(min(time1),min(time2),min(time11),min(time22))


    flag = 1
    if "_nc" in keys[0]:
        methods = ['Without loss classifier', 'With loss classifier', 'PLT ratio']
    else:
        methods = ['With loss classifier', 'Without loss classifier', 'PLT ratio']
        flag = 0

    global xloss
    global ydelay

    ztime1 = np.zeros((len(ydelay),len(xloss)))
    ztime2 = np.zeros((len(ydelay),len(xloss)))
    ztime11 = np.zeros((len(ydelay),len(xloss)))
    ztime22 = np.zeros((len(ydelay),len(xloss)))
    ztime3 = np.zeros((len(ydelay),len(xloss)))
    ztime33 = np.zeros((len(ydelay),len(xloss)))
    


    for i in range(len(xloss)):
        for j in range(len(ydelay)):
            for k in range(len(loss)):
                if loss[k]==xloss[i] and delay[k]==ydelay[j]:
                    ztime1[j,i] = time1[k]
                    ztime2[j,i] = time2[k]
                    ztime11[j,i] = time11[k]
                    ztime22[j,i] = time22[k]
    
    if flag == 1:
        ztime3 = (ztime1-ztime2)/ztime1*100
        ztime33 = (ztime11-ztime22)/ztime11*100
    else:
        ztime3 = (ztime2-ztime1)/ztime2*100
        ztime33 = (ztime22-ztime11)/ztime22*100

    ztime3 = np.around(ztime3,decimals=1)
    ztime33 = np.around(ztime33,decimals=1)
    maxt3 = max(np.amax(ztime3),np.amax(ztime33))
    mint3 = min(np.amin(ztime3),np.amin(ztime33))


    tmp = max(abs(maxt3),abs(mint3))
    grids = [ztime1,ztime2,ztime11,ztime22,ztime3,ztime33]
    print grids
    print "\nPLT gain:",np.mean(ztime33)

    str1="First connection\n"
    str2="Subsequent connection\n"
    heatmap(figPath,ztime1,ztime2,ztime3,ztime11,ztime22,ztime33,str1,str2,maxt,maxt,tmp,mint,mint,-tmp,methods)
    
    methods = ['PLT ratio(%) of connection', 'PLT ratio(%) of classifier']
    #methods = ['', '']of firstConn-subConn to firstConn

    str1=""
    str2=""
    figPath = os.path.join(path, OutRatioFigName)
    print figPath
    ztime111 = np.around((ztime1-ztime11)/ztime1*100,decimals=1)
    tmp1 = max(abs(np.amax(ztime111)),abs(np.amin(ztime111)))
    tmp2 = max(abs(np.amax(ztime33)),abs(np.amin(ztime33)))

    heatmapratio(figPath,ztime111,ztime33,str1,str2,tmp1,tmp2,methods)

def dataProcess(dirs):
    bw = []
    bwNC = []
    normBwNC = []

    loss = []
    lossNC = []
    normLossNC = []

    columns = ["avgBW","lossAllNum"]
    global xloss
    global ydelay

    subDirAndFile = os.walk(dirs)
    for path,dirList,fileList in subDirAndFile:  
        for fileName in fileList:  
            subFilePath = os.path.join(path, fileName)
            if "Metrics" not in fileName or ".DS_Store" in fileName:
                continue

            df = pd.read_csv(subFilePath, usecols=columns, low_memory=False)
            avgBW=pd.to_numeric(df['avgBW'],errors='coerce').tolist()
            lossAllNum=pd.to_numeric(df['lossAllNum'],errors='coerce').tolist()
            #print type(avgBW)

            size = len(xloss) * len(ydelay)
            segsize = len(avgBW)/size

            if "_nc" in fileName:
                for i in range(size):
                    #print avgBW[segsize*i:segsize*(i+1)]
                    bwNC.append(round(np.mean(avgBW[segsize*i:segsize*(i+1)]),2))
                    lossNC.append(round(np.mean(lossAllNum[segsize*i:segsize*(i+1)]),2))
            else:
                for i in range(size):
                    bw.append(round(np.mean(avgBW[segsize*i:segsize*(i+1)]),2))
                    loss.append(round(np.mean(lossAllNum[segsize*i:segsize*(i+1)]),2))

    bw = np.array(bw).reshape(len(xloss),len(ydelay)).T
    bwNC = np.array(bwNC).reshape(len(xloss),len(ydelay)).T
    loss = np.array(loss).reshape(len(xloss),len(ydelay)).T
    lossNC = np.array(lossNC).reshape(len(xloss),len(ydelay)).T
    normBwNC = np.around((bw-bwNC)/bwNC*100,decimals=1)
    normLossNC = np.around((lossNC-loss)/lossNC*100,decimals=1)

    return bw,bwNC,normBwNC,loss,lossNC,normLossNC

def plotMetrics(path):
    figPath = os.path.join(path, OutMetricFigName)
    print figPath

    ztime1,ztime2,ztime3,ztime11,ztime22,ztime33 = dataProcess(path)

    maxt = max(np.amax(ztime1),np.amax(ztime2))
    maxt2 = max(np.amax(ztime11),np.amax(ztime22))
    maxt3 = max(np.amax(ztime3),np.amax(ztime33))
    mint = min(np.amin(ztime1),np.amin(ztime2))
    mint2 = min(np.amin(ztime11),np.amin(ztime22))
    mint3 = min(np.amin(ztime3),np.amin(ztime33))
    tmp = max(abs(maxt3),abs(mint3))


    methods = ['With loss classifier', 'Without loss classifier', 'Gain ratio']


    grids = [ztime1,ztime2,ztime11,ztime22,ztime3,ztime33]
    print grids

    str1="Average BW\n"
    str2="Lost packet count\n"
    heatmap(figPath,ztime1,ztime2,ztime3,ztime11,ztime22,ztime33,str1,str2,maxt,maxt2,tmp,mint,mint2,-tmp,methods)
    
    methods = ['Average BW ratio(%)', 'Lost packet count ratio(%)']
    str1=""
    str2=""
    figPath = os.path.join(path, OutMetricRatioFigName)
    print figPath

    tmp1 = max(abs(np.amax(ztime3)),abs(np.amin(ztime3)))
    tmp2 = max(abs(np.amax(ztime33)),abs(np.amin(ztime33)))
    heatmapratio(figPath,ztime3,ztime33,str1,str2,tmp1,tmp2,methods)

    
