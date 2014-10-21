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

connection_local = mongoConn('mongodb://localhost:27017/')
db_local = connection_local.traffic
db = connection_local.traffic
rawtweets = db_local.twitter_mapped 
#cnn_remote = db_remote.twitter_streaming.find().skip(0).limit(2000)

texts = []
values = []

def predict(param):
    q = {"_id":param}
    qtime = {"time": param }
    print(q)
    tweet = db.tweetitems.find(q)
    predict = db.predict_real.find(qtime)
    twititems = []
    for record in tweet:
        print("tweet")
        twititems = record['item'] 
    tweets =json.dumps(twititems, separators=(',',':'))
    tweets =json_util.loads(tweets)
    predictitems = []
    for res in predict:  
        print("predict")
        predictitems.append(res)        
    pred = json.dumps(predictitems, separators=(',',':'))
    pred =json_util.loads(pred)

    return {"tweets":tweets,"traffic":pred}

def feed(param):
    result={}
    tweetdata = rawtweets.find(param)
    json_str =json_util.dumps(tweetdata)
    tweetdata =json_util.loads(json_str)
    path = os.path.dirname(os.path.realpath(__file__))
    for tweetlist in tweetdata:
        for tweet in tweetlist["item"]:
            #d = datetime.strptime(tweetlist["_id"], '%Y/%m/%d/%H')
            result[tweetlist["_id"]] = tweetlist["item"];
            if not tweet["geo"] == "None":
                geo = tweet["geo"]
                pt1 = geopy.Point(geo['coordinates'][0], geo['coordinates'][1])
                #AMIENS STREET TALBOT STREET
                pt2 = geopy.Point(53.337711529200433,-6.265935340601275)
                #pt2 = geopy.Point(53.346951058081927,-6.259268157760138)
                dist = geopy.distance.distance(pt1, pt2).km
                text = unicodedata.normalize('NFKD', tweet["text"]).encode('ascii','ignore').decode('utf-8')
                if dist < 1:
                    #if "traffic" in text:
                    item = {"text":text,"geo":geo}
                    print(text,geo)
                    texts.append(text)
                    values.append(item)

    return json.dumps(values)
if __name__ == "__main__":
    param = "2014/04/21/20"
    print(predict(param))
        
if __name__ == "__main3__":
    param = {"_id":"2014/04/25/18"}
    v = feed(param);
    trans = TfidfTransformer()
    vectorizer = TfidfVectorizer(
        analyzer='word',
        token_pattern=r'[a-z]{5,}',
        use_idf=True,
        stop_words='english',
        strip_accents='unicode',
        sublinear_tf=True)
    print(len(texts))
    vectorizer.fit_transform(texts)
    idf = vectorizer._tfidf.idf_
    z = [list(a) for a in zip(vectorizer.get_feature_names(), idf)]
    print(len(z))
    z = sorted(z, key=itemgetter(1))
    
    
    for a in z:
        print(a)
    