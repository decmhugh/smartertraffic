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
collection = db.observation 

def main(argv):
    argv.timeframe = AttrDict()
    argv.mapset = {}
    if len(Junction.items.values()) == 0:
        csvreadjunctions(argv)
    if False:
        for value in Junction.items.values() :
            print(value)
    if True:
        csvreaddata(argv)
        for key,tf in argv.timeframe.iteritems():
            dir = "observation/" + key[:8]
            try: 
                os.makedirs(dir)
            except (OSError):
                if not os.path.isdir(dir):
                    print("no dir")
            with open(dir + '/' + key +".csv", 'wb') as fp:
                a = csv.writer(fp, delimiter=',')
                data = [['id','date', 'route','link', 'direction','stt', 
                                'tcs1', 'X_tcs1','Y_tcs1',  
                                'tcs2', 'X_tcs2','Y_tcs2', 
                                'line', 'speed', 'distance']
                                ]
                a.writerows(data)
                distance.VincentyDistance.ELLIPSOID = 'WGS-84'
                for i,value in enumerate(tf) :
                    
                    # All observations with date and time of matching 
                    if isValidObserbvation(value):
                        #if (value['date'].find(date + '-083') > -1 or value['date'].find(date + '-084') > -1) and (value['direction'] == '1'):
                        
                        try:
                            v1 = value['junction1']
                            v2 = value['junction2']
                            stt = float(value['stt'])
                            d = distance.distance
                            
                            key = value['tcs2'] + "." + value['direction'] + "." + value['date']
                            
                            line_wkt =  "LINESTRING(" + re.sub(',',' ',v1['point'])
                            line_wkt += "," +  re.sub(',',' ',v2['point']) +  ")"
                            
                            line =  "LINESTRING(" + str(v1['lon']) + " " +  str(v1['lat'])
                            line += "," +  str(v2['lon']) + " " + str(v2['lat']) +  ")"
                        
                            dist = lsc.distance_of_line(line_wkt)
                            data = [[value['id'],value['date'], value['route'], 
                                    value['link'], value['direction'], stt, 
                                    value['tcs1'], 
                                    v1['lon'],
                                    v1['lat'], 
                                    value['tcs2'], 
                                    v2['lon'],
                                    v2['lat'],
                                    line,
                                    dist,
                                    dist/stt]                             
                                    ]
                            a.writerows(data)
                        except IOError as errno:
                            print(errno)
                        except ValueError:
                            print("Could not convert data to an integer.")
                        
            del a                        #raise
    del argv
                    
    return
listInvalid = {'1','22'} 
def isValidObserbvation(value):
    if (value["route"] in listInvalid):
        return False
    return True
def formatdate(date_string):
    # expect string date format is "%Y%m%d-%H%M"
    result = ""
    try :
        print(date_string) 
        result = datetime.strptime(date_string, "%Y%m%d-%H%M")
        print("result")
        print(result)
    except (RuntimeError, TypeError, NameError, ValueError) as error:
        print("Error format date:")
        print(date_string)
        print(error)
    return result


def csvreaddata(argv):
    #print argv.filename
    datefromfile = r"observation/" + argv.filename[4:12]
    print(datefromfile)
    result = os.path.isdir(datefromfile)
    if result is False:
        with open("extracted/" + argv.filename) as csvfile:
            print("getting extracted/" + argv.filename)
            csvreader = csv.reader(csvfile, delimiter=',' )
            for i, row in enumerate(csvreader):
                if len(row) > 7:
                    
                    try :
                        #if row[1].strip() == '9':
                        mydate = formatdate(row[0].strip())
                        #mydate2 = todate(row[0].strip())
                        timeid = mydate.strftime('%Y%m%d')
                        
                        obs = {'date': mydate.strftime('%Y%m%d%H%M%S'), 'route': row[1].strip(), 'link': row[2].strip(),'direction':row[3].strip(),
                               'stt':float(row[4].strip()),'accstt':row[5].strip(),'tcs1':row[6].strip(),'tcs2':row[7].strip()}
                        obs['junction1'] = j.find(row[6])
                        obs['junction2'] = j.find(row[7])
                        if (obs['junction1'] and obs['junction2']):
                            obs['id'] = makeId(obs)
                            keys = argv.timeframe.keys()
                            if not timeid in keys:
                                argv.timeframe[timeid] = []
                            argv.timeframe[timeid].append(obs)
                            collection.insert(obs)  
                    except (RuntimeError, TypeError, NameError, ValueError) as error:
                        print("ERROR:")
                        print(row)
                        print(error)



def csvreadjunctions(argv):
    parser = ElementTree.XMLParser()
    tree = ElementTree.parse("junctions.kml",parser)
    sites = tree.iterfind(".//*[@name=\"SiteID\"]")
    x = tree.iterfind(".//*[@name=\"X\"]")
    y = tree.iterfind(".//*[@name=\"Y\"]")
    points = tree.findall('.//{http://www.opengis.net/kml/2.2}coordinates')
    my={}
    loc={}
    
    p = points
    s = sites
    for i,x in enumerate(s):
        my[i] = x.text
    
    for i,p in enumerate(points):
        loc[my[i]] = p.text
        
    with open(argv.filepath + "junctions.csv") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for y,row in enumerate(csvreader):
            if (y > 0):
                if (validatecsvjunctions(row)):
                    id = row[0].strip()
                    jun = {'point':loc[id],'id': id, 'lon': row[1].strip(), 'lat': row[2].strip(),'desc':row[3].strip()}
                    j.add(jun);

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


            

def makeId(item):
        return item["route"] + "/" + item["link"]  + "/" + item["direction"] + "/" + item["date"]
    
def validatecsvjunctions(argv):
    result = True;
    for w in argv:
        if (len(w) == 0):
            result = False  
    if (not (argv[0].isdigit())):
        result = False
    if (not (argv[1].isdigit())):
        result = False
    if (not (argv[2].isdigit())):
        result = False
        
    return result

j = Junction()
filename = "day-20140102.csv.bz2.csv"
filepath = ""
date = ''
if __name__ == "__main__":
    date = filename[4:12]
    argv = attrdict.AttrDict()
    argv.filename = filename
    argv.filepath = filepath
    argv.date = date
    
    main(argv)