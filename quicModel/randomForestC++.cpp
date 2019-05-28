#include <iostream>

#include <fstream>

#include <sstream>

#include "random_forest.h"

 

using namespace std;

 

vector<decision_tree*>  alltrees;               // 森林（决策树集合）

vector<TupleData>       trainAll,train,test; // 样本集

vector<int>                  attributes;            // 属性集（元素为属性序号）

 

int                     trainAllNum = 0;      

int                     testAllNum  = 0;      

int                     MaxAttr;             // 属性总数

int                     *ArrtNum;               // 属性个数集（元素为属性最大值）

unsigned int            F;

int                     tree_num    = 100;     // 决策树个数

const int               leafattrnum = -1;       // 叶子节点的属性序号

int                     TP          = 0,

                        FN          = 0,

                        FP          = 0,

                        TN          = 0,

                        TestP       = 0,

                        TestN       = 0;

 

// 读入数据

void init(char * trainname, char * testname)

{

   trainAllNum     =readData(trainAll, trainname);

   testAllNum      = readData(test,testname);

   calculate_attributes();

   double temp     =(double)trainAllNum;

   temp            =log(temp)/log(2.0);

   F               = (unsigned int)floor(temp+0.5)+1;

   if(F>MaxAttr) F = MaxAttr;

}

 

// 初始化训练样本子集

void sub_init()

{

   // 选取决策树的训练样本集合

   RandomSelectData(trainAll, train);

 

   // 计算样本属性个数

   calculate_ArrtNum();

}

 

// 读数据

int readData(vector<TupleData>&data, const char* fileName)

{

   ifstream fin;

   fin.open(fileName);

   string line;

 

   int datanum=0;

 

   // 每行数据作为一个样本

   while(getline(fin,line))

   {

       TupleData d;

       istringstream stream(line);

       string str;

 

       // 设置每个样本的标签和内容

       while(stream>>str)

       {

           if(str.find('+')==0)

           {

                d.label='+';

           }

           else if(str.find('-')==0)

           {

                d.label='-';

           }

           else

           {

                int j=stringtoint(str);

                d.A.push_back(j);

           }

       }

 

       data.push_back(d);

       datanum++;

   }

 

   fin.close();

   return datanum;

}

 

// 生成根节点的训练样本子集

voidRandomSelectData(vector<TupleData> &data, vector<TupleData>&subdata)

{

   int index;

   subdata.clear();

   int d = 0;

   while (d < trainAllNum)

   {

       index = rand() % trainAllNum;

       subdata.push_back(data.at(index));

       d++;

   }

}

 

// 计算属性序列

void calculate_attributes()

{

   // 每个样本必须具有相同的属性个数

   TupleData d = trainAll.at(0);

   MaxAttr = d.A.size();

   attributes.clear();

 

   // 建立属性集合attributes,元素为属性序号

   for (int i = 0; i < MaxAttr; i++)

   {

       attributes.push_back(i);

   }

 

   // 初始化属性最大值序列，元素为属性最大值

   ArrtNum = new int[MaxAttr];

}

 

// 字符串转化为int

int stringtoint(string s)

{

   int sum=0;

   for(int i=0; s[i]!='\0';i++)

   {

       int j=int(s[i])-48;

       sum=sum*10+j;

   }

   return sum;

}

 

// 计算ArrtNum元素值

void calculate_ArrtNum()

{

   for(int i = 0; i < MaxAttr; i++) ArrtNum[i] = 0;

 

   // ArrtNum元素值为属性最大值

   for (vector<TupleData>::const_iterator it = train.begin(); it !=train.end(); it++)

   {

       int i = 0;

 

       for (vector<int>::const_iterator intt=(*it).A.begin();intt!=(*it).A.end();intt++)

       {

           int valuemax=(*intt)+1;

           if(valuemax>ArrtNum[i]) ArrtNum[i]=valuemax;

           i++;

       }

   }

}

 

// 计算熵

double Entropy(double p, double s)

{

   double n = s - p;

   double result = 0;

   if (n != 0)

       result += - double(n) / s * log(double(n) / s) / log(2.0);

   if (p != 0)

       result += double(-p) / s * log(double(p) / s) / log(2.0);

   return result;

}

 

// 训练一棵决策树

int creat_classifier(decision_tree*&p, const vector<TupleData> &samples, vector<int>&attributes)

