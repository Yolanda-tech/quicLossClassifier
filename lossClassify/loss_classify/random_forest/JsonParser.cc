//
//  JsonParser.cpp
//  RandomForest
//
//  Created by yyj on 19/3/22.
//  Copyright (c) 2019年 yyj. All rights reserved.
//

#include "JsonParser.h"

using namespace std;

// json value(serializeRoot) to string(output)
void CJsonSerializer::SubSerialize(std::string& output, Json::Value& serializeRoot){
    /*OK
    ostringstream ostr;
    Json::StreamWriterBuilder builder;
    unique_ptr<Json::StreamWriter> writer(builder.newStreamWriter());
    writer->write(serializeRoot, &ostr);
    output = ostr.str();

    return true;*/

    Json::StreamWriterBuilder builder;
    output = Json::writeString(builder, serializeRoot);
}

// pObj serialize json value(serializeRoot) to string(output)
bool CJsonSerializer::Serialize( IJsonSerializable* pObj, std::string& output, Json::Value& serializeRoot)
{
    
    if (pObj == NULL)
        return false;
      
    pObj->Serialize(serializeRoot);
    
    CJsonSerializer::SubSerialize(output, serializeRoot);
    
    return true;
}

// string(input) to json value(deserializeRoot)
bool CJsonSerializer::SubDeserialize( std::string& input, Json::Value& deserializeRoot)
{
    Json::CharReaderBuilder builder;
    JSONCPP_STRING errs;

    /*OK
    unique_ptr<Json::CharReader> const reader(builder.newCharReader());
    const char *pStart = input.c_str();
    int nLen = input.length();

    if (!reader->parse(pStart, pStart + nLen, &deserializeRoot, &errs))
        return false;

    pObj->Deserialize(deserializeRoot);

    return true;*/

    istringstream istr(input);
    if (!Json::parseFromStream(builder, istr, &deserializeRoot, &errs))
    {
        return false;
    }
    return true;
}

// pObj deserialize the json value(deserializeRoot)
void CJsonSerializer::JsonValueDeserialize( IJsonSerializable* pObj, Json::Value& deserializeRoot){
    pObj->Deserialize(deserializeRoot);
}

// from string(input) to json value(deserializeRoot) and pObj deserializes 
bool CJsonSerializer::Deserialize( IJsonSerializable* pObj, std::string& input, Json::Value& deserializeRoot)
{   
    if (pObj == NULL)
        return false;

    if(!CJsonSerializer::SubDeserialize( input, deserializeRoot)){
        return false;
    }
    CJsonSerializer::JsonValueDeserialize( pObj, deserializeRoot);

    return true;
}
