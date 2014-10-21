'''
Created on 3 Dec 2013

@author: declan
'''
from pymongo import Connection as mongoConn
import unicodedata
connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
collection = db.twitter_stream 
collection_aa = db.twitter_aa 
collection_mapped = db.twitter_mapped

def tweetread():   
    results_nontraffic = collection_mapped.find({"_id":"2014/04/18/09"}) 
    for res in results_nontraffic:
        for item in res["item"]:
            text = unicodedata.normalize('NFKD', item["text"]).encode('ascii','ignore').decode('utf-8')
            print(text)
  
tweetread();     
