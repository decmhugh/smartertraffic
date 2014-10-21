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



connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic

def process(args):
    #print(args)
    arg = args.split("/")
    csv = "traffic/min5_set_" + arg[0] + "_" + arg[1] + "_" + arg[2] + ".csv"
    print(csv)
    dframe = df.from_csv(csv)
    grouped = dframe.groupby(lambda x: x.hour)
    rec = []
    for hour, group in grouped:
        print(hour,"hour")
        group['weekday'] = [x.weekday() for x in group.index]
        group = group[group['weekday'] > 4]
        r = {}
        q = [round(float(group["STT"].quantile(i/100)),2) for i in range(1,99)]
        f = round(float(group["STT"].std()),2)
        r = {"std": f,
                    "hour": int(hour),
                    "quantile80": float(group["STT"].quantile(.80)),
                    "obs_quantile":  q}
        r["obs_count"] = float(group["STT"].count())
        r["obs_min"] = float(group["STT"].min())
        r["obs_max"] = float(group["STT"].max())
        r["obs_std"] = float(group["STT"].std())
        r["obs_mean"] = float(group["STT"].mean())
        r["obs_median"] = float(group["STT"].median())
        rec.append(r) 
    rec = sorted(rec, key=lambda k: k['quantile80'])[::-1]
    dframe['weekday'] = [x.weekday() for x in dframe.index]
    dframe = dframe[dframe['weekday'] > 4]
    item = {"_id":args,"item":rec,"route":arg[0],"link":arg[1],"direction":arg[2]}
    item["obs_count"] = float(group["STT"].count())
    item["obs_quantile"] = [dframe["STT"].quantile(i/100) for i in range(1,99)]
    item["obs_min"] = float(group["STT"].min())
    item["obs_max"] = float(group["STT"].max())
    item["obs_std"] = float(group["STT"].std())
    item["obs_mean"] = float(group["STT"].mean())
    item["obs_median"] = float(group["STT"].median())
    db.peak_weekend.remove({"_id":args})
    db.peak_weekend.insert(item)
        

def run():
    cursor = db.junctions.find()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in junctions:
        process(junction["_id"])
   
if __name__ == "__main__":
    #process(sys.argv[1])
    pd.options.display.float_format = '{:20.2f}'.format
    b = [1.0,50.67]
    a = [2.0,30.67]
    a1 = [1.0,40.67]
    c = {"hour":1,"item":[a,b,a1]}
    #item = c['item']
    #item = sorted(item, key=lambda k: k[1])
    #print(item[::-1])
    run()
        
     

    