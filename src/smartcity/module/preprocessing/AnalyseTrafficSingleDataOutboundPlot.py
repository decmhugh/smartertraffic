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
    dframe = df.from_csv("traffic/min5_set_" + arg[0] + "_" + arg[1] + "_" + arg[2] + ".csv")
    return dframe
        
        
       
    #db.peak_top.insert(rec)
        

def run():
    cursor = db.junctions.find({"_id":"30/4/2"})
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    d1 = None
    for junction in junctions:
        d1 = process(junction["_id"])
        
    cursor = db.junctions.find({"_id":"10/7/2"})
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    d2 = None
    for junction in junctions:
        d2 = process(junction["_id"])
    
    cursor = db.junctions.find({"_id":"16/2/2"})
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    d3 = None
    for junction in junctions:
        d3 = process(junction["_id"])
        #d3.plot()
    
    d = df({
            "Low - 30/4/2": [d1["STT"].quantile(i/100) for i in range(1,99,10)],
            "Medium - 10/7/2":[d2["STT"].quantile(i/100) for i in range(1,99,10)],
            "High - 16/2/2":[d3["STT"].quantile(i/100) for i in range(1,99,10)]
            })
    d.plot(ylim=[0,600])
    
    #d_series = df({
    #        "Low - 9/1/1": d1["STT"].values,
    #        "Medium - 16/2/2":d2["STT"].values,
    #        "High - 10/8/2":d3["STT"].values
    #        })
    #d_series.plot()
    #d_series.resample("D").plot()
    #d_series.resample("W").plot()
    #x = np.array(d3["STT"].values)
    #print(x)
    #y = len(np.array(d1["STT"].values))
    #plt.plot(x, range(0,y), 'bo')
    plt.show()
    
   
if __name__ == "__main__":
    #process(sys.argv[1])
    pd.options.display.float_format = '{:20.2f}'.format
    run()
        
     

    