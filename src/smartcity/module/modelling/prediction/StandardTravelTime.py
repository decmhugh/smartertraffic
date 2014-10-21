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
from smartcity.module.utils import junctionhelper as jh

class Spatial:
    
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Spatial, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

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
    def addrow(self, df, row):
        return df.append(pd.DataFrame(row), ignore_index=True)
    
    def process_lock(self, args,junction):
        
        self.table
        self.spatialstore
        self.n_data
        name = args.replace("/","_")
        neighbours = self.get_neighbour(junction['_id'])
        neighbours = [n for n in neighbours.index[neighbours.values == 1]]
      
        def data_result(args):
            data = df().from_csv(dir + "data.csv")
            result = self.db.peak_weekday.find({"_id":args}).sort("_id", -1) 
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
        if not args in self.n_data.keys():
            self.n_data[args] = data_result(args)
        stt = self.n_data[args] 
        ts1 = pd.Series(stt["STT"].values.squeeze())
        for n in neighbours:
            if not n in self.n_data.keys():
                self.n_data[n] = data_result(n)
        
        #print(neighbours)
        def implace(n):
            missing = np.mean(n)
            return n.shift(1).fillna(missing).values.squeeze()
        
    
        inout = [np.corrcoef(ts1.values,implace(self.n_data[n]))[0,1] 
                            for n in neighbours]
        
        res = dict(zip(neighbours,inout))
        max_res = max(res)
    
        neighsame = [n for n in neighbours if n.split("/")[2] is args.split("/")[2]]
        samedir = [np.corrcoef(ts1.values,implace(self.n_data[n]))[0,1] 
                            for n in neighsame]
        neighopp = [n for n in neighbours if not n.split("/")[2] is args.split("/")[2]]
        oppdir = [np.corrcoef(ts1.values,implace(self.n_data[n]))[0,1] 
                            for n in neighopp]
        self.spatialstore[args] = {"inout-1": np.mean(inout),"max-1":res[max_res],
                              "samedir-1":np.mean(samedir),"oppdir-1":np.mean(oppdir),
                              "itself-1":np.mean(oppdir)}
        
        
                   
        
    def process(self,args,junction):
        pickle_dir = "pickle/" + args.replace("/","_")
        print(pickle_dir)
        result = None
        if not os.path.isdir(pickle_dir):
            os.makedirs(pickle_dir)
        a = datetime.now().strftime('%Y%m%d%H%M%S')
        
        self.process_lock(args,junction);
    
            
        b = datetime.now().strftime('%Y%m%d%H%M%S')
        with open("pickle/" + args.replace("/","_") + "/timestamp.txt", "w") as target:
            target.write("start:" + a)
            target.write("end:" + b)
            target.close()
        return result;  
    
    def run(self):
        cursor = self.db.junctions.find()
        json_str =json_util.dumps(cursor)
        junctions =json_util.loads(json_str)
        #os.remove(r'weather_correlation_lagged.csv')
        junctions = sorted(junctions, key=lambda k: k['route']) 
        for junction in junctions[:2]:
            self.process(junction["_id"],junction)
        data = [self.spatialstore[y] for y in self.spatialstore]
        def quote(s):
            return "\"" + s  + "\""
        idx = [quote(i) for i in self.spatialstore.keys()]
        d = df(data, index=idx)
        d.dropna().to_csv("spatial_features.csv")  
        
    
    matrix = ""
    
    def get_neighbour(self,id):
        if self.matrix is "":
            cursor = self.db.junctions.find()
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
    Spatial().run()
    
    #jh.neightbours(junctions);
    #run()
    
        
     

    