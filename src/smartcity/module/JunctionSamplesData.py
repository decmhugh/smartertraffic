'''
Created on 3 Dec 2013

@author: declan
'''
from pymongo import Connection as mongoConn
from pandas import Series
import numpy as np
import pandas as pd
import random
import vincent
#Create a date range and populate it with some random data
dates = pd.date_range('4/1/2013 00:00:00', periods=1441, freq='T')
data = [random.randint(20, 100) for x in range(len(dates))]
series = pd.Series([1,2,3], index=[3,2,1])
series.plot()



connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
collection = db.observation
collectionj = db.junctions

def getstt(item):  
    time=[]   
    for i in item:
        time.append(i["stt"]) 
    return time
        
def getseries():
    result = db.observation.find({"route":"9","link":"1","direction":"1","hour":"09"})
    #series = Series(result, index=[])
    data = {}
    for res in reversed(list(result)):
        d = getstt(res["item"])
        data[res["day"]] = np.average(d)
        print(res["day"],np.average(d))
    return Series(data)

def getseries2():
    result = db.observation.find({"route":"1","link":"9","direction":"1","day":"20140114"})
    #series = Series(result, index=[])
    data = {}
    for res in result:
        d = getstt(res["item"])
        data[res["day"]] = np.average(d)
        #print(res["day"],d,res["hour"])
    return Series(data)

    
    
 

if __name__ == "__main__":
    series = getseries2()
    #print(series)

    