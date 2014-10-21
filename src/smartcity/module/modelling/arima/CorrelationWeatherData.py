'''
Created on 3 Dec 2013

@author: declan
'''
from datetime import datetime, date
import os, gc, sys, geopy,csv

from bson import json_util
from pandas import DataFrame as df
from pymongo import Connection as mongoConn
import numpy as np
import pandas as pd
from smartcity.module.utils import WeatherData as wd
from smartcity.module.utils import junctionhelper as jh



connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
col = ["Weather -" + str(a) for a in range(1,16)]
table = []
links = []
weatherstore = []
records = []
nearest = []
middle = []
furthest = []
columns = None
def addrow(df, row):
    return df.append(pd.DataFrame(row), ignore_index=True)

def process_lock(args,junction):
    global table
    name = args.replace("/","_")
    dir = "pickle/" + name +  "/"
    path = "C:/Users/IBM_ADMIN/Documents/Disseration/Figures/"
    data = df().from_csv(dir + "data.csv")
    
    result = db.peak_weekday.find({"_id":args}).sort("_id", -1) 
    hour = [0,0]
    
    global weatherstore
    loc = df()
    data["IDUBLINC2_dailyrainMM"] = weatherstore["IDUBLINC2"]["dailyrainMM"]
    data["IDUBLINC2_TemperatureC"] = weatherstore["IDUBLINC2"]["TemperatureC"]
    point = wd.stations_coordinates("IDUBLINC2")
    loc["IDUBLINC2_distance"] = jh.distance_between_junction(junction, point)
    data["ILEINSTE8_dailyrainMM"] = weatherstore["ILEINSTE8"]["dailyrainMM"]
    data["ILEINSTE8_TemperatureC"] = weatherstore["ILEINSTE8"]["TemperatureC"]
    point = wd.stations_coordinates("ILEINSTE8")
    loc["ILEINSTE8_distance"] = jh.distance_between_junction(junction, point)
    data["ICODUBLI2_dailyrainMM"] = weatherstore["ICODUBLI2"]["dailyrainMM"]
    data["ICODUBLI2_TemperatureC"] = weatherstore["ICODUBLI2"]["TemperatureC"]
    point = wd.stations_coordinates("ICODUBLI2")
    loc["ICODUBLI2_distance"] = jh.distance_between_junction(junction, point)
    
    
    data = data.dropna()
    for res in result:
        h = res["item"][0]["hour"]
        hour[0] = str(h) + ":00"
        hour[1] = str((h)) + ":59"
        
    try:
        data = data.between_time(hour[0],hour[1]).resample('B').dropna()
    except Exception: 
        data = data.resample('B').dropna()
    
    ts1 = pd.Series(data["STT"].values.squeeze())
    ts_rain = {}
    #ts_temp = {}
    ts_rain["IDUBLINC2_dailyrainMM"] = pd.Series(data["IDUBLINC2_dailyrainMM"].values.squeeze())
    ts_rain["IDUBLINC2_TemperatureC"] = pd.Series(data["IDUBLINC2_TemperatureC"].values.squeeze())
    ts_rain["ILEINSTE8_dailyrainMM"] = pd.Series(data["ILEINSTE8_dailyrainMM"].values.squeeze())
    ts_rain["ILEINSTE8_TemperatureC"] = pd.Series(data["ILEINSTE8_TemperatureC"].values.squeeze())
    ts_rain["ICODUBLI2_dailyrainMM"] = pd.Series(data["ICODUBLI2_dailyrainMM"].values.squeeze())
    ts_rain["ICODUBLI2_TemperatureC"] = pd.Series(data["ICODUBLI2_TemperatureC"].values.squeeze())
    global columns
    #result = autocorrelation_plot(ts1)
    row = [np.corrcoef(ts1.values,ts_rain[a].values)[0,1] 
                        for a in ts_rain.keys()]
    table.append(row);
    columns=ts_rain.keys()
    records.append(args.replace("/","_")) 
    #loc.append(args)    
    
    #print(table)    
    
    #print("-----------SCORE-----------------------------")
    #print(args,">>>")
    #print(hour,">>>")
    #result = sm.ols(formula="STT ~ Lag_1 + Lag_2 + Lag_3 + Lag_4 + Lag_5 + Lag_6", data=d).fit()
    #print(result.summary())
    
    
             
    
def process(args,junction):
    pickle_dir = "pickle/" + args.replace("/","_")
    print(pickle_dir)
    result = None
    if not os.path.isdir(pickle_dir):
        os.makedirs(pickle_dir)
    a = datetime.now().strftime('%Y%m%d%H%M%S')
    
    process_lock(args,junction);

        
    b = datetime.now().strftime('%Y%m%d%H%M%S')
    with open("pickle/" + args.replace("/","_") + "/timestamp.txt", "w") as target:
        target.write("start:" + a)
        target.write("end:" + b)
        target.close()
    return result;  

def run():
    global weatherstore
    weatherstore = wd.getseriesweather()
    global table
    np.set_printoptions(precision=2,suppress=True)
    cursor = db.junctions.find()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    #os.remove(r'weather_correlation_lagged.csv')
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in junctions:
        process(junction["_id"],junction)
    data = df(table,columns=columns)
    data["_index"] = records
    
    print(df.dtypes)
    data.reindex_axis(sorted(data.columns), axis=1)
    data.dropna().to_csv("weather_correlation_lagged.csv")          

if __name__ == "__main__":
    run()
    
        
     

    