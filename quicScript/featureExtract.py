# coding = utf-8

import os
import math
import pandas as pd
import matplotlib.pyplot as plt

quicDir = "/Users/yuyajun/Downloads/quic_loss_project/quicLossExp/quicLog/0308/"
dicts = {}
featureDataDict = {}
MAXDIST = 100

def featureExtract(dir, name, suffix):
    path = os.path.join(dir, name + suffix)
    print path
    time = 0
    numAckEvent = 0
    LostDist = 0 
    lastLostDist = 0
    with open(path, 'r') as f:
        line = f.readline()
        while line:
            featureDict = toDict(line)
            if "Time" in featureDict.keys() and len(featureDict.keys())==1:
                numLossEvent = 0
                numAckEvent = 0
                time = featureDict["Time"]

            if len(featureDict) > 8:
                numAckEvent = numAckEvent+1
                #print "numAckEvent:", numAckEvent
                featureDict["numAckEvent"] = numAckEvent
                featureDict["Time"] = time
                if "LostPacketCount" not in featureDict.keys():
                    featureDict["LostPacketCount"] = 0
                    featureDict["LostCount"] = 0
                    LostCount = 0 

                    featureDict["LostDist"] = -1
                    LostDist = LostDist + 1
                else:
                    if LostCount == 0:
                        lastLostDist = LostDist
                    featureDict["LostDist"] = min(lastLostDist, MAXDIST)
                    LostDist = 0
                      
                    LostCount = LostCount + 1
                    featureDict["LostCount"] = LostCount

                    
             
                for k,v in featureDict.items():
                    if k not in featureDataDict.keys():
                        featureDataDict[k] = []   
                    featureDataDict[k].append(v)
            line = f.readline()

        dataframe = pd.DataFrame(featureDataDict)
        outPath = dir+name+"Clear.csv"
        dataframe.to_csv(outPath, index=True, sep=',')#, mode='a')

def toDict(text):
    t = text.split('] ')[1]
    contents = t.split('\n')[0]
    #print contents
    if ';' in contents:
        contents = contents.split(';')
        for content in contents:
            c = content.split(':')
            key = c[0]
            value = c[1]
            dicts[key] = value
            featureDict = dicts.copy()
        dicts.clear()
    else:
        c = contents.split(':')
        key = c[0]
        value = c[1]
        dicts[key] = value
        featureDict = dicts.copy()
    return featureDict

def plotFig(oneHeader, filePath, outFigPath):
    y = pd.read_csv(filePath, usecols=[oneHeader])
    x = [i for i in range(len(y))]
    plt.figure()
    plt.plot(x,y)
    plt.savefig(outFigPath+oneHeader+".jpg")


if __name__ == "__main__":
    fname = "lossFeature0308"
    #featureExtract(quicDir, fname, ".log")
    filePath = quicDir+fname+"Clear.csv"
    outFigPath = quicDir
    header = "CongWin" #"BW"
    plotFig(header, filePath, outFigPath)
