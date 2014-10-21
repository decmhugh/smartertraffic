'''
Created on 3 Dec 2013

@author: declan
'''
from pymongo import Connection as mongoConn

import json,pickle
from bson import json_util
from smartcity.module.Singleton import Singleton


rain = None
wind = None
temperature = None

connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic

def parse(x):
    return str(round(x))

def convert(d):
    q = [parse(x) for x in d["obs_quantile"]]
    return {"_id":d["_id"]
              ,"obs_count":parse(d["obs_count"])
              ,"obs_std":parse(d["obs_std"])
              ,"obs_min":parse(d["obs_min"])
              ,"obs_max":parse(d["obs_max"])
              ,"obs_quantile":q}
    
def convert_day(d):
    q = [parse(x) for x in d["obs_quantile"]]
    return {"_id":d["_id"]
              ,"obs_count":parse(d["obs_count"])
              ,"obs_std":parse(d["obs_std"])
              ,"obs_min":parse(d["obs_min"])
              ,"obs_max":parse(d["obs_max"])
              ,"obs_quantile":q}

def dist_simple():
    cursor = db.obs_stats.find()
    json_str =json_util.dumps(cursor)
    return json_util.loads(json_str)

def dist():
    res = Singleton()._instance.cache.get("describe_dist",None)
    if res == None:
        cursor = db.obs_stats.find()
        json_str =json_util.dumps(cursor)
        dist = sorted(json_util.loads(json_str), key=lambda k: k['_id']) 
        res = []
        for d in dist:
            res.append(convert(d))
            
        Singleton()._instance.cache["describe_dist"] = res
    return res

def weekday():
    res = Singleton()._instance.cache.get("describe_dist_wd",None)
    if res == None:
        cursor = db.peak_weekday.find()
        json_str =json_util.dumps(cursor)
        dist = sorted(json_util.loads(json_str), key=lambda k: k['_id']) 
        res = []
        for d in dist:
            res.append(convert_day(d))
            
        Singleton()._instance.cache["describe_dist_wd"] = res
    return res

def weekend():
    res = Singleton()._instance.cache.get("describe_dist_we",None)
    if res == None:
        cursor = db.peak_weekday.find()
        json_str =json_util.dumps(cursor)
        dist = sorted(json_util.loads(json_str), key=lambda k: k['_id']) 
        res = []
        for d in dist:
            res.append(convert_day(d))
            
        Singleton()._instance.cache["describe_dist_we"] = res
    return res
    
        
   
if __name__ == "__main__":
    #process(sys.argv[1])
    #print(dist())
    distribution = dist()
    dist = sorted(distribution, key=lambda k: k['_id']) 
    print(r"\emph{id}"," & ",r"\emph{count}",r"\emph{std}"," & ","\emph{min}"
          ,"\emph{max}"," & ","\emph{.20}"," & ","\emph{.40}",
          " & ","\emph{.60}"," & ","\emph{.80}" , r"\\ \hline")
    
    for d in dist:
        print(d["_id"]," & "
              ,d["obs_count"]," & "
              ,d["obs_std"]," & "
              ,d["obs_min"]," & "
              ,d["obs_max"]," & "
              ,d["obs_quantile"][20]," & "
              ,d["obs_quantile"][40]," & "
              ,d["obs_quantile"][60]," & "
              ,d["obs_quantile"][80],r" \\ \hline ")
        
        
   
if __name__ == "__main2__":
    #process(sys.argv[1])
    #print(dist())
    distribution = dist_simple()
    dist = sorted(distribution, key=lambda k: k['_id']) 
    #print(r"\emph{id}"," & ",r"\emph{count}",r"\emph{std}"," & ","\emph{min}"
    #      ,"\emph{max}"," & ","\emph{.20}"," & ","\emph{.40}",
    #      " & ","\emph{.60}"," & ","\emph{.80}" , r"\\ \hline")
    for d in dist:
        print(d["_id"]," & "
              ,str(round(d["obs_count"]))," & "
              ,str(round(d["obs_std"]))," & "
              ,str(round(d["obs_min"]))," & "
              ,str(round(d["obs_max"]))," & "
              ,str(round(d["obs_quantile"][20]))," & "
              ,str(round(d["obs_quantile"][40]))," & "
              ,str(round(d["obs_quantile"][60]))," & "
              ,str(round(d["obs_quantile"][80])),r" \\  ")
        
        
    
    
        
     

    