'''
Created on 3 Dec 2013

@author: declan
'''
from datetime import datetime, date
import os, gc, sys, pickle
from sklearn.svm import SVR
from sklearn.svm import LinearSVC
from sklearn.metrics import fbeta_score, make_scorer
from bson import json_util
from pandas import DataFrame as df
from pandas.core.series import TimeSeries
from pandas.stats.moments import ewma
from pymongo import Connection as mongoConn
from scipy import stats, spatial
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
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from smartcity.module.utils import WeatherData as wd
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
from sklearn.metrics.metrics import explained_variance_score
from smartcity.module.modelling.prediction import spatialdata,\
    ClassifyAlgorithms



connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
weatherstore = None

def data_result(args,mydatetime):
    name = args.replace("/","_")
    dir = "pickle/sample/" + name +  "/"
    path = "C:/Users/IBM_ADMIN/Documents/Disseration/Figures/"
    result = db.peak_weekday.find({"_id":args}).sort("_id", -1) 
    s = datetime.strptime(mydatetime, "%Y%m%d/%H")
    f = s.strftime('%H')
    
    hour = ['','']
    hour[0] = f + ":00"
    hour[1] = f + ":59"
    data = df().from_csv(dir + "data.csv")
    data = data.dropna()
       
    try:
        data = data.between_time(hour[0],hour[1]).resample('B').dropna()
    except Exception: 
        data = data.resample('B').dropna()
    data = data.resample('B').dropna()
    return data

def process_lock(args,junction,mydatetime):
    print("===============================")
    print(args,">>>>>>")
    name = args.replace("/","_")
    dir = "pickle\\" + name +  "\\"
    path = "C:/Users/IBM_ADMIN/Documents/Disseration/Figures/" 
    id = '\'' + args + '\''
    result = db.top_predicted.find({"_id":id})
    result =json_util.dumps(result)
    result =json_util.loads(result)[0]
    print(result)
    pname = ''.join(e for e in result['clf'] if e.isalnum() or e is "_")
    fl = dir + "" + pname + ".cls.pkl"
    print(fl)
    fo = open(fl , 'rb' )
    clf = pickle.load(fo)
    
    cursor = db.max_neighbour.find({"_id":args})
    json_str =json_util.dumps(cursor)
    neighbour_list =json_util.loads(json_str)
    neighbour = neighbour_list[0]["max"]
    n_data = data_result(neighbour,mydatetime).fillna(0)
    
    
    global weatherstore
    if weatherstore is None:
        {}
        weatherstore = wd.getseriesweather()
        
    pkl = "pickle/peak/" + args.replace("/","_") +  "/"
    data = data_result(args,mydatetime).fillna(0)
    
    data["ILEINSTE8_dailyrainMM"] = weatherstore["ILEINSTE8"]["dailyrainMM"].fillna(0)
    data["ILEINSTE8_TemperatureC"] = weatherstore["ILEINSTE8"]["TemperatureC"].fillna(0)
    data["IDUBLINC2_dailyrainMM"] = weatherstore["IDUBLINC2"]["dailyrainMM"].fillna(0)
    data["IDUBLINC2_TemperatureC"] = weatherstore["IDUBLINC2"]["TemperatureC"].fillna(0)
    
    d = df({"STT":data["STT"],
            "W_ILT":data["ILEINSTE8_TemperatureC"],
            "W_ILR":data["ILEINSTE8_dailyrainMM"],
            "W_DLR":data["IDUBLINC2_dailyrainMM"],
            "W_DLT":data["IDUBLINC2_TemperatureC"],
            "S_MAX":n_data["STT"].shift(1)}
            )
    
    d = d.resample('B').dropna()
    # Do the lagging
    d["STT1"]=d.shift(1)["STT"]
    d["STT2"]=d.shift(2)["STT"]
    d["STT3"]=d.shift(3)["STT"]
    d["STT5"]=d.shift(5)["STT"]
    s = datetime.strptime(mydatetime, "%Y%m%d/%H")
    f = s.strftime('%Y-%m-%d')
    id_str = s.strftime('%Y/%m/%d')
    stt = d[f:f]['STT']
    d = d.dropna().fillna(0).astype(np.float)
    d.__delitem__("STT")
    #print(d)
    
    result = {"_id":(s.strftime('%Y/%m/%d/%H')+ "_" + args),
              "time":(s.strftime('%Y/%m/%d/%H')),
              "junction":args,
              "result" : list(clf.predict(d[f:f]))[0],'actual':stt[0]}
    db.predict_real.remove({"_id":(id_str + "_" + args)})
    db.predict_real.insert(result)
     
    
def process(args,junction,mydatetime):
    pickle_dir = "pickle/peak/" + args.replace("/","_")
    print(pickle_dir)
    result = None
    if not os.path.isdir(pickle_dir):
        os.makedirs(pickle_dir)
    a = datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        process_lock(args,junction,mydatetime);
    except ValueError as error:
        print(error)
    b = datetime.now().strftime('%Y%m%d%H%M%S')

def run():
    mydatetime = "20140421/20"
    
    cursor = db.junctions.find()
    global weatherstore
    db.prediction_results_peak.remove()
    #weatherstore = wd.getseriesweather()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in junctions:
        try:
            process(junction["_id"],junction,mydatetime)
        except:
            pass
        
   
if __name__ == "__main__":
    run()
    #for p in ["17/6/1","13/2/1","30/7/1","10/7/2","16/2/2","30/4/2"]:
    #mydatetime = "20140418/09"
    #for p in ["1/9/1"]:
        #cursor = db.junctions.find({"_id":p})
        #db.prediction_results_peak.remove()
        #weatherstore = wd.getseriesweather()
        #json_str =json_util.dumps(cursor)
        #junctions =json_util.loads(json_str)
        #junctions = sorted(junctions, key=lambda k: k['route']) 
        #process_lock(p,junctions[0],mydatetime)
        
     

    