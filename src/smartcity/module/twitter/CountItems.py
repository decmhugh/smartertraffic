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
weather = db.weather


results_nontraffic = weather.find() 
i = 0

for res in results_nontraffic:
    for item in res["item"]:
        i += 1
print("weather",i)
            
    
