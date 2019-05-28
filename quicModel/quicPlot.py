# coding = utf-8

import numpy as np
from sklearn.tree import export_graphviz
from sklearn.calibration import calibration_curve
from sklearn.metrics import auc,roc_curve,confusion_matrix
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.naive_bayes import GaussianNB

#from sklearn.utils.multiclass import unique_labels
import pydotplus
#import collections
#import graphviz
#from subprocess import call
#from IPython.display import Image

def calibrationPlot(classifiers, X_train, X_test, y_train, y_test):
    # Plot calibration plots
    plt.figure(figsize=(10, 10))
    ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
    ax2 = plt.subplot2grid((3, 1), (2, 0))

    ax1.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")
    for clf, name in classifiers:
        clf.fit(X_train, y_train)
        if hasattr(clf, "predict_proba"):
            prob_pos = clf.predict_proba(X_test)[:, 1]
        else:  # use decision function
            prob_pos = clf.decision_function(X_test)
            prob_pos = \
                (prob_pos - prob_pos.min()) / (prob_pos.max() - prob_pos.min())
        fraction_of_positives, mean_predicted_value = \
            calibration_curve(y_test, prob_pos, n_bins=10)

        ax1.plot(mean_predicted_value, fraction_of_positives, "s-",
                 label="%s" % (name, ))

        ax2.hist(prob_pos, range=(0, 1), bins=10, label=name,
                 histtype="step", lw=2)

    ax1.set_ylabel("Fraction of positives")
    ax1.set_ylim([-0.05, 1.05])
    ax1.legend(loc="lower right")
    ax1.set_title('Calibration plots  (reliability curve)')

    ax2.set_xlabel("Mean predicted value")
    ax2.set_ylabel("Count")
    ax2.legend(loc="upper center", ncol=2)

    #plt.tight_layout()
    plt.show()
    plt.close()


def decisionTreeVisualization(model,features,displayDepth,class_names,rf=False,treei=0):

    # Visualize data
    dot_data = export_graphviz(model,
                                max_depth = displayDepth,
                                feature_names=features,
                                class_names=class_names,
                                proportion = True, ## samples = 34395
                                out_file=None,
                                filled=True,
                                rounded=True)
    '''# Convert to png using system command (requires Graphviz)
    call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])

    # Display in jupyter notebook
    Image(filename = 'tree.png')
    '''
    ###graph = graphviz.Source(dot_data) ###sudo pip install graphviz

    graph = pydotplus.graph_from_dot_data(dot_data)
    '''
    colors = ('lightskyblue', 'pink')
    edges = collections.defaultdict(list)

    for edge in graph.get_edge_list():
        edges[edge.get_source()].append(int(edge.get_destination()))

    for edge in edges:
        edges[edge].sort()    
        for i in range(2):
            dest = graph.get_node(str(edges[edge][i]))[0]
            dest.set_fillcolor(colors[i])
    '''
    if not rf:
        graph.write_pdf('fig/decisionTree.pdf')
    else:
        graph.write_pdf('fig/randomForestTree%d.pdf' %treei)

def plot_confusion_matrix(method, y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    np.set_printoptions(precision=2)
    if not title:
        if normalize:
            title =""
            #title = 'Normalized confusion matrix of %s' %method
        else:
            title = 'Confusion matrix, without normalization of %s' %method

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    #print y_true[:10],y_pred[:10]
    #classes = classes[unique_labels(y_true, y_pred)]#
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title)
    plt.xlabel('Predicted label',fontsize=20)
    #plt.ylabel('True label',fontsize=20)
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center",
             rotation_mode="anchor",fontsize=17)
    plt.setp(ax.get_yticklabels(), rotation=90, ha="center",
             rotation_mode="anchor", fontsize=17, 
             verticalalignment = 'baseline')

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center", fontsize=22, 
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    fig.savefig("fig/confusionMatrixof%s%d.pdf" %(method,normalize))   

    #plt.show()
    plt.close()
    return ax


