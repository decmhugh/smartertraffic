'''
Created on 20 Jul 2014

@author: declan
'''
from pymongo import Connection as mongoConn
import geopy
import numpy as np
from bson import json_util
from geopy import distance
from smartcity.module.utils import WeatherData as wd
connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic

def junction_center(junction):
    j1 = junction['junction1']['point'].split(',')
    j2 = junction['junction2']['point'].split(',')
    loc1 = geopy.Point(j1)
    loc2 = geopy.Point(j2)
    long = (loc1[0] + loc2[0])/2
    lat = (loc1[1] + loc2[1])/2
    result = geopy.Point(long,lat)
    return result;

def point_from_junction(j):
    arr = j['point'].split(',')
    loc = geopy.Point(arr[1],arr[0])
    return loc

def neightbours(junctions):
    for i,j in enumerate(junctions):
        junctions[i]['junction1']['coord'] = point_from_junction(junctions[i]['junction1'])
        junctions[i]['junction2']['coord'] = point_from_junction(junctions[i]['junction2'])

def is_neighbour(junction,otherJunction):
    if junction['_id'] is otherJunction['_id']:
        return False
    junction['junction1']['coord'] = point_from_junction(junction['junction1'])
    junction['junction2']['coord'] = point_from_junction(junction['junction2'])
    otherJunction['junction1']['coord'] = point_from_junction(otherJunction['junction1'])
    otherJunction['junction2']['coord'] = point_from_junction(otherJunction['junction2'])
    if otherJunction['junction1']['coord'] == junction['junction1']['coord']:
        return True
    if otherJunction['junction1']['coord'] == junction['junction2']['coord']:
        return True
    if otherJunction['junction2']['coord'] == junction['junction1']['coord']:
        return True
    if otherJunction['junction2']['coord'] == junction['junction2']['coord']:
        return True
    return False;
    

def distance_between_junction(junction,point):
    print(junction,point)
    _to = geopy.Point(point[1],point[0])
    _from = junction_center(junction)
    return geopy.distance.VincentyDistance(_from,_to)

def junctions():
    global table
    np.set_printoptions(precision=2,suppress=True)
    cursor = db.junctions.find()
    junctions = convert(cursor)
    return junctions
    
def junctions_one(arg):
    global table
    np.set_printoptions(precision=2,suppress=True)
    cursor = db.junctions.find({"_id":arg})
    junctions = convert(cursor)[0]
    return junctions

def convert(cursor):
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    return sorted(junctions, key=lambda k: k['route']) 

def pretty(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]

if __name__ == '__main__':
    a = junctions_one("9/7/1")
    b = junctions_one("9/7/1")
    print(is_neighbour(a,b))
    #print(a)
    #print(junction_center(a))
    #print(wd.coordinates())
    #point = wd.coordinates()[0]
    #print(list(point))
    #distance = distance_between_junction(a,point)
    #print(distance)
    