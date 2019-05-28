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

from heatmapFig import plotAvgPLT
from boxFig import boxPlot
#PLTDIR = "/Users/yuyajun/Downloads/quic_loss_project/quicLossExp/quicPLT"
PLTDIR =  "/Users/yuyajun/Downloads/quic_loss_project/quicLossExp/quicPLT/before/0402(1)small"

OutFileName = "avgPLT.csv"


def fileProcess(path,file):
    f = open(path);
    firstConn = []
    subsequentConn = []
    avgPLT = []
    index = 0
    for line in f.readlines():
        line = line.strip() #remove the space at the beginning and end of line
        if index == 0:#the first line of my file is date
            index = 1
            continue
        if not len(line) or line.startswith("#") or ".txt" not in file:#skip the null line and comment line
            continue
        aPLT = line.split()
        aPLT = list(map(int, aPLT)) 
        firstConn.append(aPLT[0])
        subsequentConn.extend(aPLT[1:])
    if len(firstConn)>0 and len(subsequentConn)>0:
        avgPLT.append(round(np.mean(firstConn),2))
        avgPLT.append(round(np.mean(subsequentConn),2))
    else:
        avgPLT.extend([-1,-1])
    return firstConn,subsequentConn,avgPLT

def writeToFile(path,filename,data):
    filePath = os.path.join(path, filename)
    #print "filePath:", filePath
    df = pd.DataFrame(data)
    df.to_csv(filePath, index=False)


# traverse all files under current dir path
def traverseFile(path):    
    avgPLT={}
    firstConn = {}
    subsequentConn = {}
    files= os.listdir(path) 
    for file in files: 
        filePath = os.path.join(path, file)
        if not os.path.isdir(filePath):#skip subdir
            #print filePath
            if ".txt" in file:#skip the result file
                firstConn[file],subsequentConn[file],avgPLT[file] = fileProcess(filePath,file)
    #print avgPLT
    file = path.split("/")[-1]
    filename = file+"_avgPLT.csv"
    writeToFile(path,filename,avgPLT)
    filename = file+"_firstConn.csv"
    writeToFile(path,filename,firstConn)
    filename = file+"_subsequentConn.csv"
    writeToFile(path,filename,subsequentConn)

    return firstConn,subsequentConn,avgPLT

def combineAllDirPLT(PLTdict,FirstConnDict,SubConnDict):
    #print PLTdict
    combAvgPLT = {"fileName":[],"fileSize":[],"loss":[],"delay":[],"firstConn":[],"subsequentConn":[]} 
    fileName = []
    keys = []
    for key, value in PLTdict.iteritems():
        if len(value) != 0:
            fileName.extend(value.keys())
            keys.append(key)
    fileName = list(set(fileName))

    for file in fileName:
        if ".txt" not in file:
            continue
        firstConn = []
        subsequentConn = []
        for key, value in PLTdict.iteritems():
            if len(value) == 0:
                continue
            if file in value.keys():
                firstConn.append(value[file][0])
                subsequentConn.append(value[file][1])
            else:
                firstConn.append(-1)
                subsequentConn.append(-1)
        combAvgPLT["fileName"].append(file)
        fnsplit = file.split(".txt")[0].split("_")
        combAvgPLT["fileSize"].append(fnsplit[0])
        combAvgPLT["loss"].append(fnsplit[1])
        combAvgPLT["delay"].append(fnsplit[2])
        combAvgPLT["firstConn"].append(firstConn)
        combAvgPLT["subsequentConn"].append(subsequentConn)

        for i in range(len(keys)):
            if "firstConn_%d" %i not in combAvgPLT.keys():
                combAvgPLT["firstConn_%d" %i] = []
            if "subsequentConn_%d" %i not in combAvgPLT.keys():
                combAvgPLT["subsequentConn_%d" %i] = []
            combAvgPLT["firstConn_%d" %i].append(firstConn[i])
            combAvgPLT["subsequentConn_%d" %i].append(subsequentConn[i])

        firstConnAll = []
        subsequentConnAll = []
        for key,value in FirstConnDict.iteritems():
            if len(value) == 0:
                continue
            if file in value.keys():
                firstConnAll.append(value[file])
            else:
                firstConnAll.append([-1])
        for key,value in SubConnDict.iteritems():
            if len(value) == 0:
                continue
            if file in value.keys():
                subsequentConnAll.append(value[file])
            else:
                subsequentConnAll.append([-1])

        for i in range(len(keys)):
            if "firstConnAll_%d" %i not in combAvgPLT.keys():
                combAvgPLT["firstConnAll_%d" %i] = []
            if "subsequentConnAll_%d" %i not in combAvgPLT.keys():
                combAvgPLT["subsequentConnAll_%d" %i] = []
            combAvgPLT["firstConnAll_%d" %i].append(firstConnAll[i])
            combAvgPLT["subsequentConnAll_%d" %i].append(subsequentConnAll[i])

    return keys,fileName,combAvgPLT


