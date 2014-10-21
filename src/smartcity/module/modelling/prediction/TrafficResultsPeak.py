'''
Created on 3 Dec 2013

@author: declan
'''
from datetime import datetime, date
import os, gc, sys
import operator
from bson import json_util
from pandas import DataFrame as df
from pymongo import Connection as mongoConn
import json,pprint


class TrafficResults(object):
    
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            print("Init PredictionResultTraffic")
            cls._instance = super(TrafficResults, cls).__new__(
                                cls, *args, **kwargs)
        else:
            #print("Already loaded PredictionResultTraffic")
            pass
        
        return cls._instance

            
    connection = mongoConn('mongodb://localhost:27017/')
    db = connection.traffic
    
    def result(self,args):
        print("result start")
        result = self.db.prediction_results.find({"_id":args});
        json_str =json_util.dumps(result)
        obj = json_util.loads(json_str)   
        return obj 
    
    def top(self,args):
        print("result start")
        result = self.db.top_predicted.find();
        json_str =json_util.dumps(result)
        obj = json_util.loads(json_str)   
        return obj 
    
    def resultall(self):
        print("result all start")
        result = self.db.prediction_results.find()
        items = []
        for r in result:
            items.append(r)
            
        return items 
    
    def resultpeakall(self):
        print("result all start")
        result = self.db.prediction_peak_results.find()
        items = []
        for r in result:
            items.append(r)
            
        return items 
    
    def highest(self,obj):
        ret = {i:float(r['scores_mse']) for i,r in enumerate(obj['scores'])}
        sorted_x = sorted({(value,key) for (key,value) in ret.items()})
        value, key = sorted_x[0]
        return obj['scores'][key]
    
    def highestall(self):
        arr=[]
        res = self.resultall()
        for result in res:
            answer = TrafficResults().highest(result)
            answer['_id'] = result['_id']
            arr.append(answer)
        
        return json.dumps(arr, separators=(',',':'))
        
    
if __name__ == "__main2__":
    print(TrafficResults().highestall())
    
            
if __name__ == "__main__":
    ##res = TrafficResults().result("1/13/2");
    ##res = TrafficResults().result("1/13/1");
    connection = mongoConn('mongodb://localhost:27017/')
    db = connection.traffic
    
    res = TrafficResults().resultpeakall()
    p = res[4]['result'][0]['predicted']
    t = res[4]['result'][0]['target']
    arr = []
    d = df()
    for result in res:
        answer = TrafficResults().highest(result)
        
        db.top_predicted_peak.remove({"_id":result["_id"]})
        answer["_id"] = str('\'') + result["_id"] + str('\'')
        db.top_predicted_peak.insert(answer)
        arr.append(answer)
    import csv
    headings2 = ['_id','i','clf','scores_mse','scores_r2','scores_evs','scores_mae','std','quantile']
    headings = ['_id','clf','scores_mse','scores_r2','scores_evs','scores_mae','std','quantile','i']
    myFilePath = 'C:/result_peak.csv'

    with open(myFilePath,'w', newline='') as myCSVFile:
        csvWriter = csv.DictWriter(myCSVFile, fieldnames=headings, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        csvWriter.writeheader()
        for data in arr:
            print(data['_id'] + ' & ' 
                   + data['clf'].split('_')[0] 
                   + ' & ' + str(data['i'])
                   + ' & ' + str(data['scores_mse']) 
                   + ' & ' + str(data['scores_r2'])
                   + ' & ' + str(data['scores_mae'])
                   + ' & ' + str(data['scores_evs'])
                   + ' & ' + str(round(data['std'],1))
                   + ' & ' + str(round(data['quantile'],1))
                   + ' \\\\  ')
            csvWriter.writerow(data)
    
    #df(answer,index=range(0,len(answer))).to_csv("C:/pickle/_results.csv")
    
        
        

            
        
     

    