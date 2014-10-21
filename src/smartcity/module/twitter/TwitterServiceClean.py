'''
Created on 3 Dec 2013

@author: declan
'''

import pymongo, geopy
from geopy import distance
from pymongo import Connection as mongoConn
from datetime import datetime
from bson import json_util
import json,os
import unicodedata
from pprint import pprint
import pickle

connection_local = mongoConn('mongodb://localhost:27017/')
db_local = connection_local.traffic
rawtweets = db_local.twitter_mapped_old 
#cnn_remote = db_remote.twitter_streaming.find().skip(0).limit(2000)

def feed(param):
    values=[]
    result={}
    tweetdata = rawtweets.find()
    json_str =json_util.dumps(tweetdata)
    tweetdata =json_util.loads(json_str)
    path = os.path.dirname(os.path.realpath(__file__))
    filename = path + '/classifier.pickle'
    vectorizorname = path + '/vector.pickle'
    print(filename)
    print(vectorizorname)
    f = open(filename, 'rb')
    v = open(vectorizorname, 'rb')
    classifier = pickle.load(f);
    vectorizor = pickle.load(v);
    f.close();
    v.close();
    for tweetlist in tweetdata:
        for tweet in tweetlist["item"]:
            #d = datetime.strptime(tweetlist["_id"], '%Y/%m/%d/%H')
            result[tweetlist["_id"]] = tweetlist["item"];
            if not tweet["geo"] == "None":
                geo = json.loads(tweet["geo"].replace("'", '"'))
                pt1 = geopy.Point(geo["coordinates"][0], geo["coordinates"][1])
                pt2 = geopy.Point(53.346951058081927,-6.259268157760138)
                dist = geopy.distance.distance(pt1, pt2).km
                text = unicodedata.normalize('NFKD', tweet["text"]).encode('ascii','ignore').decode('utf-8')
                vector_text = vectorizor.transform([text])
                if dist < 21:
                    tweet = {}
                    tweet["text"] = str(text)
                    tweet["dist"] = dist
                    tweet["geo"]  = geo
                    values.append(tweet)
        tweetlist["item"] = values
        db_local.twitter_clean.insert(tweetlist)
    #return json.dumps(values)
if __name__ == "__main__":
    param = {"_id":"2014/04/17/12"}
    v = feed(param);
    print(v)
    