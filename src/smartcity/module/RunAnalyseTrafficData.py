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

from bson import json_util
from sklearn.externals import joblib
import pandas as pd





       
if __name__ == "__main__":
    #{"route":"1","link":"9","direction":"1"}
    connection = mongoConn('mongodb://localhost:27017/')
    db = connection.traffic
    pd.options.display.float_format = '{:,.3f}'.format
    cursor = db.junctions.find({"direction":"2"})
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    r = {}
    junctions = sorted(junctions, key=lambda k: k['route']) 
    path = os.path.dirname(os.path.realpath(__file__))
    for junction in junctions[20:]:
        exec("AnalyseTrafficData.py", {"id":junction["_id"]})
         
    
    #process("1/7/1")

    