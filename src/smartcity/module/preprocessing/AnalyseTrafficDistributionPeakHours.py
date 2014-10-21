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


def weekend():
    cursor = db.peak_weekday.find({"direction":"2"})
    json_str =json_util.dumps(cursor)
    dist = sorted(json_util.loads(json_str), key=lambda k: k['_id']) 
    return dist
    
        
   
if __name__ == "__main__":
    #process(sys.argv[1])
    #print(dist())
    distribution = weekend()
    dist = sorted(distribution, key=lambda k: k['_id']) 
    print(r"\emph{id}"," & ",r"\emph{hour (value)}", r"\\ \hline")
    
    for d in dist:
        q1 = "(" + str(d["item"][0]["obs_quantile"][80]) + ")"
        q2 = "(" + str(d["item"][1]["obs_quantile"][80]) + ")"
        q3 = "(" + str(d["item"][2]["obs_quantile"][80]) + ")"
        print(d["_id"]," & ", d["item"][0]["hour"], q1, 
              d["item"][1]["hour"], q2, d["item"][2]["hour"],q3, r" \\ \hline")
    
    
    
        
     

    