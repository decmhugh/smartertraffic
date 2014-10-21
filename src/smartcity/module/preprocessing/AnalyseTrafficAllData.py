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

connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic

def getstt(item):  
    time=[]   
    for i in item:
        time.append(i["stt"]) 
    return time    

def getseriesweather(attr,bool,location):
    result = db.weather.find({"location":location}).sort("_id", -1)
    
    weather = []
    dates = []

    for res in (result):
        for res2 in (res['item']):
            if set((attr,'Time')).issubset(res2.keys()):
                weather.append(float(res2[attr]))
                dates.append(datetime.strptime(res2['Time'],'%Y-%m-%d %H:%M:%S'))
    ts = TimeSeries(weather,dates)  
    result = ts.resample('10min', how=bool,convention='end',fill_method="pad")
    return result

def getseries(q):
    pkl = "observation_" + q["route"] + "_" + q["link"] + "_" + q["direction"]
    
    result = db.observation.find(q).sort("_id", -1)
        
    data = []
    dates = []
    for res in result:
        d = res["item"]
        for res2 in d:
            data.append(res2["stt"])
            dates.append(res2['date'])
    ts = TimeSeries(data,dates)   
    result = ts.resample('10min', how="mean",convention='end',fill_method="pad")
    return result

def process_lock(args):
    print(args)
    arg = args.split("/")
    series1 = {"route":arg[0],"link":arg[1],"direction":arg[2]}
    ds = {"STT":getseries(series1)}
    dframe = df(ds)
    dframe.to_csv("traffic/min5_set_" + arg[0] + "_" + arg[1] + "_" + arg[2] + ".csv")
    dframe["STT"].fillna(dframe["STT"].mean())
    print(dframe["STT"].describe())
    rec = {}
    
    rec["obs_count"] = float(dframe["STT"].count())
    rec["obs_min"] = float(dframe["STT"].min())
    rec["obs_max"] = float(dframe["STT"].max())
    rec["obs_quantile"] = [dframe["STT"].quantile(i/100) for i in range(1,99)]
    rec["obs_std"] = float(dframe["STT"].std())
    rec["obs_mean"] = float(dframe["STT"].mean())
    rec["obs_median"] = float(dframe["STT"].median())
    rec["_id"] = args
    print(rec["obs_quantile"])
    db.obs_stats.insert(rec)
    
    
             
    
def process(args):
    process_lock(args)  

def run():
    cursor = db.junctions.find()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in junctions:
        res = db.obs_stats.find_one({"_id":junction["_id"]})
        process(junction["_id"])
   
if __name__ == "__main__":
    #process(sys.argv[1])
    pd.options.display.float_format = '{:20.2f}'.format
    run()
        
     

    