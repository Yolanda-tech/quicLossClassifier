//
//  DesionTree.h
//  RandomForest
//
//  Created by wc on 15/6/10.
//  Copyright (c) 2015年 wc. All rights reserved.
//
//  Modified by yyj on 19/3/22.
//

#ifndef __RandomForest__DesionTree__
#define __RandomForest__DesionTree__

#include <vector>
#include <string>
#include <stack>
#include <map>
#include <json/json.h>
#include <sstream>
#include <assert.h>
#include "JsonParser.h"

using namespace std;

typedef double ElementType;
typedef vector<ElementType> Row;
typedef vector<Row> Mat;

struct Node{
    Mat _mat;
    int _level;
    ElementType _splitFeatureName;
    ElementType _splitFeatureValue;
    ElementType _label;
    
    Node *_left;
    Node *_right;
    
    Node():
        _left(nullptr),
        _right(nullptr){};

    Node(Mat mat,
         int level = 1,
         ElementType splitFeatureName = 0.0,
         ElementType splitFeatureValue = 0.0,
         ElementType label = 0.0,
         Node *left = nullptr,
         Node *right = nullptr) :
        _mat(mat),
        _level(level),
        _splitFeatureName(splitFeatureName),
        _splitFeatureValue(splitFeatureValue),
        _label(label),
        _left(left),
        _right(right){}
};

typedef Node* treeNode;

class DesionTree : public IJsonSerializable {
public:
    DesionTree();
    ~DesionTree();
    
    void builtTree(Mat &mat, Row &featureName);
    Row predict(Mat &mat, Row &featureName);
    void deleteTree();
    
    virtual void Serialize( Json::Value& root);
    virtual void Deserialize( Json::Value& root);
private:
    bool idLabelTheSame(Mat &mat);
    map<ElementType, int> getLabelNum(Mat &mat);
    ElementType getLabel(Mat &mat);
    void getBestSplitFeatureInfo(Mat &mat, Row &feature,
                                 int &bestSplitFeatureIndex,
                                 ElementType &splitFeatureValue);
    double getMinGiniGain(Mat &mat, int featureIndex, ElementType &splitValue);
    double getGini(map<ElementType, int> &labelNum, double &total);
    double getGiniGain(map<ElementType, int> &leftLabel,
                       map<ElementType, int> &rightLabel);
    void splitMat(Mat &mat,
                  Mat &mat1,
                  Mat &mat2,
                  int bestSplitFeatureIndex,
                  ElementType &splitFeatureValue);
    ElementType classify(Row &row, map<ElementType, int> &featureIndex);
    
    void clearTree();
public: //private:
    treeNode _tree;
};

void _serialize( Json::Value& root, treeNode& tree);
void _deserialize(Json::Value& root, treeNode& tree);
bool findKeyAndValue(Json::Value& root,std::string key, Json::Value &value);

#endif /* defined(__RandomForest__DesionTree__) */
