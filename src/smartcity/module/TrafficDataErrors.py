'''
Created on 3 Dec 2013

@author: declan
'''
from pymongo import Connection as mongoConn

import os
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

mem = memcache.Client(["localhost:11211"])


connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic

    
def process():
    cursor = db.observation_errors.find()
    for res in (cursor):
        if (len(np.array(res["item"])) > 0):
            print(res)
            
                  
    
   
if __name__ == "__main__":

    process()

    