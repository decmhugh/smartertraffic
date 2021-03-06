'''
Created on 3 Dec 2013

@author: declan
'''
from pymongo import Connection as mongoConn
import os,gc,sys
import numpy as np
from datetime import datetime
from matplotlib import pylab as plt
from pandas.core.series import TimeSeries
from pandas import DataFrame as df
from pandas.stats.moments import ewma
from sklearn import linear_model
import json,pickle
from bson import json_util
import memcache
from sklearn.externals import joblib
import pandas as pd

from sklearn.svm.classes import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.utils.extmath import pinvh
from scipy import linalg
from sklearn.utils.extmath import density
from sklearn import metrics
rain = None
wind = None
temperature = None
mem = memcache.Client(["localhost:11211"])
connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
pickle_dir = None

def getstt(item):  
    time=[]   
    for i in item:
        time.append(i["stt"]) 
    return time 

def getseries(q):
    pkl = "observation_" + q["route"] + "_" + q["link"] + "_" + q["direction"]
    print(q)
    result = db.observation.find(q).sort("_id", -1) 
    data = []
    dates = []
    for res in result:
        d = res["item"]
        for res2 in d:
            data.append(res2["stt"])
            dates.append(res2['date'])
    ts = TimeSeries(data,dates)   

    result = ts.resample('10min', how="mean",convention='end',fill_method='pad')
    stt = (result["2014-01-13":"2014-04-21"].dropna().values)
    idx = (result["2014-01-13":"2014-04-21"].dropna().index.values)
    ts = TimeSeries(stt,idx)  
    return ts

def process_lock(args):
    print(datetime.now())
    print(args)
    dir = args.split("/")
    pickle_dir = "../prediction/pickle/sample/" + args.replace("/","_")
    if not os.path.exists(pickle_dir):
        os.makedirs(pickle_dir)
    series1 = {"route":dir[0],"link":dir[1],"direction":dir[2],"day":{"$regex":"201404*"}}
    selected_series = getseries(series1)
    ds = {"STT":selected_series}
    dframe = df(ds)
    
    dframe.to_csv(pickle_dir +  "/" + "data.csv")
    
    
def run():
    cursor = db.junctions.find()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in junctions:
        print(junction["_id"])
        dir = junction["_id"].split("/")
        pickle_dir = "../prediction/pickle/sample/" + junction["_id"].replace("/","_")
        process_lock(junction["_id"])
               
if __name__ == "__main__":
    #"13/2/1","30/7/1","10/7/2"
    #for p in ["18/2/1"]:
    run()
    
    #for p in ["17/6/1","13/2/1","30/7/1","10/7/2","16/2/2","30/4/2"]:
    #    pickle_dir = "pickle/" + p.replace("/","_")
    #    if not os.path.exists(pickle_dir):
    #        print(pickle_dir)
    #        os.mkdir(pickle_dir) 
        #process_lock(p)
        
     

    