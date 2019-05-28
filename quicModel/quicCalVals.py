# coding = utf-8

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score,classification_report


def calAccuracy(classifiers,X_train, X_test,y_train, y_test):
    Accuracys = {}
    for clf, name in classifiers:
        #print type(model)
        meanAccuracy = clf.score(np.concatenate((X_train, X_test), axis=0),np.concatenate((y_train, y_test), axis=0))
        #print "Model Accuracy of %s: %.4f!" %(name,meanAccuracy)

        testAccuracy = clf.score(X_test,y_test)
        #print "Model Test Accuracy of %s: %.4f!" %(name,testAccuracy)

        trainAccuracy = clf.score(X_train,y_train)
        #print "Model Train Accuracy of %s: %.4f!" %(name,trainAccuracy)
        
        Accuracys[name] = [meanAccuracy,testAccuracy,trainAccuracy]

    #print Accuracys
    return Accuracys


def calScore(classifiers,X_train, X_test,y_train, y_test):
    aucValues = {}
    scores = {}
    for clf, name in classifiers:
        # Actual class predictions
        rf_predictions = clf.predict(X_test)
        # Probabilities for each class
        if hasattr(clf, "predict_proba"):
            rf_probs = clf.predict_proba(X_test)[:, 1]
        else:  # use decision function
            rf_probs = clf.decision_function(X_test)
            rf_probs = \
                (rf_probs - rf_probs.min()) / (rf_probs.max() - rf_probs.min())

        # Calculate roc auc
        auc_value = roc_auc_score(y_test, rf_probs)
        score = classification_report(y_test, rf_predictions, digits=4)#, target_names=target_names)
        aucValues[name] = auc_value
        scores[name] = score
    return aucValues,scores


def calfeatureimportance(classifiers, features, top):
    fis = {}
    fitop = {}
    for clf, name in classifiers:
        if hasattr(clf, "feature_importances_"):
            #confusion matrix
            # Extract feature importances
            fi = pd.DataFrame({'feature': features,'importance': clf.feature_importances_}).\
                            sort_values('importance', ascending = False)
            fis[name] = fi#print fi #.head()
            fitop[name] = fi.head(top)

    return fis,fitop
