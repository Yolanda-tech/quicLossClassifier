#coding=utf-8

from dataForPLT import getSubDirAndFile,plotAvgPLT
from featureExtract_Cong import extractAllFeature,plotMetrics
from heatmapFig import File

fileName = "0402(1)small"#"0411small"#"0408small"#"0403thin"#"0402(2)thin"#"0403(1)small/"
PLTDIR =  "/Users/yuyajun/Downloads/quic_loss_project/quicLossExp/quicPLT/before/"+fileName
quicDir = "/Users/yuyajun/Downloads/quic_loss_project/quicLossExp/quicLog/"+fileName

FileType = "small"

if __name__ == '__main__':
    if File != FileType:
        print "please modify *File* in heatmapFig.py to *FileType*\n"
    else:
        keys,currentDir,combAvgPLT = getSubDirAndFile(PLTDIR)
        plotAvgPLT(currentDir,combAvgPLT,keys)
        
        '''extractAllFeature(quicDir)
        plotMetrics(quicDir)'''