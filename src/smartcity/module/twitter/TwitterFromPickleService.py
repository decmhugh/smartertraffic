'''
Created on 3 Dec 2013

@author: declan
'''
from pymongo import Connection as mongoConn
from bson import json_util
import json,os
import unicodedata
import pickle

connection_local = mongoConn('mongodb://localhost:27017/')
db_local = connection_local.traffic
rawtweets = db_local.twitter_mapped 
#cnn_remote = db_remote.twitter_streaming.find().skip(0).limit(2000)



def feed(param):
    values=[]
    result={}
    tweetdata = rawtweets.find(param)
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
                geo = tweet["geo"]
                text = unicodedata.normalize('NFKD', tweet["text"]).encode('ascii','ignore').decode('utf-8')
                vector_text = vectorizor.transform([text])
                item = {"text":text,"geo":geo,"label":str(classifier.predict(vector_text)[0])}
                #print(item);
                values.append(item)
    
    return json.dumps(values)
if __name__ == "__main__":
    param = {"_id":"2014/04/17/12"}
    v = feed(param);
    print(v)
    