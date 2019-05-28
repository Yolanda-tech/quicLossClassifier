//
//  RandomForest.cpp
//  RandomForest
//
//  Created by wc on 15/6/11.
//  Copyright (c) 2015年 wc. All rights reserved.
//
//  Modified by yyj on 19/3/22.
//

#include "RandomForest.h"

// Get util message from util file.
// Initialize the util variable.
RandomForest::RandomForest() {
    trainNum = TREENUM;
    dataScale = DATASCALE;
    featureScale = FEATURESCALE;
    IsCombinateFeatureCol = ISCOMBINATEFEATURECOL;
}

// Free the memory.
RandomForest::~RandomForest() {
    deleteForest();
}

/********************************************************************
 * Description: Train random forest with the data set.
 *
 *@para mat Data set
 *@para featureName The feature name
 *@para argc The first parament of main function
 *@para argv The second parament of main function
 ********************************************************************/
void RandomForest::train(Mat& mat, Row &featureName, int argc, char *argv[]) {
    
    // If need to combinate the feature.
    if (IsCombinateFeatureCol) {
        composIndex = getComposFeatureIndex(featureName, 1);
        composFeature(mat, featureName, composIndex);
    } 
    
    Mat currentMat;
    Row currentFeatureName;
    this->getDataSet(mat, currentMat, featureName, currentFeatureName,
                     dataScale, featureScale, trainNum+1);
    DesionTree *trainTree = new DesionTree();
    
    // Create a tree and then store this tree in the processor who created it.
    trainTree->builtTree(currentMat, currentFeatureName);

    trees.push_back(trainTree);
}

/********************************************************************
 * Description: Predict with random forest.
 *
 *@para mat Data set
 *@para featureName The feature name
 *@para argc The first parament of main function
 *@para argv The second parament of main function
 *
 *@return The predict result
 ********************************************************************/
vector<ElementType> RandomForest::predict(Mat &mat, Row &featureName, int argc, char *argv[]) {
    
    int dataSize = (int)mat.size();
    vector< Row > result;
    
    if (IsCombinateFeatureCol) {
        composFeature(mat, featureName, composIndex);
    }
    
    for (auto tree : trees) {
        result.push_back(tree->predict(mat, featureName));
    }
    
    vector<ElementType> resultLabel = getLabelResult(result);

    return resultLabel;
}

// Get the result of each row in test data
// In each row, there are TREENUM numbers predict by
//      each tree. This function is to get the one
//      with max times.
vector<ElementType> RandomForest::getLabelResult(vector< Row > &resultList) {
    vector<ElementType> result;
    if (resultList.size() == 0)
        return result;
    
    // labelNumList id to store all the result of label predicted
    // and its times.
    vector<map<ElementType, int> > labelNumList;
    bool flag = true;
    for (auto row : resultList) {
        if (flag) {
            flag = false;
            for (auto item : row) {
                map<ElementType, int> temp;
                temp[item] = 1;
                labelNumList.push_back(temp);
            }
        } else {
            for (int i = 0; i < row.size(); ++i) {
                labelNumList[i][row[i]] += 1;
            }
        }
    }
    
    for (auto labelNum : labelNumList) {
        result.push_back(getResult(labelNum));
    }
    
    return result;
}

// Get the label with max times
ElementType RandomForest::getResult(map<ElementType, int> &labelNum) {
    int maxNum = 0;
    ElementType maxNumLabel = 0.0;
    for (auto item : labelNum) {
        if (maxNum < item.second) {
            maxNum = item.second;
            maxNumLabel = item.first;
        }
    }
    
    return maxNumLabel;
}

// This function is to get a dataset and its feature name for tree train
// To get the data set, you should provide the DATASCALE and FEATURESCALE,
//      which means the scale of the train data for each tree.
// The function chose the train data randomly. The parameter seed is to
// ensure the data set of each tree is different.
void RandomForest::getDataSet(Mat &sourceMat, Mat &aimMat, Row &featureName, Row &aimFeature,
                              double DataSetScale, double featureScale, int seed) {
    if (sourceMat.size() == 0) {
        cout<<"\tThe data set is empty!"<<endl;;
        return;
    }
    
    aimMat.clear();
    aimFeature.clear();
    
    int featureNum = (int)featureName.size();
    int dataSize = (int)sourceMat.size();
    
    int aimRowNum = (int)(DataSetScale * dataSize);
    int aimFeatureNum = (int)(featureScale * featureNum);
    
    //!!!NOTE!!!
    int labelIndex = (int)sourceMat[0].size() - 1;
    
    srand ((unsigned int)time(NULL) * seed);
    set<int> featureIndex;
    
    // The feature in one data set should be different.
    while (featureIndex.size() < aimFeatureNum) {
        int index = rand() % featureNum;
        featureIndex.insert(index);
    }
    
    // The rows in one data set can repeat. which means sampling with replacement
    while (aimMat.size() < aimRowNum) {
        Row rowTemp;
        int rowIndex = rand() % dataSize;
        for (auto featureIndex_  : featureIndex) {
            rowTemp.push_back(sourceMat[rowIndex][featureIndex_]);
        }
        rowTemp.push_back(sourceMat[rowIndex][labelIndex]);
        
        aimMat.push_back(rowTemp);
    }
    
    for (auto featureIndex_  : featureIndex)
        aimFeature.push_back(featureName[featureIndex_]);
}

