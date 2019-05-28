//
//  JsonParser.cpp
//  RandomForest
//
//  Created by yyj on 19/3/22.
//  Copyright (c) 2019年 yyj. All rights reserved.
//

#ifndef __RandomForest__JsonParser__
#define __RandomForest__JsonParser__

#include <json/json.h>
#include <iostream>
#include <sstream>

class IJsonSerializable
{
public:
   virtual ~IJsonSerializable( void ) {};
   virtual void Serialize( Json::Value& root) =0;
   virtual void Deserialize( Json::Value& root) =0;
};

class CJsonSerializer
{
public:
   static void SubSerialize( std::string& output, Json::Value& serializeRoot);
   static bool Serialize( IJsonSerializable* pObj, std::string& output, Json::Value& serializeRoot);
   
   static bool SubDeserialize( std::string& input, Json::Value& deserializeRoot );
   static void JsonValueDeserialize( IJsonSerializable* pObj, Json::Value& deserializeRoot);
   static bool Deserialize( IJsonSerializable* pObj, std::string& input, Json::Value& deserializeRoot );
 
private:
   CJsonSerializer( void ) {};
};

#endif