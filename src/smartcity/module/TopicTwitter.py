import codecs
from datetime import datetime
import sys
from pymongo import Connection as mongoConn
import threading

from TwitterAPI import TwitterAPI, TwitterRestPager
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

at = "30843655-qpmhkCInoDu0GVbOeFcovqPvqhUmEuNSNFzBDg8Oo"
ats = "43RLokonH5Xm6xVVK3k32y3lpcwoNAuw2vSnSxW1pBS83"
ct = "QVP5fPwdWvy4mTS02k5ylg"
cs ="WD5HYZZYvdYs712AxeKHAHuOPfN8qec3OGu87GG7kM"

# SAVE YOUR APPLICATION CREDENTIALS IN TwitterAPI/credentials.txt.
#o = TwitterOAuth.read_file()
api = TwitterAPI(ct, cs, at, ats)

connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
collection = db.twitter_search_term

def parse(item,s):
    d = datetime.now()
    user = {}
    place = {}
    if not item['user'] is None:
        print(item['user'])
        for key,value in item['user'].items():
            if not key is None and not value is None:
                user[key] = str(value)
    if not item['place'] is None:            
        for key, value in item['place'].items():
            if not key is None and not value is None:
                place[key]=str(value)
    
    item = {"date": d,
            "search":s,
            "id" : str(item['id']),
            "user": user,
            "place": place,
            "text": item['text'],
            "geo": str(item['geo']),
            "coordinates": str(item['coordinates']),
            "retweeted" : str(item['retweeted']),
            "source" : str(item['source'])}
    return item
      

def runner(s):
    try:        
        # STREAM TWEETS FROM AROUND THE WORK
        #for item in api.request('statuses/filter', {'locations':'-180,-90,180,90'}):
        for item in api.request('search/tweets', {'q':s,'locations':'54,-8,52.6,-5.78'}):
        #for item in api.request('statuses/filter', {'locations':'53,20,6,15'}):
            print(s,item)
            if (item['text'] if 'text' in item else item):
                result = parse(item,s)
                collection.insert(result)
    except Exception as e:
        print(e)
t = []      
t.append(threading.Thread(target=runner("weather")))
t.append(threading.Thread(target=runner("flood")))
t.append(threading.Thread(target=runner("traffic")))
t.append(threading.Thread(target=runner("jam")))
t.append(threading.Thread(target=runner("@aaroadwatch")))
for tr in t:
    tr.start()
    

        