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
from sklearn.externals import joblib
import pandas as pd

rain = None
wind = None
temperature = None

connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic



def run():
    cursor = db.junctions.find()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    route = [int(j["route"]) for j in junctions]
    link = [int(j["link"]) for j in junctions]
    direction = [int(j["direction"]) for j in junctions]
    d = df({"route":route,
            "link":link,
            "direction":direction})
    print(d.describe())
   
if __name__ == "__main__":
    #process(sys.argv[1])
    pd.options.display.float_format = '{:20.2f}'.format
    run()
        
     

    