{

   if (p == NULL)

       p = new decision_tree();

 

   // 根据样本真实类别，输出叶子节点类别

   if (Allthesame(samples, '+'))

   {

       p->node.label = '+';

       p->node.attrNum = leafattrnum;

       p->childs.clear();

       return 1;

   }

   if (Allthesame(samples, '-'))

   {

       p->node.label = '-';

       p->node.attrNum = leafattrnum;

       p->childs.clear();

       return 1;

   }

   // 如果属性序列为空，当前节点就为叶子节点

   if (attributes.size() == 0)

   {

       p->node.label = Majorityclass(samples);

       p->node.attrNum = leafattrnum;

       p->childs.clear();

       return 1;

   }

 

   // 计算当前节点的最优属性

   p->node.attrNum = BestGainArrt(samples, attributes);

 

   // 中间节点无标签

   p->node.label = ' ';

 

   // 计算子节点候选属性集合，候选集合元素越来越少

   vector<int> newAttributes;

   for (vector<int>::iterator it = attributes.begin(); it !=attributes.end(); it++)

       if ((*it) != p->node.attrNum)

           newAttributes.push_back((*it));

 

   // 初始化样本子集，建立maxvalue个样本子集，也就说明该节点有maxvalue个子节点

   // 为什么不建立一个阈值，进行二分类？

   int maxvalue = ArrtNum[p->node.attrNum];

   vector<TupleData>* subSamples = newvector<TupleData>[maxvalue];

   for (int i = 0; i < maxvalue; i++)

       subSamples[i].clear();

 

   // 将样本集合分为样本子集

   for (vector<TupleData>::const_iterator it = samples.begin(); it !=samples.end(); it++)

   {

       // 对样本进行分类，分别分到maxvalue个子节点中

       // p->node.attrNum是当前节点的最优属性序号

       // (*it).A.at(p->node.attrNum)正是子节点的序号

       // 基于当前节点最优属性，计算当前样本的归类

       subSamples[(*it).A.at(p->node.attrNum)].push_back((*it));

   }

 

   decision_tree *child;

   for (int i = 0; i < maxvalue; i++)

   {

       child = new decision_tree;

 

       if (subSamples[i].size() == 0)

           child->node.label = Majorityclass(samples);

       else

           creat_classifier(child, subSamples[i], newAttributes);

 

       p->childs.push_back(child);

   }

   delete[] subSamples;

   return 0;

}

 

// 计算节点处的信息增益

int BestGainArrt(constvector<TupleData> &samples, vector<int> &attributes)

{

   int attr,

       bestAttr = 0,

       p = 0,

       s = (int)samples.size();

 

   // 计算正样本个数

   for (vector<TupleData>::const_iterator it = samples.begin(); it !=samples.end(); it++)

   {

       if ((*it).label == '+')

           p++;

   }

 

   double infoD;

   double bestResult = 0;

 

   // 计算初始熵

   infoD = Entropy(p, s);

 

   vector<int> m_attributes;

 

   // 随机确定候选属性集

   RandomSelectAttr(attributes, m_attributes);

 

   // 遍历属性（即主题），通过信息增益筛选最优属性

   for (vector<int>::iterator it = m_attributes.begin(); it !=m_attributes.end(); it++)

   {

       attr            = (*it);

       double result   = infoD;

 

       // 第attr个属性的最大属性值

       int maxvalue    = ArrtNum[attr];

 

       // 正负样本集

       int* subN       = newint[maxvalue];

       int* subP       = newint[maxvalue];

       int* sub        = newint[maxvalue];

 

       for (int i = 0; i < maxvalue; i++)

       {

           subN[i] = 0;

           subP[i] = 0;

           sub[i]  = 0;

       }

 

       // 基于特定属性，对当前训练样本进行分类

       // 属性计算这一步的确没有，属性值直接存储在样本中

       for (vector<TupleData>::const_iterator jt = samples.begin(); jt !=samples.end(); jt++)

       {

           if ((*jt).label == '+')

                subP[(*jt).A.at(attr)] ++;

           else

                subN[(*jt).A.at(attr)] ++;

           sub[(*jt).A.at(attr)]++;

       }

 

       // 计算特定属性下信息增益（相对熵）

       double SplitInfo = 0;

       for(int i = 0; i < maxvalue; i++)

       {

           double partsplitinfo;

           partsplitinfo   =-double(sub[i])/s*log(double(sub[i])/s)/log(2.0);

           SplitInfo       =SplitInfo+partsplitinfo;

       }

 

       double infoattr = 0;

       for (int i = 0; i < maxvalue; i++)

       {

           double partentropy;

           partentropy     = Entropy(subP[i],subP[i] + subN[i]);

           infoattr        =infoattr+((double)(subP[i] + subN[i])/(double)(s))*partentropy;

       }

       result = result - infoattr;

       result = result / SplitInfo;

 

       // 寻找最优属性

       if (result > bestResult)

       {

           bestResult      = result;

           bestAttr        = attr;

       }

       delete[] subN;

       delete[] subP;

       delete[] sub;

   }

 

   if (bestResult == 0)

   {

       bestAttr=attributes.at(0);

   }

   return bestAttr;

}

 

