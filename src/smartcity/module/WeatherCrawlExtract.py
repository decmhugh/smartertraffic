'''
Created on 3 Dec 2013

@author: declan
'''

import csv,io
import requests
from dateutil import rrule
from datetime import datetime
from pymongo import Connection as mongoConn

connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
collection = db.weather

path = 'weather/'
def extractNodeText(node):
    return node.xpath("string()", encoding="UTF-8").replace('\t','').replace('\s','').replace('\n','')

def weatherForDate(data):
    urlarg = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID={:s}&&day={:s}&year={:s}&month={:s}&format=1"
    url = urlarg.format(data['location'],data['day'],data['year'],data['month'])
    print(url)
    r = requests.get(url)
    text = r.text
    csvreader = csv.reader(io.StringIO(text), delimiter=',' )
    headers = []
    data["item"] = []
    
    for row in csvreader:
        if check(row):
            if len(headers) == 0:
                headers = row
            else:
                item= {}
                for idx, cell in enumerate(row[:15]):
                    item[headers[idx]] = cell
                data["item"].append(item) 
    #collection.remove({"_id":data["_id"]})      
    collection.insert(data)
    print(data)
    
            
def check(row):  
    if len(row) > 1:  
        return True
    return False 

def daterange(start_date, end_date):
    for n in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
        yield(n)  

def crawlWeatherForDate(args):
    obj = args 
    stations = ['ICODUBLI2','ILEINSTE8','IDUBLINC2']
    for station in stations:
        print(obj)
        s = obj.strftime("%Y") + obj.strftime("%m") + obj.strftime("%d") + "_" + station
        data = {"_id":s,'date': obj.now(),'location': station, 'month': obj.strftime("%m"), 
                "year": obj.strftime("%Y"), 'day': obj.strftime("%d")}
        weatherForDate(data)

if __name__ == "__main__":
    end = datetime.now()
    #end = datetime.strptime("20140201", "%Y%m%d")
    start = datetime.strptime("20140101", "%Y%m%d")
    #datelist = 
    d = daterange(start,end)
    stations = ['ICODUBLI2','ILEINSTE8','IDUBLINC2']
    for obj in reversed(list(d)):
        for station in stations:
            print(obj)
            s = obj.strftime("%Y") + obj.strftime("%m") + obj.strftime("%d") + "_" + station
            data = {"_id":s,'date': obj.now(),'location': station, 'month': obj.strftime("%m"), 
                    "year": obj.strftime("%Y"), 'day': obj.strftime("%d")}
            weatherForDate(data)