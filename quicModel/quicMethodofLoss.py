# coding = utf-8

import time
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.naive_bayes import BernoulliNB, GaussianNB


def DecisionTreeofLoss(X_train,X_test,y_train,y_test):
    # Make a decision tree and train
    model = DecisionTreeClassifier(max_depth=10,
                                  min_samples_leaf=25,
                                  min_samples_split=50)

    startT = time.time()
    model.fit(X_train, y_train)
    lastT = time.time()-startT
    print "the last time of DecisionTree is %.4fs!" %lastT
    return lastT,model


def RandomForestofLoss(X_train,X_test,y_train,y_test):
    # Create the model with 100 trees
    model = RandomForestClassifier(n_estimators=10, 
                                   bootstrap = True,
                                   max_features = 0.7,
                                   max_depth = 10,
                                   min_samples_leaf = 25,
                                   min_samples_split = 50)

    startT = time.time()
    # Fit on training data
    model.fit(X_train, y_train)
    lastT = time.time()-startT
    print "the last time of RandomForest is %.4fs!" %lastT
    #visualize of random forest tree
    return lastT,model


def AdaBoostofLoss(X_train,X_test,y_train,y_test):
    model = AdaBoostClassifier(n_estimators=10, learning_rate=1.0, algorithm='SAMME.R')
    startT = time.time()
    model.fit(X_train,y_train)
    lastT = time.time()-startT
    print "the last time of AdaBoost is %.4fs!" %lastT
    return lastT,model


def BaggingofLoss(X_train,X_test,y_train,y_test):
    model = BaggingClassifier(n_estimators=10, bootstrap=True)
    startT = time.time()
    model.fit(X_train,y_train)
    lastT = time.time()-startT
    print "the last time of Bagging is %.4fs!" %lastT
    return lastT,model


def NaiveBayesBernoulliNBofLoss(X_train,X_test,y_train,y_test):
    model = BernoulliNB()
    startT = time.time()
    model.fit(X_train,y_train)
    lastT = time.time()-startT
    print "the last time of NaiveBayesBernoulliNB is %.4fs!" %lastT
    return lastT,model


def NaiveBayesGaussianNBofLoss(X_train,X_test,y_train,y_test):
    model = GaussianNB() #default
    startT = time.time()
    model.fit(X_train,y_train)
    lastT = time.time()-startT
    print "the last time of NaiveBayesGaussianNB is %.4fs!" %lastT
    return lastT,model