# get the subdir of current dir and traverse the files under subdir
def getSubDirAndFile(currentDir):
    eachAvgPLT={}
    eachFirstConn={}
    eachSubsequentConn={}
    subDirAndFile = os.walk(currentDir)    
    for path,dirList,fileList in subDirAndFile:  
        '''for fileName in fileList:  
            print(os.path.join(path, fileName))'''
        #print dirList
        for dirName in dirList:
            subDirPath = os.path.join(path, dirName)
            #print subDirPath
            eachFirstConn[dirName],eachSubsequentConn[dirName],eachAvgPLT[dirName] = traverseFile(subDirPath)
        break #skip the subdir

    keys, allFile, combAvgPLT = combineAllDirPLT(eachAvgPLT,eachFirstConn,eachSubsequentConn)
    print "the list of dir:", keys
    file = currentDir.split("/")[-1]
    filename = file+"_avgPLT.csv"
    writeToFile(currentDir,filename,combAvgPLT)

    boxPlot(keys,currentDir,filename,combAvgPLT)

    return keys,currentDir,combAvgPLT



def lossDelayPLT3D():
    data = np.random.randint(0, 255, size=[40, 40, 40])

    x, y, z = data[0], data[1], data[2]
    ax = plt.subplot(111, projection='3d') 
    ax.scatter(x[:10], y[:10], z[:10], c='y')  
    ax.scatter(x[10:20], y[10:20], z[10:20], c='r')
    ax.scatter(x[30:40], y[30:40], z[30:40], c='g')

    ax.set_zlabel('Z')  
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()

if __name__ == '__main__':
    keys,currentDir,combAvgPLT = getSubDirAndFile(PLTDIR)
    plotAvgPLT(currentDir,combAvgPLT,keys)
    #lossDelayPLT3D()

'''
#ax.bar(x, y, z1, zdir='y', color='y', alpha=0.8)
    #ax.plot_wireframe(x, y, z1, rstride=10, cstride=10)
    #ax.plot_wireframe(x, y, z2, rstride=10, cstride=10)
    ax.scatter(loss, delay, time1, c='y')  
    ax.scatter(loss, delay, time2, c='b')  
    ax.set_zlabel('PLT of first connection(ms)')  
    ax.set_ylabel('Delay(ms)')
    ax.set_xlabel('Loss(%)')
    #plt.show()

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x = [0.001,0.05,0.1,0.5,1,2]
    y = [0,20,50,100,200]
    xx, yy = np.meshgrid(x,y)
    z1 = np.zeros((len(x),len(y)))
    z2 = np.zeros((len(x),len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            for k in range(len(loss)):
                if loss[k]==x[i] and delay[k]==y[j]:
                    z1[i,j] = time1[k]
                    z2[i,j] = time2[k]
    #surf = ax.plot_surface(xx, yy, z1.T, cmap=cm.coolwarm, linewidth=1, antialiased=True)
    #surf = ax.plot_surface(xx, yy, z2.T, cmap=cm.coolwarm, linewidth=1, antialiased=True)

    top = z1.T.ravel()
    bottom = np.zeros_like(top)

    width = 1
    depth = 1
    ax.bar3d(xx.ravel(), yy.ravel(), bottom, width, depth, top)
    plt.show()

    mpl.rcParams['font.size'] = 10
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for z in y:
        xs = x
        ys1 = []
        ys2 = []
        for xx in xs:
            for k in range(len(loss)):
                if loss[k]==xx and delay[k]==z:
                    ys1.append(time1[k])
                    ys2.append(time2[k])


        color = plt.cm.Set2(random.choice(range(plt.cm.Set2.N)))
        ax.bar(xs, ys1, zs=z, zdir='y', width = 0.03, facecolor = 'lightskyblue', edgecolor = 'white', alpha=0.9)
        ax.bar(xs, ys2, zs=z, zdir='y', width = 0.03, facecolor = 'yellowgreen', edgecolor = 'white', alpha=0.9)
     
    ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(xs))
    ax.yaxis.set_major_locator(mpl.ticker.FixedLocator(y))
    ax.set_xlabel('Loss(%)')
    ax.set_ylabel('Delay(ms)')
    ax.set_zlabel('PLT of first connection(ms)')
    plt.show()


    # setup the figure and axes
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')

    # fake data
    _x = np.arange(4)
    _y = np.arange(5)
    _xx, _yy = np.meshgrid(_x, _y)
    x, y = _xx.ravel(), _yy.ravel()
    print _x,_y,_xx,_yy

    top = x + y
    bottom = np.zeros_like(top)

    width = 1
    depth = 1

    print x,y,bottom,top
    ax1.bar3d(x, y, bottom, width, depth, top)
    ax1.set_title('Shaded')

    plt.show()
'''