//
//  RandomForest.h
//  RandomForest
//
//  Created by wc on 15/6/11.
//  Copyright (c) 2015年 wc. All rights reserved.
//  
//  Modified by yyj on 19/3/22.
//

#ifndef __RandomForest__RandomForest__
#define __RandomForest__RandomForest__

#include "DesionTree.h"
#include <cmath>
#include <set>
#include <algorithm>
#include <fstream>

// This three utils are used only if the util file can't use.
#define TREENUM 10         // The tree number of the forest
#define DATASCALE 0.8         // The data set scale for each tree
#define FEATURESCALE 0.75    // The feature scale for each tree


#define ISCOMBINATEFEATURECOL false  // If do feature combinate operation
#define COMPOSOPERATION + // The operation of feature combinate

#define FORESTFILE "../result/forest.json"
#define CONGLABEL 0
const double EPS = 1e-6;

typedef vector<DesionTree*> Forest;

class RandomForest {
public:
    RandomForest();
    ~RandomForest();
    
    void train(Mat& mat, Row &featureName, int argc, char *argv[]); 
    vector<ElementType> predict(Mat &mat, Row &featureName,int argc, char *argv[]);
    void deleteForest();

    void writeTreesToJson(Forest forest);
    static Forest readJsonToTrees();
    bool predictIsCong(Mat mat);

public:
    static Forest trees;
private:
    vector<int> composIndex;
    int trainNum;
    double dataScale;
    double featureScale;
    bool IsCombinateFeatureCol;
    
private:
    void getDataSet(Mat &sourceMat, Mat &aimMat,
                    Row &featureName, Row &aimFeature,
                    double DataSetScale, double featureScale,
                    int seed);
    vector<ElementType> getLabelResult(vector< Row > &result);
    ElementType getResult(map<ElementType, int> &labelNum);
    void composFeature(Mat &sourceMat, Row &featureName, vector<int> &composIndex);
    void _composFeature(Mat &sourceMat, Row &featureName, int index1, int index2);
    
    vector<int> getComposFeatureIndex(Row &featureName, int seed);
};

#endif /* defined(__RandomForest__RandomForest__) */
