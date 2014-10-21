'''
Created on 3 Dec 2013

@author: declan
'''
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
import pickle
from pymongo import Connection as mongoConn
import nltk
from sklearn import metrics
import nltk.downloader as d
from nltk.corpus import treebank
from nltk import sem
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from time import time
import sys
import os
from pandas import DataFrame as df
import numpy as np
import scipy.sparse as sp
import pylab as pl
import unicodedata
from sklearn.datasets import load_mlcomp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier,RidgeClassifier,Perceptron,PassiveAggressiveClassifier
from sklearn.feature_extraction.dict_vectorizer import DictVectorizer
import json
connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic

data = []
catagory = []
train_test_data = None
vectorizer = {}
parameters = {}

traffic_label = []
nontraffic_label = []
traffic_scores = []
nontraffic_scores = []

def show_most_informative_features(vectorizer, clf, n=10):
    c_f = sorted(zip(clf.coef_[0], vectorizer.get_feature_names()))
    
    
    
    cf = c_f[:n]
    val,score = [x[1] for x in cf],[x[0] for x in cf]
    for y in val:
        traffic_label.append(str(y))
    for y in score:
        traffic_scores.append(str(y))
        
    cf = c_f[:-(n+1):-1]
    val,score = [x[1] for x in cf],[x[0] for x in cf]
    for y in val:
        nontraffic_label.append(str(y))
    for y in score:
        nontraffic_scores.append(str(y))
def check_in(words , text):
    for w in words:
        if w in text: 
            return True
    return False
    

def tweetread():   
    f = open('classifier.pickle', 'rb')
    v = open('vector.pickle', 'rb')
    nb_classifier = pickle.load(f)
    vectorizer = pickle.load(v)
    f.close()
    results_nontraffic = db.twitter_mapped.find({"_id":{"$regex":"2014/04/21/20*"}}) 
    tweetitems = []
    predictitems = []
    
    for res in results_nontraffic:
        for item in res["item"]:
            text = unicodedata.normalize('NFKD', item["text"]).encode('ascii','ignore').decode('utf-8')
            X_test = vectorizer.transform([text])
            y_nb_predicted = nb_classifier.predict(X_test)
            #score = metrics.f1_score(X_test, y_nb_predicted)
            if y_nb_predicted == 0:
                #if check_in(['delays', 'crash', 'cleared'] , text):
                #print(res["_id"])
                print("PREDICTED", text)
                
                tweetitems.append(item)
    db.tweetitems.remove({"_id":"2014/04/21/20"})
    db.tweetitems.insert({"_id":"2014/04/21/20","item":tweetitems})
    result = db.predict_real.find()
    for res in result:  
        predictitems.append(res)        
    
    return {"tweets":json.dumps(tweetitems, separators=(',',':'))
            ,"traffic":json.dumps(predictitems, separators=(',',':'))}
    #simple thing to do would be to up the n-grams to bigrams; try varying ngram_range from (1, 1) to (1, 2)
    #we could also modify the vectorizer to stem or lemmatize
    #print('\nHere is the confusion matrix:');


print(tweetread());     
