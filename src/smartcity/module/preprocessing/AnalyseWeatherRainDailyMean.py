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
data = None

def getstt(item):  
    time=[]   
    for i in item:
        time.append(i["stt"]) 
    return time    

def getseriesweather(location):
    data = db.weather.find({"location":location}).sort("_id", -1)
    
    dates = []
    HourlyPrecipMM = []
    
    
    for res in (data):
        for res2 in (res['item']):
            HourlyPrecipMM.append(float(res2["HourlyPrecipMM"]))
            dates.append(datetime.strptime(res2['Time'],'%Y-%m-%d %H:%M:%S'))
    
    res = TimeSeries(HourlyPrecipMM,dates)
    
    return res


def process(args):
    
    #['ICODUBLI2','ILEINSTE8','IDUBLINC2']
    
    dframe1 = getseriesweather("ICODUBLI2").resample("D", how="mean",convention='end',fill_method="pad")
    dframe2 = getseriesweather("ILEINSTE8").resample("D", how="mean",convention='end',fill_method="pad")
    dframe3 = getseriesweather("IDUBLINC2").resample("D", how="mean",convention='end',fill_method="pad")
    dframe = df({"ICODUBLI2":dframe1,"ILEINSTE8":dframe2,"IDUBLINC2":dframe3})
    
    dframe.plot()
    dframe.hist()
    print(dframe.corr())
    plt.show()
    #dframe.plot()
    
    #plt.show()
             
    
   
if __name__ == "__main__":
    #process(sys.argv[1])
    process(sys.argv)
        
     

    