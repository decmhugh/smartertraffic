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
connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
collection = db.twitter_stream 
collection_aa = db.twitter_aa 
collection_mapped = db.twitter_mapped

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
    data = []
    catagory = []
    
    results_traffic = collection_aa.find({"manualtype":{"$ne":"/^non*/"}}) 
    for i,item in enumerate(results_traffic):
        text = unicodedata.normalize('NFKD', item["text"]).encode('ascii','ignore').decode('utf-8')
        text = re.sub(r"@([A-Za-z]+[A-Za-z]+[A-Za-z0-9-_\.]+)", "", text)
        print(text)
        data.append(str(text))
        catagory.append(0)
    results_nontraffic = collection_mapped.find({"_id":{"$regex":"2014/04/18/09*"}}) 
    nontraffic = []
    data = data[:5000]
    catagory = catagory[:5000]
    #docs = [{f["text"]:"TRAFFIC"} for f in results_traffic]
    print(len(data), " TRAFFIC SIZE ")
    
    for res in results_nontraffic:
        #print(len(res["item"]))
        for i in res["item"]:
            if len(data) < 10000:
                text = unicodedata.normalize('NFKD', i["text"]).encode('ascii','ignore').decode('utf-8')
                #if not check_in(['delays', 'crash', 'cleared'] , text):
                text = re.sub(r"@([A-Za-z]+[A-Za-z0-9-_\.]+)", "", text)
                print(text)
                data.append(text)
                catagory.append(1)
                #else:
                #    print(text)
    print(len(data), "SAMPLE SIZE ")
    vectorizer =  TfidfVectorizer(
        analyzer='word',  # features made of words
        token_pattern=r'[a-z]{3,}',
        use_idf=True,
        strip_accents='unicode',
        #ngram_range=(2,3),
        sublinear_tf=True, max_df=0.95, min_df=0.05,stop_words='english')
    #vectorizer =  DictVectorizer();
   
    X_train = vectorizer.fit_transform(data)
    X_test = vectorizer.transform(data)
    feature_names = vectorizer.get_feature_names()#np.vectorize(vectorizer.get_feature_names())
    
    
    
    #BernoulliNB(alpha=.01)
    #nb_classifier = BernoulliNB(alpha=.01).fit(X_train, catagory)
    #nb_classifier = RidgeClassifier(tol=1e-2, solver="lsqr").fit(X_train, catagory)
    #nb_classifier = Perceptron(n_iter=50).fit(X_train, catagory)
    b = [BernoulliNB(alpha=.01).fit(X_train, catagory),
         RidgeClassifier(tol=1e-2, solver="lsqr").fit(X_train, catagory),
         PassiveAggressiveClassifier(n_iter=50).fit(X_train, catagory)]
    nb_classifier = PassiveAggressiveClassifier(n_iter=50).fit(X_train, catagory)
    #nb_classifier = MultinomialNB(alpha=.01).fit(X_train, catagory)
    y_nb_predicted = nb_classifier.predict(X_test)
    

    print("Dimensionality: %d" % nb_classifier.coef_.shape[0])
    print('\nHere is the classification report:');
    print(classification_report(catagory, y_nb_predicted));
    print(metrics.confusion_matrix(catagory, y_nb_predicted, labels=[0,1]))
        
    results_nontraffic = collection_mapped.find({"_id":{"$regex":"2014/04/*"}}) 
    nontraffic = []
    data = data[:1000]
    catagory = catagory[:1000]
    print(len(data), " TRAFFIC SIZE ")
    
    
    for res in results_nontraffic:
        for item in res["item"]:
            text = unicodedata.normalize('NFKD', item["text"]).encode('ascii','ignore').decode('utf-8')
            X_test = vectorizer.transform([text])
            y_nb_predicted = nb_classifier.predict(X_test)
            #score = metrics.f1_score(X_test, y_nb_predicted)
            if y_nb_predicted == 0:
                #if check_in(['delays', 'crash', 'cleared'] , text):
                print( text, "&" , "\\\\")
                
    
    #simple thing to do would be to up the n-grams to bigrams; try varying ngram_range from (1, 1) to (1, 2)
    #we could also modify the vectorizer to stem or lemmatize
    #print('\nHere is the confusion matrix:');


tweetread();     
