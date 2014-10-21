'''
Created on 3 Dec 2013

@author: declan
'''
from pymongo import Connection as mongoConn

import os
import pickle
import json


    
def process(args):
    path = os.path.dirname(os.path.realpath(__file__))
    pickle_dir = "/pickle/" + args.replace("/","_");
    dir = path + pickle_dir
    print(os.path.exists(dir + "/result.res"));
    data = pickle.load(open(dir + "/result.res","rb"));  
    print(data);
    return data;

def data(args):
    result = process(args);
    li = []
    for i,r in enumerate(result["results"]):
        r["coef"] = r["coef"].tolist()
        li.append( r)
    
    result["results"] = li
    return json.dumps(result, sort_keys=True, indent=4) 
    #return result;
        
   
if __name__ == "__main__":
    result = process("9/7/1");
    li = []
    for i,r in enumerate(result["results"]):
        
        r["coef"] = r["coef"].tolist()
        print(r);
        li.append(r)
    
    result["results"] = li
    print(json.dumps(result, sort_keys=True, indent=4))
    

    