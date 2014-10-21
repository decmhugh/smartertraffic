'''
Created on 3 Dec 2013

@author: declan
'''

import csv, os, re
import pymongo
from pymongo import Connection as mongoConn
from datetime import datetime
from bson import json_util
from pandas.core.series import TimeSeries
from pandas import DataFrame as df

connection_local = mongoConn('mongodb://localhost:27017/')
db_local = connection_local.traffic
rawtweets = db_local.twitter_mapped 
#cnn_remote = db_remote.twitter_streaming.find().skip(0).limit(2000)


dates=[]
values=[]
result={}

tweetdata = rawtweets.find()
for tweetlist in tweetdata:
    d = datetime.strptime(tweetlist["_id"], '%Y/%m/%d/%H')
    result[tweetlist["_id"]] = tweetlist["item"];
    dates.append(d)
    values.append(len(tweetlist["item"]))
    #print(d, len(tweetlist["item"]))
ts = TimeSeries(dates,values) 
print(ts.head(100))   
    