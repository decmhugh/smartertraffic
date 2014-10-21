'''
Created on 3 Dec 2013

@author: declan
'''

import csv, os, re
import pymongo
from pymongo import Connection as mongoConn
from datetime import datetime
from bson import json_util

connection_local = mongoConn('mongodb://localhost:27017/')
connection_remote = mongoConn('mongodb://admin:admin@ds063287.mongolab.com:63287/traffic')
db_local = connection_local.traffic
db_remote = connection_remote.traffic
cnn_local = db_local.twitter_mapped 
#cnn_remote = db_remote.twitter_streaming.find().skip(0).limit(2000)


#result = cnn_remote
data = {}
start = 0
end = 2000
cnn_remote = db_remote.twitter_streaming.find().skip(start).limit(end) 
result = cnn_remote;
json_str =json_util.dumps(result)
r =json_util.loads(json_str)
for item in r:
    item["timestamp"] = datetime.strptime(item["date"], '%Y-%m-%d %H:%M:%S ')
    item["day"] = item["timestamp"].strftime('%Y/%m/%d/%H')
    item["parent_id"] = item["timestamp"].strftime('%Y/%m/%d/%H')
    item["hour"] = item["timestamp"].strftime('%H')
    if not item["day"] in data.copy().keys():
        data[item["day"]] = {"item":[item]}
    else:
        data[item["day"]]["item"].append(item)
    
for d in data:
    print(d)
    result = cnn_local.find({"_id":d})
    json_str =json_util.dumps(result)
    record =json_util.loads(json_str)
    if len(record) > 0:
        r = record[0]
        print("Original Update Length: "+str(len(r["item"])))
        # update
        for newitem in data[d]["item"]:
            exist = False
            for i,res in enumerate(r["item"]):
                if newitem["item_id"] is item["item_id"]:
                    r["item"][i]=newitem
                    exist = True
            if not exist:
                    r["item"].append(newitem)
        cnn_local.save(r)
        print("Update Length: "+str(len(r["item"])))
                        
    else:
        # insert
        data[d]["_id"] = d
        data[d]["items_id"] = d
        print("Insert Length: "+str(len(data[d])))
        cnn_local.save(data[d])
                    
            
    
    