def confusionMatrixPlot(classifiers, X_test, y_test, class_names):
    print "start confusion matrix plot..."
    for clf, name in classifiers:
        y_pred = clf.predict(X_test)
        # Plot non-normalized confusion matrix
        plot_confusion_matrix(name, y_test, y_pred, classes=class_names)
        # Plot normalized confusion matrix
        plot_confusion_matrix(name, y_test, y_pred, classes=class_names, normalize=True)


def rocPlot(classifiers, X_train, X_test, y_train, y_test):
    print "start roc plot..."
    plt.figure()
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    for clf, name in classifiers:
        #clf.fit(X_train, y_train)
        if hasattr(clf, "predict_proba"):
            prob_pos = clf.predict_proba(X_test)[:, 1]
        else:  # use decision function
            print "use decision function------"
            prob_pos = clf.decision_function(X_test)
            prob_pos = \
                (prob_pos - prob_pos.min()) / (prob_pos.max() - prob_pos.min())

         # Compute ROC curve and ROC area for each class
        
        fpr, tpr, _ = roc_curve(y_test, prob_pos)
        roc_auc = auc(fpr, tpr)

        plt.plot(fpr, tpr, ".-",
                 label="%s (area = %.3f)" % (name, roc_auc))
   
        # Compute micro-average ROC curve and ROC area
        '''fpr = dict()
        tpr = dict()
        roc_auc = dict()
        fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), prob_pos.ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])'''
    
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('FPR or (1-specificity)',fontsize=18)
    plt.ylabel('TPR or sensitivity',fontsize=18)
    plt.title('ROC curve',fontsize=18)
    plt.legend(loc="lower right",fontsize=15)
    plt.savefig("fig/rocCurve.pdf")
    plt.close()
    #plt.show()


def classifierCompPlot(names, topFeatures, X_train, X_test, y_train, y_test):
    findex = topFeatures.index
    if len(findex)< 2:
        raise Exception("The length of topFeatures has to be larger than 1",len(findex))

    featureIndex = findex.tolist()
    #featureIndex = [7,8]

    X_train = X_train[:,featureIndex]
    X_test = X_test[:,featureIndex]

    classifiers = [DecisionTreeClassifier(max_depth=10,
                                          min_samples_leaf=25,
                                          min_samples_split=50),
                    RandomForestClassifier(n_estimators=10, 
                                           bootstrap = True,
                                           max_features = 0.7,
                                           max_depth = 10,
                                           min_samples_leaf = 25,
                                           min_samples_split = 50),
                    AdaBoostClassifier(n_estimators=50, learning_rate=1.0, algorithm='SAMME.R'),
                    BaggingClassifier(n_estimators=50, bootstrap=True),
                    GaussianNB()]
 
    h = 0.2
    datasetLen = 1

    figure = plt.figure(figsize=(35, 4))
    i = 1

    X = np.concatenate((X_train, X_test), axis=0)
    y = np.concatenate((y_train, y_test), axis=0)

    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    # just plot the dataset first
    cm = plt.cm.RdBu
    cm_bright = ListedColormap(['#FF0000', '#0000FF'])
    ax = plt.subplot(datasetLen, len(classifiers) + 1, i)
    ax.set_title("Input data")
    # Plot the training points
    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright,
               edgecolors='k')
    # Plot the testing points
    ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, alpha=0.6,
               edgecolors='k')
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_xticks(())
    ax.set_yticks(())
    i += 1

    # iterate over classifiers
    for name, clf in zip(names, classifiers):
        ax = plt.subplot(datasetLen, len(classifiers) + 1, i)
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)

        # Plot the decision boundary. For that, we will assign a color to each
        # point in the mesh [x_min, x_max]x[y_min, y_max].
        if hasattr(clf, "decision_function"):
            Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
        else:
            Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)

        # Plot the training points
        ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright,
                   edgecolors='k')
        # Plot the testing points
        ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright,
                   edgecolors='k', alpha=0.6)

        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xticks(())
        ax.set_yticks(())
        ax.set_title(name)
        ax.text(xx.max() - 5, yy.max() - 32, ('%.2f' % score).lstrip('0'),
                size=15, horizontalalignment='right')
        i += 1

    plt.tight_layout()
    plt.savefig("fig/classifierComp.pdf")
    plt.show()
    plt.close()










