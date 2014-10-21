'''
Created on 3 Dec 2013

@author: declan
'''
from datetime import datetime, date
import os, gc, sys

from bson import json_util
from pandas import DataFrame as df
from pandas.core.series import TimeSeries
from pandas.stats.moments import ewma
from pymongo import Connection as mongoConn
from scipy import stats
from sklearn import cross_validation
from sklearn import linear_model
from sklearn import linear_model
from sklearn import svm
from sklearn.linear_model import RandomizedLogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from statsmodels.graphics.api import qqplot
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.graphics.tsaplots import plot_pacf

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from smartcity.module.utils import WeatherData as wd


class PredictionResultTraffic(object):
    
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            print("Init PredictionResultTraffic")
            cls._instance = super(PredictionResultTraffic, cls).__new__(
                                cls, *args, **kwargs)
        else:
            print("Already loaded PredictionResultTraffic")
        
        return cls._instance

            
    connection = mongoConn('mongodb://localhost:27017/')
    db = connection.traffic
    
    def result(self,args):
        print("result start")
        result = self.db.prediction_results.find({"_id":args});
        json_str =json_util.dumps(result)
        obj = json_util.loads(json_str)   
        return obj 
   
if __name__ == "__main__":
    res = PredictionResultTraffic().result("1/13/2");
    res = PredictionResultTraffic().result("1/13/2");
    print(res)
        
     

    