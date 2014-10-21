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

def getseries(q):
    arg = q.split("/")
    series1 = {"route":arg[0],"link":arg[1],"direction":arg[2]}
    result = db.observation.find(series1).sort("_id", -1)
    data = []
    dates = []
    for res in result:
        d = res["item"]
        for res2 in d:
            data.append(res2["stt"])
            dates.append(res2['date'])
    ts = TimeSeries(data,dates)   
    result = ts.resample('D')
    return result

def process(args):
    dframe = getseries(args)
    return dframe
        
        
       
    #db.peak_top.insert(rec)
        

def run():
    #cursor = db.junctions.find({"_id":"40/1/1"})
    d1 = process("30/4/2")
    d2 = d1["2014-01-01":"2014-04-15"].dropna().values
    d3 = d1["2013-05-01":"2013-08-01"].dropna().values
    d4 = d1["2012-09-01":"2012-10-31"].dropna().values
    a = np.append(d4,np.append(d3,d2))
    plt.plot(a)  
    plt.show()
    
   
if __name__ == "__main__":
    #process(sys.argv[1])
    pd.options.display.float_format = '{:20.2f}'.format
    run()
        
     

    