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
n_data = {}
spatialstore = {}
records = []
nearest = []
junc = []
furthest = []
columns = None
def addrow(df, row):
    return df.append(pd.DataFrame(row), ignore_index=True)

def process_lock(args,junction):
    
    global table
    global spatialstore
    global n_data
    name = args.replace("/","_")
    neighbours = get_neighbour(junction['_id'])
    neighbours = [n for n in neighbours.index[neighbours.values == 1]]
  
    def data_result(args):
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
        return data
    if not args in n_data.keys():
        n_data[args] = data_result(args)
    stt = n_data[args] 
    ts1 = pd.Series(stt["STT"].values.squeeze())
    for n in neighbours:
        if not n in n_data.keys():
            n_data[n] = data_result(n)
    
    #print(neighbours)
    def implace(n):
        missing = np.mean(n)
        return n.shift(1).fillna(missing).values.squeeze()
    

    inout = [np.corrcoef(ts1.values,implace(n_data[n]))[0,1] 
                        for n in neighbours]
    
    res = dict(zip(neighbours,inout))
    max_res = max(res)
    print(max_res," << max neighbour")
    db.max_neighbour.insert({"_id":args, "max":max_res})    
    
               
    
def process(args,junction):
    pickle_dir = "pickle/" + args.replace("/","_")
    print(pickle_dir)
    result = None
    if not os.path.isdir(pickle_dir):
        os.makedirs(pickle_dir)
    a = datetime.now().strftime('%Y%m%d%H%M%S')
    
    process_lock(args,junction);

def run():
    #s = {}
    #s['rr'] = {"ss":22,"a":22}
    #s['rr2'] = {"ss":22,"a":22}
    #data = [s[y] for i,y in enumerate(s)]
    
    cursor = db.junctions.find()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    #os.remove(r'weather_correlation_lagged.csv')
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in junctions:
        process(junction["_id"],junction)
    

matrix = ""

def get_neighbour(id):
    global matrix
    if matrix is "":
        cursor = db.junctions.find()
        json_str =json_util.dumps(cursor)
        junctions =json_util.loads(json_str)
        junctions = sorted(junctions, key=lambda k: k['route']) 
        matrix = []
        headers = [y['_id'] for y in junctions]
        for x in junctions:
            matrix.append([int(jh.is_neighbour(x, y)) for y in junctions])
        matrix = df(matrix,columns=headers,index=headers) 
    return matrix[id]   
 

if __name__ == "__main__":
    run()
    
    #jh.neightbours(junctions);
    #run()
    
        
     

    