void RandomSelectAttr(vector<int>&data, vector<int> &subdata)

{

   int index;

   unsigned int dataNum=data.size();

   subdata.clear();

   if(dataNum<=F)

   {

       for (vector<int>::iterator it = data.begin(); it != data.end();it++)

       {

           int attr = (*it);

           subdata.push_back(attr);

       }

   }

   else

   {

       set<int> AttrSet;

       AttrSet.clear();

       while (AttrSet.size() < F)

       {

           index = rand() % dataNum;

           if (AttrSet.count(index) == 0)

           {

                AttrSet.insert(index);

               subdata.push_back(data.at(index));

           }

       }

   }

}

 

bool Allthesame(constvector<TupleData> &samples, char ch)

{

   for (vector<TupleData>::const_iterator it = samples.begin(); it !=samples.end(); it++)

       if ((*it).label != ch)

           return false;

   return true;

}

 

// 确定节点中哪个类别样本个数最多

char Majorityclass(constvector<TupleData> &samples)

{

   int p = 0, n = 0;

   for (vector<TupleData>::const_iterator it = samples.begin(); it !=samples.end(); it++)

       if ((*it).label == '+')

           p++;

       else

           n++;

   if (p >= n)

       return '+';

   else

       return '-';

}

 

// 测试阶段

char testClassifier(decision_tree *p,TupleData d)

{

   // 抵达叶子节点

   if (p->node.label != ' ')

       return p->node.label;

 

   // 节点处最优属性

   int attrNum = p->node.attrNum;

 

   // 错误样本

   if (d.A.at(attrNum) < 0)

       return ' ';

 

   // 确定分支

   return testClassifier(p->childs.at(d.A.at(attrNum)), d);

}

 

void testData()

{

   for (vector<TupleData>::iterator it = test.begin(); it !=test.end(); it++)

   {

       printf("新样本\n");

       if((*it).label=='+') TestP++;

       else TestN++;

 

       int p = 0, n = 0;

 

       for(int i = 0; i < tree_num; i++)

       {

           if(testClassifier(alltrees.at(i), (*it))=='+')  p++;

           else n++;

       }

 

       if(p>n)

       {

           if((*it).label=='+') TP++;

           else FP++;

       }

       else

       {

           if((*it).label=='+') FN++;

           else TN++;

       }

   }

}

 

void freeClassifier(decision_tree *p)

{

   if (p == NULL)

       return;

   for (vector<decision_tree*>::iterator it = p->childs.begin();it != p->childs.end(); it++)

   {

       freeClassifier(*it);

   }

   delete p;

}

 

void freeArrtNum()

{

   delete[] ArrtNum;

}

 

void showResult()

{

   cout << "Train size:   "<<trainAllNum<<endl;

   cout << "Test size:    "<<testAllNum<<endl;     

   cout << "True positive:        "<< TP << endl;

   cout << "False negative:       "<<FN<<endl;

   cout << "False positive:       "<<FP<<endl;

   cout << "True negative:        "<<TN<<endl;

}

 

int main(int argc, char **argv)

{

   char * trainfile=argv[1];

    char* testfile=argv[2];

 

   srand((unsigned)time(NULL));

 

   // 初始化样本

   init("1.txt", "2.txt");

 

   // 训练阶段

   for(int i = 0; i < tree_num; i++)

   {

       printf("第 %d 棵决策树训练开始\n", i);

 

       // 每棵树的训练样本子集

       sub_init();

 

       // 训练每棵决策树

       decision_tree * root=NULL;

       creat_classifier(root, train, attributes);

 

       // 建立森林

       alltrees.push_back(root);

       printf("第 %d 棵决策树训练完毕\n", i);

   }

 

   // 测试阶段

   testData();

 

   for (vector<decision_tree *>::const_iterator it =alltrees.begin(); it != alltrees.end(); it++)

   {

       freeClassifier((*it));

   }

 

   freeArrtNum();

 

   showResult();

 

   system("pause");

   return 0;

}