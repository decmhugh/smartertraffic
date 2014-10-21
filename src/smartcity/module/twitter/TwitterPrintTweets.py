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
from sklearn.feature_extraction.text import CountVectorizer
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

vectorizer =  CountVectorizer(
        analyzer='word',  # features made of words
        token_pattern=r'[a-z]{2,}',
        strip_accents='unicode',
        stop_words='english')

    

def tweetread():   
    data = []
    catagory = []
    
    results_traffic = collection_aa.find() 
    for i,item in enumerate(results_traffic):
        text = unicodedata.normalize('NFKD', item["text"]).encode('ascii','ignore').decode('utf-8')
        text = re.sub(r"@([A-Za-z]+[A-Za-z]+[A-Za-z0-9-_\.]+)", "", text)
        print(str(text))
        data.append(text)
    
    X_train = vectorizer.fit_transform(data)
    feature_names = vectorizer.get_feature_names()
    print(feature_names);

    
    #simple thing to do would be to up the n-grams to bigrams; try varying ngram_range from (1, 1) to (1, 2)
    #we could also modify the vectorizer to stem or lemmatize
    #print('\nHere is the confusion matrix:');


tweetread();     
