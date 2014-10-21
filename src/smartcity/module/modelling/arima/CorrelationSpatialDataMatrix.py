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
import pprint



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
    cursor = db.junctions.find()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    #os.remove(r'weather_correlation_lagged.csv')
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in junctions[:4]:
        process(junction["_id"],junction)
    data = df(table,columns=columns)
    data["_index"] = records
    
    data.dropna().to_csv("spatial_correlation_lagged.csv")   

matrix = ""

def get_neighbour(id):
    global matrix
    if matrix is "":
        cursor = db.junctions.find()
        json_str =json_util.dumps(cursor)
        junctions =json_util.loads(json_str)
        junctions = sorted(junctions, key=lambda k: k['route']) 
        matrix = []
        i = 6
        #df = DataFrame(, index=dates, columns=['A', 'B', 'C', 'D'])
        headers = [y['_id'] for y in junctions]
        for x in junctions:
            matrix.append([int(jh.is_neighbour(x, y)) for y in junctions])
        matrix = df(matrix,columns=headers,index=headers) 
    return matrix[id]      

if __name__ == "__main__":
    cursor = db.junctions.find()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    matrix = []
    def quote(s):
        return "\"" + s  + "\""
    i = 6
    #df = DataFrame(, index=dates, columns=['A', 'B', 'C', 'D'])
    headers = [quote(y['_id'])  for y in junctions]
    for x in junctions:
        matrix.append([int(jh.is_neighbour(x, y)) for y in junctions])
    d = df(matrix,columns=headers,index=headers,)
    
    #pp = pprint.PrettyPrinter(indent=4)
    d.to_csv("neighbours_all9.csv")
    
    #jh.neightbours(junctions);
    #run()
    
        
     

    