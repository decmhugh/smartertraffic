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
from sklearn.preprocessing import Normalizer
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
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from optparse import OptionParser

op = OptionParser()
op.add_option("--lsa",
              dest="n_components", type="int",
              help="Preprocess documents with latent semantic analysis.")
op.add_option("--no-minibatch",
              action="store_false", dest="minibatch", default=True,
              help="Use ordinary k-means algorithm (in batch mode).")
op.add_option("--no-idf",
              action="store_false", dest="use_idf", default=True,
              help="Disable Inverse Document Frequency feature weighting.")
op.add_option("--use-hashing",
              action="store_true", default=False,
              help="Use a hashing feature vectorizer")
op.add_option("--n-features", type=int, default=10000,
              help="Maximum number of features (dimensions)"
                   "to extract from text.")
op.add_option("--verbose",
              action="store_true", dest="verbose", default=False,
              help="Print progress reports inside k-means algorithm.")


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
feature = None


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
    
    results_traffic = collection_aa.find() 
    for i,item in enumerate(results_traffic):
        text = unicodedata.normalize('NFKD', item["text"]).encode('ascii','ignore').decode('utf-8')
        data.append(str(text))
        catagory.append(0)
    results_nontraffic = collection_mapped.find({"_id":{"$regex":"2014/04/26/2*"}}) 
    nontraffic = []
    data = data[:5000]
    catagory = catagory[:5000]
    #docs = [{f["text"]:"TRAFFIC"} for f in results_traffic]
    print(len(data), " TRAFFIC SIZE ")
    
    
    vectorizer =  TfidfVectorizer(
        analyzer='word',  # features made of words
        token_pattern=r'[a-z]{3,}',
        use_idf=True,
        strip_accents='unicode',
        ngram_range=(2,3),
        sublinear_tf=True, max_df=0.95, min_df=0.05,stop_words='english')
    #vectorizer =  DictVectorizer();
   
    X_train = vectorizer.fit_transform(data)
    X = Normalizer(copy=False).fit_transform(X_train)
    feature_names = vectorizer.get_feature_names()#np.vectorize(vectorizer.get_feature_names())
    km = KMeans(n_clusters=2, init='k-means++', max_iter=100, n_init=1,
                verbose=True)
    #print("Clustering sparse data with %s" % km)
    t0 = time()
    km.fit(X_train)
    #print("done in %0.3fs" % (time() - t0))
    #print()
    
    for i,l in enumerate(km.labels_):
        if ("thank" in data[i]):
            print(i, " ", l, " " ,data[i])
    

tweetread();     
