# coding = utf-8

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

dataDir = "/Users/yuyajun/Downloads/quic_loss_project/quicLossExp/quicLog/"
def dataSplit(dataDir, file):
    path = dataDir + file
    columns = ['type',
               'ConstantLostPacketCount','LostCount','LostDistWeight','LostPacketCount',
               'inRcvry','inSS',
               'Rlmrtt','Rlsrtt','Rsprtt']
    '''df_wine.columns = ['type',
                       'ConstantLostPacketCount','LostCount','LostDistWeight','LostPacketCount',
                       'inRcvry','inSS',
                       'Rlmrtt','Rlsrtt','Rsprtt',
                       'BW','CongWin','LostDist','PacketAckedCount','Time','ackReceiveTime','loss','numAckEvent','retransmit','sent','net',
                       'latestRTT','minRTT','preRTT','smoothRTT']'''
    df_wine = pd.read_csv(path, usecols=columns, low_memory=False)
    ### pandas convert string to float
    #df_wine['Rsprtt'] = df_wine['Rsprtt'].convert_objects(convert_numeric=True) #ok
    df_wine['Rsprtt'] = pd.to_numeric(df_wine['Rsprtt'],errors='coerce') #ok
    #df_wine['Rsprtt'] = df_wine['Rsprtt'].astype(dtype=np.float64) #no 
    y, X = df_wine.ix[:, ['type']].values, df_wine.ix[:, columns[1:]].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    idColTrain = np.array([i for i in range(len(y_train))])
    idColTest = np.array([i for i in range(len(y_test))])
    idColAll = np.array([i for i in range(len(y))])
    fileTrain = "LossFeatureTrain.csv"
    fileTest = "LossFeatureTest.csv"
    fileTestLabel = "LossFeatureTestLabel.csv"
    fileAll = "LossFeatureAll.csv"
    pathTrain = dataDir + fileTrain
    pathTest = dataDir + fileTest
    pathTestLabel = dataDir + fileTestLabel
    pathAll = dataDir + fileAll
    fmt = "%d, %d, %d, %.4f, %d, %d, %d, %.4f, %.4f, %.4f"
    newColumns = ['id']
    newColumns.extend(columns[1:])
    test = np.column_stack((idColTest,X_test))
    np.savetxt(pathTest, test, delimiter = ',',fmt=fmt,header=",".join(newColumns))

    fmt = "%d, %d, %d, %.4f, %d, %d, %d, %.4f, %.4f, %.4f, %d"
    newColumns.append(columns[0])
    train= np.column_stack((idColTrain,X_train,y_train))
    np.savetxt(pathTrain, train, delimiter = ',',fmt=fmt,header=",".join(newColumns))
    testLabel = np.column_stack((idColTest,X_test, y_test))
    np.savetxt(pathTestLabel, testLabel, delimiter = ',',fmt=fmt,header=",".join(newColumns))
    all = np.column_stack((idColAll,X,y))
    np.savetxt(pathAll, all, delimiter = ',',fmt=fmt,header=",".join(newColumns))

if __name__ == "__main__":
    file = "MarkLossFeature0308AfterCalculate.csv"
    dataSplit(dataDir, file)