'''
Created on 3 Dec 2013

@author: declan
'''

from pymongo import Connection as mongoConn
from bson.json_util import dumps
import json
from smartcity.module.utils import junctionhelper as jh

connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
collection = db.junctions 


def result_all(arg):
    result = collection.find(arg)
    #result = dict([r for r in result])
    return result

def json_str(arg):
    return dumps(result_all(arg))

def json_all(arg):
    return json.loads(json_str())

def json_pretty():
    return json.dumps(json_all(), sort_keys=True, indent=4)
    #return json_all()

def json_pointdata():
    for r in result_all():
        print(r['junction1'])
        
def json_geodata():
    juncs = {}
    for r in result_all():
        if juncs[r['junction1']['id']] in juncs.keys():
            print()
        print(r['junction1'])
        
        
    
if __name__ == "__main__":
    print(json_str({"direction":'1'}))