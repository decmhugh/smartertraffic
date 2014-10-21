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

def getstt(item):  
    time=[]   
    for i in item:
        time.append(i["stt"]) 
    return time    

def getseriesweather(attr,bool,location):
    result = mem.get(location)
    
    if result == None:
        result = db.weather.find({"location":location}).sort("_id", -1)
    else:
        print("cached weather")
    
    weather = []
    dates = []

    for res in (result):
        for res2 in (res['item']):
            if set((attr,'Time')).issubset(res2.keys()):
                weather.append(float(res2[attr]))
                dates.append(datetime.strptime(res2['Time'],'%Y-%m-%d %H:%M:%S'))
    ts = TimeSeries(weather,dates)  
    result = ts.resample('10min', how=bool,convention='end',fill_method="pad")
    return result

def getseries(q):
    pkl = "observation_" + q["route"] + "_" + q["link"] + "_" + q["direction"]
    
    ts = mem.get(pkl)
    # existising query stored
    if ts:
        print("cached trips")
    else:
        result = db.observation.find(q).sort("_id", -1)
        
        data = []
        dates = []
        for res in result:
            d = res["item"]
            for res2 in d:
                data.append(res2["stt"])
                dates.append(res2['date'])
        ts = TimeSeries(data,dates)   
    #put_pickle(pkl, ts)
    
    
    result = ts
    return result

def process_lock(args):
    cursor = db.junctions.find({"_id":args})
    
    rain = getseriesweather('dailyrainMM',"mean","IDUBLINC2")
    wind = getseriesweather('WindSpeedGustKMH',"mean","IDUBLINC2")
    temperature = getseriesweather('TemperatureC',"mean","IDUBLINC2")
    #json_str =json_util.dumps(cursor)
    #junctions =json_util.loads(json_str)
    #neighbours1 = list(db.junctions.find({"junction2.point":junctions[0]["junction1"]["point"]}))
    #neighbours2 = list(db.junctions.find({"junction1.point":junctions[0]["junction2"]["point"]}))
    series = []
    neighbours = []
    #neighbours.extend(neighbours1)
    #neighbours.extend(neighbours2)
    #print("1",neighbours1)
    #print("2",neighbours2)    
    

    arg = args.split("/")
    series1 = {"route":arg[0],"link":arg[1],"direction":arg[2]}
    selected_series = getseries(series1)
    #for n in neighbours:
        #if not n["direction"] == series1["direction"]:
            #if not (n["route"] + "/" + n["link"]) == (series1["route"] + "/" + series1["link"]):
                #series.append(getseries({"route": n["route"],"link": n["link"],"direction": n["direction"]}))

    
    shift = 10*6*24

    ds = {"STT":selected_series}
    
    dframe = df(ds)
             
    
def process(args):
    pickle_dir = "pickle/" + args.replace("/","_")
    print(pickle_dir)
    result = None
    if not os.path.isdir(pickle_dir):
        os.makedirs(pickle_dir)
    a = datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        
        process_lock(args);
    except ValueError as error:
        print(error)
    b = datetime.now().strftime('%Y%m%d%H%M%S')
    with open("pickle/" + args.replace("/","_") + "/timestamp.txt", "w") as target:
        target.write("start:" + a)
        target.write("end:" + b)
        target.close()
    return result;  

def run():
    pd.options.display.float_format = '${:,.2f}'.format
    cursor = db.junctions.find()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in junctions:
        process(junction["_id"])
   
if __name__ == "__main__":
    #process(sys.argv[1])
    run()
        
     

    