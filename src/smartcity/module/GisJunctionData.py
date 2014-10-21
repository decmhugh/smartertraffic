'''
Created on 3 Dec 2013

@author: declan
'''

import csv
import os
import re
from time import *
from xml import etree
from xml.etree import ElementTree
import pymongo
from datetime import datetime

from attrdict import AttrDict
import attrdict
from geopy import distance
from shapely.wkt import loads

import smartcity.module.LineStringConvertor as lsc
from pymongo import Connection as mongoConn

connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
collection = db.junctions 

def main(argv):
    csvreadjunctions(argv)
    return
_routes={}
_juncs={}

def csvreadroutes(argv):
    parser = ElementTree.XMLParser()
    tree = ElementTree.parse("routes.kml",parser)
    
    routes = tree.findall(".//{http://www.opengis.net/kml/2.2}Placemark")
    my={}
    
    
    #p = points
    #s = sites
    for i,x in enumerate(routes):
        route = (routes[i].findtext(".//*[@name=\"Route\"]"))
        link = (routes[i].findtext(".//*[@name=\"Link\"]"))
        direction = (routes[i].findtext(".//*[@name=\"Direction\"]"))
        tcs1 = (routes[i].findtext(".//*[@name=\"TCS1\"]"))
        tcs2 = (routes[i].findtext(".//*[@name=\"TCS2\"]"))
        co = (routes[i].findtext(".//{http://www.opengis.net/kml/2.2}coordinates"))
        routeObj = {"_id": route + "/" + link + "/" + direction,'route':route,'link': link, 'direction': direction, 'tcs1': tcs1,'tcs2':tcs2}
        _routes[route + "/" + link + "/" + direction] = routeObj
    

def csvreadjunctions(argv):
    csvreadroutes(argv)
    parser = ElementTree.XMLParser()
    tree = ElementTree.parse("junctions.kml",parser)
    
    junctions = tree.findall(".//{http://www.opengis.net/kml/2.2}Placemark")
    #print(junctions)
    #sites = tree.iterfind(".//*[@name=\"SiteID\"]")
    #x = tree.iterfind(".//*[@name=\"X\"]")
    #y = tree.iterfind(".//*[@name=\"Y\"]")
    #points = tree.findall('.//{http://www.opengis.net/kml/2.2}coordinates')
    my={}
    loc={}
    
    #p = points
    #s = sites
    for i,x in enumerate(junctions):
        site = (junctions[i].findtext(".//*[@name=\"SiteID\"]"))
        lon = (junctions[i].findtext(".//*[@name=\"X\"]"))
        lat = (junctions[i].findtext(".//*[@name=\"Y\"]"))
        loc = (junctions[i].findtext(".//*[@name=\"Location\"]"))
        co = (junctions[i].findtext(".//{http://www.opengis.net/kml/2.2}coordinates"))
        _juncs[site] = {'point':co,'id': site, 'lon': lon, 'lat': lat,'desc':loc}
        c = collection.find();
        
    for r in _routes:
        route = _routes[r]
        print(route)
        print(_juncs[route['tcs1']])
        route["junction1"] = _juncs[route['tcs1']]
        route["junction2"] = _juncs[route['tcs2']]
        collection.insert(route);
    
    #for i,p in enumerate(points):
    #    loc[my[i]] = p.text
        

    #for y,row in enumerate(csvreader):
    #   if (y > 0):
    #            id = row[0].strip()
    #            jun = {'point':loc[id],'id': id, 'lon': row[1].strip(), 'lat': row[2].strip(),'desc':row[3].strip()}
    #            j.add(jun);

class Junction:
    items = dict()
    
    def __init__(self, *entries):
        self.__dict__.update(entries)
        
    def add(self, item):
        self.items[item['id']] = item
    
    def find(self,genid):
        if (self.items.get(genid)):
            return self.items[genid]
        return ''




if __name__ == "__main__":
    argv = attrdict.AttrDict()
    main(argv)