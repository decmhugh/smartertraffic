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
    grouped = dframe.groupby(lambda x: x.hour)
    rec = []
    for hour, group in grouped:
        r = {}
        print(hour,"hour")
        q = [round(float(group["STT"].quantile(i/100)),2) for i in range(1,99)]
        f = round(float(group["STT"].std()),2)
        rec.append({"std": f,
                    "hour": int(hour),
                    "quantile":  q}) 
        
    rec = sorted(rec, key=lambda k: k['quantile'][80]).reverse()
    item = {"_id":args,"item":rec,"route":arg[0],"link":arg[1],"direction":arg[2]}
    print(item)
    db.peak_quatile80.insert(item)
        
        
       
    #db.peak_top.insert(rec)
        

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
    run()
        
     

    