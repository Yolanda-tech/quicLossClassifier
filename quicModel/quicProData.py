# coding = utf-8

import json
import pandas as pd

def getData(dir, testData, trainData):
    trainPath = dir+trainData
    testPath = dir+testData

    df_train = pd.read_csv(trainPath)
    for col in list(df_train):
        df_train[col] = pd.to_numeric(df_train[col],errors='coerce')
    X_train, y_train = df_train.ix[:, 1:].values, df_train.ix[:, 0].values
    
    df_test = pd.read_csv(testPath)
    for col in list(df_test):
        df_test[col] = pd.to_numeric(df_test[col],errors='coerce')
    X_test, y_test = df_test.ix[:, 1:].values, df_test.ix[:, 0].values

    return X_train,X_test,y_train,y_test,list(df_train)[1:]



def saveToJson(lastTimes,accuracys,aucValues,scores,fis):
    fn = "modelValues.json"
    open(fn,'w').close()
    print "\nlastTimes:"
    print lastTimes
    print "\naccuracys:"
    print accuracys
    print "\naucValues:"
    print aucValues
    print "\nvarious scores:"
    print scores
    print scores['Bagging']
    print "\nfeature importance:"
    print fis
    with open(fn,'a') as file:
        file.write("lastTimes:\n")
        json.dump(lastTimes,file,ensure_ascii=False,encoding='utf-8')
        file.write("\naccuracys:\n")
        json.dump(accuracys,file,ensure_ascii=False,encoding='utf-8')
        file.write("\naucValues:\n")
        json.dump(aucValues,file,ensure_ascii=False,encoding='utf-8')
        file.write("\nscores:")
        for alg in scores.keys():
            file.write("\n%s:\n" %alg)
            file.write(scores[alg])
        file.write("\nfis:")
        for alg in fis.keys():
            file.write("\n%s:\n" %alg)
            file.write(str(fis[alg]))
        file.write("\n")