// Combinate feature in double.
// This function not combinate all feature in composIndex to one
//      but make each double of them into one.
void RandomForest::composFeature(Mat &sourceMat, Row &featureName,
                                 vector<int> &composIndex) {
    int counter = 0;
    while (counter < composIndex.size()) {
        int comIndex1 = composIndex[counter++];
        int comIndex2 = composIndex[counter++];
        
        _composFeature(sourceMat, featureName, comIndex1, comIndex2);
    }
}

// Combinate two feature into one.
void RandomForest::_composFeature(Mat &sourceMat, Row &featureName, int index1, int index2) {
    assert(sourceMat.size() > 0);
    
    //!!!NOTE!!!:labelIndex is the last column
    int labelIndex = (int)sourceMat[0].size() - 1;
    
    Mat aimMat;
    Row aimFeatureName;
    
    for (int i = 0; i < sourceMat.size(); ++i) {
        Row rowTemp;
        for (int j = 0; j < featureName.size(); ++j) {
            if (j == index1 || j == index2) {
                if (j == index1) {
                    rowTemp.push_back(sourceMat[i][j] COMPOSOPERATION sourceMat[i][index2]);
                }
            } else {
                rowTemp.push_back(sourceMat[i][j]);
            }
        }
        rowTemp.push_back(sourceMat[i][labelIndex]);
        
        aimMat.push_back(rowTemp);
    }
    
    for (int j = 0; j < featureName.size(); ++j) {
        if (j != index2)
            aimFeatureName.push_back(featureName[j]);
    }
    sourceMat = aimMat;
    featureName = aimFeatureName;
}

// Get combinate feature randomly.
// The scale of feature to combinate is the same as the feature
//      one tree get from source data set, which is FEATURESCALE.
vector<int> RandomForest::getComposFeatureIndex(Row &featureName, int seed) {
    vector<int> featureIndex;
    int featureNum = (int)featureName.size();
    int aimFeatureNum = featureNum * featureScale;
    if (aimFeatureNum % 2 != 0)
        aimFeatureNum += 1;
    
    srand((unsigned int)time(NULL) * seed);
    while (featureIndex.size() < aimFeatureNum) {
        int index = rand() % featureNum;

        if (find(featureIndex.begin(), featureIndex.end(), index) == featureIndex.end()) {
            featureIndex.push_back(index);
        }
    }
    
    return featureIndex;
}

// Delete trees pointer in forest to free the memory.
void RandomForest::deleteForest() {
    for (int i = 0; i < trees.size(); ++i) {
        trees[i]->deleteTree();
        delete trees[i];
    }
    
    trees.clear();
}


void RandomForest::writeTreesToJson(Forest forest){
    Json::Value jsonTrees;
    Json::Value jsonValue(Json::arrayValue);
    for(auto tree: forest){
        std::string output;
        Json::Value value;
        CJsonSerializer::Serialize(tree, output, value);
        //std::cout << "testClass Serialized Output\n" << output << "\n\n\n";
        jsonValue.append(value);
    }
    jsonTrees["forest"] = jsonValue;

    Json::StreamWriterBuilder builder;
    std::string result;
    result = Json::writeString(builder, jsonTrees);
    std::ofstream ofs(FORESTFILE);  
    if (ofs) { 
        ofs << result; 
        ofs.close(); 
    } 
    else{
        cout<<"open file to write has error..."<<endl;
    }
}

Forest RandomForest::readJsonToTrees(){
    Forest forest;

    std::ifstream ifs(FORESTFILE);  
    std::string content;
    if (ifs) { 
        content.assign( (std::istreambuf_iterator<char>(ifs) ),(std::istreambuf_iterator<char>()) );
        ifs.close();
    } 
    Json::Value jsonValue;
    CJsonSerializer::SubDeserialize(content, jsonValue);  
    Json::Value arrayNum = jsonValue["forest"]; 
    for (unsigned int i = 0; i < arrayNum.size(); i++)
    {   
        DesionTree *subTree = new DesionTree();
        CJsonSerializer::JsonValueDeserialize(subTree, arrayNum[i]); 
        forest.push_back(subTree);
    }
    return forest;
}

bool RandomForest::predictIsCong(Mat mat){
    //Mat vector<vector<ElementType>> 
    //features<ConstantLostPacketCount,LostCount,LostDistWeight,LostPacketCount,inRcvry,inSS,Rlmrtt,Rlsrtt,Rsprtt>
    if(mat.size()!=1){
        cout << "wrong size of predict data..." << endl;
    }
    Row featureName;
    int colSize = (int)mat[0].size();

    for (int j = 1; j < colSize+1; ++j) {
        featureName.push_back(j);
    }

    vector<Row> result;

    for (auto tree : trees) {
        result.push_back(tree->predict(mat, featureName));
    }

    vector<ElementType> resultLabel = getLabelResult(result);

    if(resultLabel.size()!=1){
        cout << "wrong predict size:" << resultLabel.size() << endl;
    }
    cout << "predict:" <<resultLabel[0]<< ";isCong:" << (fabs(resultLabel[0]-CONGLABEL)<EPS) <<endl;
    return fabs(resultLabel[0]-CONGLABEL)<EPS;
}