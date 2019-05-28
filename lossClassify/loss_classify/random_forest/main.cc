//
//  main.cpp
//  RandomForest
//
//  Created by wc on 15/6/10.
//  Copyright (c) 2015年 wc. All rights reserved.
//


#include <json/json.h>
#include <iostream>
#include <sstream>
#include "DesionTree.h"
#include "RandomForest.h"

typedef vector<DesionTree*> Forest;

//Forest RandomForest::trees(Forest(0,nullptr));
Forest RandomForest::trees(RandomForest::readJsonToTrees());

int main(int argc, char * argv[]) {

    //RandomForest forest;
    //forest.trees = forest.readJsonToTrees();
    //Forest RandomForest::trees = RandomForest::readJsonToTrees();

    /*string mydata = Util::getInstance()->getUtil("MYDATA");
    cout<<"mydata:"<<mydata<<endl;
    double arr[10];
    int i = 0;
    stringstream ssin(mydata);
    while (ssin.good() && i < 10){
        string tmp;
        ssin >> tmp;
        arr[i] = stod(tmp);
        ++i;
    }*/
    
    double arr[] = {10, 2, 0.6000, 7, 1, 0, 1.0094, 0.9699, 0.9957};
    int size = sizeof(arr) / sizeof(double);
    std::vector<double> tmpv(arr,arr+size);

    Mat mat = std::vector<std::vector<double>>(1,tmpv);
    RandomForest forest;
    bool result = forest.predictIsCong(mat);
    //bool result = RandomForest::predictIsCong(mat);
    cout << "the predict result IsCong is" << result << endl;
    

    //forest.writeTreesToJson(forest.trees);

    return 0;
}
