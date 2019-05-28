# coding = utf-8
import warnings
from quicProData import getData,saveToJson
from quicMethodofLoss import DecisionTreeofLoss,RandomForestofLoss,AdaBoostofLoss,BaggingofLoss,NaiveBayesGaussianNBofLoss
from quicCalVals import calAccuracy,calScore,calfeatureimportance
from quicPlot import rocPlot,confusionMatrixPlot,decisionTreeVisualization,classifierCompPlot
# 1->nonCongLoss 0->congLoss

dataDir = "/Users/yuyajun/Downloads/quic_loss_project/quicLossExp/quicLog/0308/"
class_names = ["congLoss", "nonCongLoss"]

if __name__ == "__main__":
    try:
        testData = "LossFeatureTest0312.csv"
        trainData = "LossFeatureTrain0312.csv"

        algorithm = ["DecisionTree","RandomForest","AdaBoost","Bagging","NaiveBayesGaussianNB"] #"NaiveBayesBernoulliNB"

        selectTopFeatures = 2
        if selectTopFeatures < 2:
            warnings.warn("If the classifierCompPlot is needed, the selectTopFeatures have to be larger than 1.")

        X_train,X_test,y_train,y_test,features = getData(dataDir, testData, trainData)

        classifiers = []
        lastTimes = {}
        displayDepth = 2

        lastT,model = DecisionTreeofLoss(X_train,X_test,y_train,y_test)
        classifiers.append((model,algorithm[0]))
        lastTimes[algorithm[0]] = lastT
        decisionTreeVisualization(model, features, displayDepth, class_names)
        
        lastT,model = RandomForestofLoss(X_train,X_test,y_train,y_test)
        classifiers.append((model,algorithm[1]))
        lastTimes[algorithm[1]] = lastT
        i = 0
        for treeInForest in model.estimators_:
            decisionTreeVisualization(treeInForest, features, displayDepth, class_names, True, i)
            i = i + 1

        lastT,model = AdaBoostofLoss(X_train,X_test,y_train,y_test)
        classifiers.append((model,algorithm[2]))
        lastTimes[algorithm[2]] = lastT

        lastT,model = BaggingofLoss(X_train,X_test,y_train,y_test)
        classifiers.append((model,algorithm[3]))
        lastTimes[algorithm[3]] = lastT

        #NaiveBayesBernoulliNBofLoss(dataDir,testData,trainData)
        lastT,model = NaiveBayesGaussianNBofLoss(X_train,X_test,y_train,y_test)
        classifiers.append((model,algorithm[4]))
        lastTimes[algorithm[4]] = lastT

        accuracys = calAccuracy(classifiers,X_train, X_test,y_train, y_test)
        aucValues,scores = calScore(classifiers,X_train, X_test,y_train, y_test)
        fis, fitop = calfeatureimportance(classifiers, features, selectTopFeatures)

        saveToJson(lastTimes,accuracys,aucValues,scores,fis)

        #calibrationPlot(classifiers, X_train, X_test, y_train, y_test)
        rocPlot(classifiers, X_train, X_test, y_train, y_test)
        confusionMatrixPlot(classifiers, X_test, y_test, class_names)
        methodFItop = "RandomForest"
        #classifierCompPlot(algorithm, fitop[methodFItop], X_train, X_test, y_train, y_test)
        
    except Exception,err:
        print "err:",err
    else:
        print "Happy ending!"
        

