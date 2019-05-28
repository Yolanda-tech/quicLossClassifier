# coding = utf-8

import os
import math
import pandas as pd
import matplotlib.pyplot as plt
from heatmapFig import plotMetrics

quicDir = "/Users/yuyajun/Downloads/quic_loss_project/quicLossExp/quicLog/0402(1)small/"
#fname = "lossFeature0308"
#hasRF = 0 #does the log have "lossTypeIsCong" ?

#######################
## An ACK event log(hasRF = 1)
##
## (Time: 0000000000)
## PacketAckedCount:1
## (LostPacketCount:2)
## ConstantLostPacketCount:2
## ackReceiveTime:3135630000698;CongWin:89443;BW:4882;smoothRTT:18318;preRTT:19589;latestRTT:9427;minRTT:7754;loss:31;retransmit:29;sent:442;inSS:0;inRcvry:0
## (lossTypeIsCong: 0)
##
#######################
#######################
## An ACK event log(hasRF = 0)
##
## (Time: 0000000000)
## PacketAckedCount:2
## (LostPacketCount:1)
## ConstantLostPacketCount:0
## ackReceiveTime:1563288533655;CongWin:156220;BW:2612;smoothRTT:59793;preRTT:58623;latestRTT:67985;minRTT:56037;loss:0;retransmit:1;sent:336;inSS:0;inRcvry:0
## (LostPacketCount:1)
## (ConstantLostPacketCount:1)
##
#######################


dicts = {}
featureDataDict = {}
featureDataCalculateDict = {}
metricsDict = {"lossAllNum":[], "avgBW":[]}

features = ['BW','CongWin','ConstantLostPacketCount','LostCount','LostPacketCount',
           'inRcvry','inSS']
calFeatures = ['LostDistWeight','Rlmrtt','Rlsrtt','Rsprtt','type']

nonCongNum = 7*5*20 #loss*delay*exptimes
MAXDIST = 100

xxxx = 0
yyyy = 0
zzzz = 0
# one line to dict(key:value)
def toDict(text):
    t = text.split('] ')[1]
    contents = t.split('\n')[0]
    if ';' in contents:
        contents = contents.split(';')
        for content in contents:
            c = content.split(':')
            key = c[0]
            value = c[1]
            dicts[key] = value
    else:
        c = contents.split(':')
        key = c[0]
        value = c[1]
        dicts[key] = value

def isFloatEq(f1,f2):
    return abs(f1 - f2) <= 1e-12

def insertLastAckEvent(ackEventFeatureDict, hasRF, time, numAckEvent, lostDist, lastLostDist, lostCount, connTimes, sumBW):
    featureDict = ackEventFeatureDict.copy()
    sumBW += float(featureDict["BW"])
    numAckEvent = numAckEvent+1
    featureDict["numAckEvent"] = numAckEvent
    featureDict["Time"] = time
    if "LostPacketCount" not in featureDict.keys():

        featureDict["LostPacketCount"] = 0

        featureDict["LostCount"] = 0
        lostCount = 0 #the number of times in consecutive packet losses

        featureDict["LostDist"] = -1
        lostDist = lostDist + 1 #the dist between two lossed
    else:

        if lostCount == 0:
            lastLostDist = lostDist
        featureDict["LostDist"] = min(lastLostDist, MAXDIST)
        lostDist = 0
          
        lostCount = lostCount + 1
        featureDict["LostCount"] = lostCount 

    if hasRF and "lossTypeIsCong" not in featureDict.keys():
        featureDict["lossTypeIsCong"] = -1

    '''if hasRF==0 and len(featureDict) != 19:
        print featureDict,":",len(featureDict)
    elif hasRF==1 and len(featureDict) != 20:
        print featureDict,":",len(featureDict)'''

    for k,v in featureDict.items():
        if k == "lossTypeIsCong" and hasRF == 0:
            continue
        if k not in featureDataDict.keys():
            featureDataDict[k] = []
        
        featureDataDict[k].append(v)



    if int(featureDict["LostPacketCount"]) > 0:
        minRTT = float(featureDict["minRTT"])
        smoothRTT = float(featureDict["smoothRTT"])
        preRTT = float(featureDict["preRTT"])
        latestRTT = float(featureDict["latestRTT"])
        
        if isFloatEq(minRTT,0) != True and isFloatEq(smoothRTT,0) != True and isFloatEq(preRTT,0) != True:
            for k in features:
                if k not in featureDataCalculateDict.keys():
                    featureDataCalculateDict[k] = []   
                featureDataCalculateDict[k].append(featureDict[k])

            for i in range(len(calFeatures)):
                if calFeatures[i] not in featureDataCalculateDict.keys():
                    featureDataCalculateDict[calFeatures[i]] = []

            lostDistWeight = featureDict["LostDist"]/pow(int(featureDict["LostCount"]),4.0/3)/pow(int(featureDict["LostPacketCount"]),0.5)
            Rlmrtt = latestRTT / minRTT
            Rlsrtt = latestRTT / smoothRTT
            Rsprtt = smoothRTT / preRTT
            type = 1 if connTimes>nonCongNum else 0

            featureDataCalculateDict[calFeatures[0]].append(round(lostDistWeight,4))
            featureDataCalculateDict[calFeatures[1]].append(round(Rlmrtt,4))
            featureDataCalculateDict[calFeatures[2]].append(round(Rlsrtt,4))
            featureDataCalculateDict[calFeatures[3]].append(round(Rsprtt,4))
            featureDataCalculateDict[calFeatures[4]].append(type)

    return numAckEvent, lostDist, lastLostDist, lostCount, sumBW


