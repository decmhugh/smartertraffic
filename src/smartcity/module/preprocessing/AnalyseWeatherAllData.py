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
    global data
    print(data)
    if data is None:
        data = db.weather.find({"location":location}).sort("_id", -1)
        #json_str =json_util.dumps(data)
        #data =json_util.loads(json_str)
        
    dates = []
    dailyrainMM = []
    windSpeedGustKMH = []
    Humidity = []
    HourlyPrecipMM = []
    TemperatureC = []
    
    for res in (data):
        for res2 in (res['item']):
            dailyrainMM.append(float(res2["dailyrainMM"]))
            windSpeedGustKMH.append(float(res2["WindSpeedGustKMH"]))
            Humidity.append(float(res2["Humidity"]))
            HourlyPrecipMM.append(float(res2["HourlyPrecipMM"]))
            TemperatureC.append(float(res2["TemperatureC"]))
            dates.append(datetime.strptime(res2['Time'],'%Y-%m-%d %H:%M:%S'))
    
    dframe = df({"dailyrainMM":TimeSeries(dailyrainMM,dates), 
                "WindSpeedGustKMH":TimeSeries(windSpeedGustKMH,dates), 
                "Humidity":TimeSeries(Humidity,dates), 
                "HourlyPrecipMM":TimeSeries(HourlyPrecipMM,dates),
                "TemperatureC":TimeSeries(TemperatureC,dates)})
    dframe.to_csv("c:/result.csv")
    
    return dframe


def process(args):
    
    #['ICODUBLI2','ILEINSTE8','IDUBLINC2']
    
    dframe = getseriesweather("IDUBLINC2")
    pd.options.display.float_format = '{:20,.2f}'.format
    print(dframe.describe())
    print(dframe.cov())
    dframe.hist()
    #plt.hist(np.array(dframe["HourlyPrecipMM"].values), bins=[0, 1, 2, 3, 4, 5])
    plt.show()
    #dframe.plot()
    
    #plt.show()
             
    
   
if __name__ == "__main__":
    #process(sys.argv[1])
    process(sys.argv)
        
     

    