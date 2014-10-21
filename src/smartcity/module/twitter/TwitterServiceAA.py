'''
Created on 3 Dec 2013

@author: declan
'''
from pymongo import Connection as mongoConn
from bson import json_util
import json,os,unicodedata,geopy,numpy,csv
from geopy import distance
from time import sleep
from operator import itemgetter
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.preprocessing import normalize


connection_local = mongoConn('mongodb://localhost:27017/')
db_local = connection_local.traffic
rawtweets = db_local.twitter_aa
#cnn_remote = db_remote.twitter_streaming.find().skip(0).limit(2000)

def feed(param):
    values=[]
    result={}
    tweetdata = rawtweets.find()
    json_str =json_util.dumps(tweetdata)
    tweetdata =json_util.loads(json_str)
    path = os.path.dirname(os.path.realpath(__file__))
    texts = []
    for tweetlist in tweetdata:
        tweet = tweetlist["text"]
        print(tweet)
        #d = datetime.strptime(tweetlist["_id"], '%Y/%m/%d/%H')
        text = unicodedata.normalize('NFKD', tweet).encode('ascii','ignore').decode('utf-8')
        texts.append(text)
    vectorizer = TfidfVectorizer(
        analyzer='char',
        #token_pattern=r'[a-z]{4,}',
        #use_idf=True,
        #strip_accents='unicode',
        #sublinear_tf=False
        )
    print(len(texts))
    vectorizer.build_analyzer()
    idf = vectorizer.fit_transform(texts)
    feature_names = np.asarray(vectorizer.get_feature_names())
    #print(idf.todense().T)
    #print((idf * idf.T).A)
    #print(idf.data)
    print("len ",(feature_names))
    z = (zip(feature_names,idf.data))
    
    d = {}
    for t in z:
        #print(t[0],t[1])
        d[t[0]] = t[1] 
    #print(d)
    return d
if __name__ == "__main__":
    param = {"_id":"2014/04/25/12"}
    v = feed(param);
    