def featureExtract(dir, name, suffix, hasRF):
    path = os.path.join(dir, name + suffix)
    time = 0
    numAckEvent = 0
    lostDist = 0
    lastLostDist = 0
    lostCount = 0
    connTimes = 0
    lossAllNum = []
    avgBW = []
    sumBW = 0.0
    with open(path, 'r') as f:
        line = f.readline()
        while line:
            if " Time:" in line:
                if len(dicts) != 0:
                    numAckEvent, lostDist, lastLostDist, lostCount, sumBW = \
                        insertLastAckEvent(dicts, hasRF, time, numAckEvent, lostDist, lastLostDist, lostCount, connTimes, sumBW)
                    lossAllNum.append(dicts["loss"])
                    avgBW.append(sumBW/numAckEvent)
                sumBW = 0.0
                numAckEvent = 0
                connTimes += 1
                time = line.split('] ')[1].split('\n')[0].split(':')[1]
                dicts.clear()
            if "PacketAckedCount" in line and "PacketAckedCount" in dicts.keys():
                numAckEvent, lostDist, lastLostDist, lostCount, sumBW = \
                    insertLastAckEvent(dicts, hasRF, time, numAckEvent, lostDist, lastLostDist, lostCount, connTimes, sumBW)
                dicts.clear()
            toDict(line)
            line = f.readline()

        #the last one ack event
        numAckEvent, lostDist, lastLostDist, lostCount, sumBW = \
            insertLastAckEvent(dicts, hasRF, time, numAckEvent, lostDist, lastLostDist, lostCount, connTimes, sumBW)
        lossAllNum.append(dicts["loss"])
        avgBW.append(sumBW/numAckEvent)

        #print lossAllNum, avgBW
        metricsDict["lossAllNum"] = lossAllNum
        metricsDict["avgBW"] = avgBW
        dicts.clear()

        dataframe = pd.DataFrame(featureDataDict)
        outPath = os.path.join(dir, name+"Clear.csv")
        dataframe.to_csv(outPath, index=True, sep=',')#, mode='a')

        dataframe = pd.DataFrame(featureDataCalculateDict)
        outPath = os.path.join(dir, name+"ClearCalculate.csv")
        dataframe.to_csv(outPath, index=True, sep=',')#, mode='a')

        dataframe = pd.DataFrame(metricsDict)
        outPath = os.path.join(dir, name+"Metrics.csv")
        dataframe.to_csv(outPath, index=True, sep=',')#, mode='a')

def plotFig(oneHeader, filePath, outFigPath):
    y = pd.read_csv(filePath, usecols=[oneHeader])
    x = [i for i in range(len(y))]
    plt.figure()
    plt.plot(x,y)
    plt.savefig(outFigPath+oneHeader+".jpg")


def extractAllFeature(quicDir):
    subDirAndFile = os.walk(quicDir)
    global dicts
    global featureDataDict
    global featureDataCalculateDict
    for path,dirList,fileList in subDirAndFile:  
        for fileName in fileList:  
            subFilePath = os.path.join(path, fileName)
            if ".log" not in fileName or ".DS_Store" in fileName:
                continue
            if "_nc" not in fileName:
                hasRF = 1
            else:
                hasRF = 0
            fname = fileName.split(".")[0]
            print fname
            featureExtract(quicDir, fname, ".log", hasRF)
            dicts.clear()
            featureDataDict.clear()
            featureDataCalculateDict.clear()
            metricsDict = {"lossAllNum":[], "avgBW":[]}
        break #skip the subdir

if __name__ == "__main__":
    extractAllFeature(quicDir)
    plotMetrics(quicDir)
