'''
Created on 3 Dec 2013

@author: declan
'''

import csv, os
from xml.etree import ElementTree
from datetime import datetime

from attrdict import AttrDict
import attrdict

from pymongo import Connection as mongoConn

connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
collection = db.observation
collectionj = db.junctions

def processfile(argv):
    argv.timeframe = AttrDict()
    argv.mapset = {}
    if len(Junction.items.values()) == 0:
        csvreadjunctions(argv)
    if False:
        for value in Junction.items.values() :
            print(value)
    if True:
        csvreaddata(argv)
        
                    
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
        result = datetime.strptime(date_string, "%Y%m%d-%H%M")
    except (RuntimeError, TypeError, NameError, ValueError) as error:
        print("Error format date:",date_string,error)
    return result


def csvreaddata(argv):
    #print argv.filename
    datefromfile = r"observation/" + argv.filename[4:12]
    print(datefromfile)
    result = os.path.isdir(datefromfile)
    argv.juncs={}
    if result is False:
        with open("extracted/" + argv.filename) as csvfile:
            print("getting extracted/" + argv.filename)
            csvreader = csv.reader(csvfile, delimiter=',' )
            for i,row in enumerate(csvreader):
                # Validate row, a row must contain 8 values
                if len(row) > 7:
                    try :
                        dateOfObservation = formatdate(row[0].strip())
                        dayOfObservation = dateOfObservation.strftime('%Y%m%d')
                        hourOfObservation = dateOfObservation.strftime('%H')
                        item = {'stt':int(row[4].strip()),
                                      'date': dateOfObservation}
                        observation = {'day': dayOfObservation, 
                               'route': row[1].strip(), 
                               'link': row[2].strip(),
                               'hour': hourOfObservation,
                               'direction':row[3].strip(),
                               'item':[]}
                        # Two junctions make up a link
                        junction1 = j.find(row[6])
                        junction2 = j.find(row[7])
                        
                        # If junctions exist in observation transform row for DB 
                        if (junction1 and junction2):
                            observation['_id'] = makeObservationId(observation)
                            jid = makeJunctionId(observation)
                            argv.juncs[jid]={
                                    "_id":jid,
                                    "junction1":junction1,
                                    "junction2":junction2
                                    }
                            keys = argv.timeframe.keys()
                            if not observation['_id'] in keys:
                                argv.timeframe[observation['_id']] = {}
                            keys = argv.timeframe[observation['_id']].keys()
                            if not hourOfObservation in keys:
                                argv.timeframe[observation['_id']][hourOfObservation] = observation
                            argv.timeframe[observation['_id']][hourOfObservation]['item'].append(item)
                    except (AttributeError, RuntimeError, TypeError, NameError, ValueError) as error:
                        db.observation_errors.insert({
                                "item":row,
                                "filename":file_name,
                                "linenumber":i
                            });
                        print("ERROR:",row,error)
                    
            for o in argv.timeframe:
                print ("Hour > " + o)
                for o1 in argv.timeframe[o]:
                    collection.insert(argv.timeframe[o][o1])


def csvreadjunctions(argv):
    parser = ElementTree.XMLParser()
    tree = ElementTree.parse("junctions.kml",parser)
    sites = tree.iterfind(".//*[@name=\"SiteID\"]")
    points = tree.findall('.//{http://www.opengis.net/kml/2.2}coordinates')
    my={}
    loc={}
    
    p = points
    s = sites
    for i,x in enumerate(s):
        my[i] = x.text
    
    for i,p in enumerate(points):
        loc[my[i]] = p.text
        
    with open("junctions.csv") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for y,row in enumerate(csvreader):
            if (y > 0):
                if (validatecsvjunctions(row)):
                    jun = {'point':loc[row[0].strip()],'id': row[0].strip(), 'lon': row[1].strip()[:8], 'lat': row[2].strip()[:8],'desc':row[3].strip()}
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


def makeObservationId(item):
    return item["route"] + "/" + item["link"]  + "/" + item["direction"] + "/" + item["day"]+ "/" + item["hour"]

def makeJunctionId(item):
    return item["route"] + "/" + item["link"]  + "/" + item["direction"]

 
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
filename = "day-20140413.csv.bz2.csv"
filepath = ""
date = ''
find_errors = True
if __name__ == "__main__":
    
    date = filename[4:12]
    if find_errors:
        for root, _, files in os.walk("extracted/"):
            for file_name in files:
                with open("extracted/" + file_name) as csvfile:
                    csvreader = csv.reader(csvfile, delimiter=',' )
                    for i, row in enumerate(csvreader):
                        if not len(row) > 7:
                            item = {
                                "item":row,
                                "filename":file_name,
                                "linenumber":i,
                                "_id": file_name + "." + str(i) 
                            }
                            db.observation_errors.insert(item)
                            
                            
    else:    
        argv = attrdict.AttrDict()
        argv.filename = filename
        argv.filepath = filepath
        argv.date = date
        
        processfile(argv)