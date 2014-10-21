'''
Created on 3 Dec 2013

@author: declan
'''
from pymongo import Connection as mongoConn
from bson import json_util
import json,os
import unicodedata
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline

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
    texts = []
    for tweetlist in tweetdata:
        for tweet in tweetlist["item"]:
            #d = datetime.strptime(tweetlist["_id"], '%Y/%m/%d/%H')
            result[tweetlist["_id"]] = tweetlist["item"];
            if not tweet["geo"] == "None":
                geo = tweet["geo"]
                text = unicodedata.normalize('NFKD', tweet["text"]).encode('ascii','ignore').decode('utf-8')
                item = {"text":text,"geo":geo}
                texts.append(text)
                values.append(item)
    vectorizer = TfidfVectorizer(analyzer='word',
        token_pattern=r'[a-z]{3,}',
        use_idf=True,
        strip_accents='unicode',
        ngram_range=(2,3),
        sublinear_tf=True, max_df=0.95, min_df=0.05,stop_words='english')
    print(texts[:10])
    X = vectorizer.fit_transform(texts[:10])
    print(vectorizer.get_feature_names())
    print(X.toarray())
    
    
    return json.dumps(values)
if __name__ == "__main__":
    param = {"_id":"2014/04/17/12"}
    v = feed(param);
    