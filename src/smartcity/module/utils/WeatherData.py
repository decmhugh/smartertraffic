'''
Created on 3 Dec 2013

@author: declan
'''
from pymongo import Connection as mongoConn
import os,gc,sys
import numpy as np
from datetime import datetime, date
from pandas.core.series import TimeSeries
from sklearn import cross_validation
from pandas import DataFrame as df
from sklearn import linear_model
from bson import json_util
import pandas as pd
from sklearn import svm
from scipy import stats
import statsmodels.formula.api as sm
from statsmodels.graphics.api import qqplot
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pandas.stats.moments import ewma
from sklearn import linear_model
    


connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
weatherstore = {}
def stations():
    return ["IDUBLINC2","ILEINSTE8"]#,"ICODUBLI2"
def coordinates():
    return [(53.387 ,-6.210),(53.296, -6.185),(53.343, -6.440 )]
def stations_coordinates(param):
    result = coordinates()[stations().index(param)]
    return result

def getseriesweather():
    for ws in stations():
        result = db.weather.find({"location":ws}).sort("_id", -1)
        dailyrainMM = []
        TemperatureC = []
        dates = []
        print(">>>> location >>> ",ws)
        for res in (result):
            for res2 in (res['item']):
                dailyrainMM.append(float(res2["dailyrainMM"]))
                TemperatureC.append(float(res2["TemperatureC"]))
                dates.append(datetime.strptime(res2['Time'],'%Y-%m-%d %H:%M:%S'))
        ts = TimeSeries(dailyrainMM,dates)  
        ts2 = TimeSeries(TemperatureC,dates)  
        result = ts.resample('10min', how="mean",convention='end',fill_method="pad")
        result2 = ts2.resample('10min', how="mean",convention='end',fill_method="pad")
        weatherstore[ws] = {"dailyrainMM":result,"TemperatureC":result2}
    return weatherstore
   
if __name__ == "__main__":
    #r = getseriesweather()
    #print(r)
    
    print(stations()[1])
    print(stations().index('ILEINSTE8'))
    print(coordinates()[1])
    print(stations_coordinates('ILEINSTE8'))
    
        
     

    