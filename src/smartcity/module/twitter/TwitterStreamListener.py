import codecs,sys
from datetime import datetime as dt
from pymongo import Connection as mongoConn
connection = mongoConn('mongodb://admin:admin@ds063287.mongolab.com:63287/traffic')
db = connection.traffic
collection = db.twitter_aa
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager


try:
        # python 3
        sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
except:
        # python 2
        sys.stdout = codecs.getwriter('utf8')(sys.stdout)
at = "30843655-qpmhkCInoDu0GVbOeFcovqPvqhUmEuNSNFzBDg8Oo"
ats = "43RLokonH5Xm6xVVK3k32y3lpcwoNAuw2vSnSxW1pBS83"
ct = "QVP5fPwdWvy4mTS02k5ylg"
cs ="WD5HYZZYvdYs712AxeKHAHuOPfN8qec3OGu87GG7kM"

# SAVE YOUR APPLICATION CREDENTIALS IN TwitterAPI/credentials.txt.
#o = TwitterOAuth.read_file()
api = TwitterAPI(ct, cs, at, ats)


TEST_NUMBER = 4

def run():
    try:
            if TEST_NUMBER == 0:
    
                    # VERIFY YOUR CREDS
                    r = api.request('account/verify_credentials')
                    print(r.text)
    
            if TEST_NUMBER == 1:
            
                    # POST A TWEET 
                    r = api.request('statuses/update', {'status':'the time is now %s' % dt.now()})
                    print(r.status_code)
    
            if TEST_NUMBER == 2:
            
                    # GET 5 TWEETS CONTAINING 'ZZZ'
                    for item in api.request('search/tweets', {'q':'zzz', 'count':5}):
                            print(item['text'] if 'text' in item else item)
    
            if TEST_NUMBER == 3:
                    print("reading option 3")
                    id = 933606542693515265
                    # STREAM TWEETS FROM AROUND NYC
                    #result = collection.find()
                    #inverse = [int(value["_id"]) for value in result]
                    #id = (min(inverse))
                    #
                    while (True):
                        for i,item in enumerate(api.request('statuses/user_timeline', {'screen_name':'aaroadwatch',"count": 180,"include_entities":"true","max_id":id})):
                                print("i")
                                place = {}
                                if not item['place'] is None:            
                                    for key, value in item['place'].items():
                                        if not key is None and not value is None:
                                            place[key]=str(value)
                                print(i,item['text'] if 'text' in item else item)
                                print(item['created_at'],item['id'])
                                d = {"text":item['text'],"place":item['place'],"geo":item['geo'],"screen_name":item['user']['name'],"_id" : item['id'],"created_at" : item['created_at'],"hashtags" : item['entities']['hashtags']}
                                collection.remove({"_id":item['id']})
                                collection.insert(d)
                                if (id > item['id']):
                                    id = item['id']
                                    print(id)
                    #while True:  
                    #until     
                    #    for j,item in enumerate(api.request('statuses/user_timeline', {'screen_name':'aaroadwatch,GardaTraffic',"count": 10,"max_id":id,"include_my_retweet":1})):
                    #            i=i+1
                    #            print(i,item['text'] if 'text' in item else item)
                    #            print(item['created_at'])
                    #            d = {"text":item['text'],"screen_name":item['user']['name'],"_id" : item['id'],"created_at" : item['created_at']}
                    #            collection.insert(d)
                    #            if (id > item['id']):
                    #                id = item['id']
    
            if TEST_NUMBER == 4:
                print("Starting")
                while True:
                    try:
                        for item in api.request('statuses/filter', {'locations':'-7,51,-5,54'}):
                        #print item.keys()
                        
                            fmt = '%Y-%m-%d %H:%M:%S %Z'
                            fmt2 = '%Y%m%d%H%M%S'
                            d = dt.now()
                            d_string = d.strftime(fmt)
                            d_string2 = d.strftime(fmt2)
                            s = {}
                            s["date"] = d_string
                            s["item_id"] = str(item['id'])
                            for key, value in item['user'].items():
                                s["user_"+key+""] = str(value)
                            s["text"] = item['text']
                            if 'place' in item.keys():
                                for key, value in item['place'].items():
                                    s["place_"+key+""] = str(value)
                            s["geo"] = str(item['geo'])
                            s["coordinates"] = str(item['coordinates'])
                            s["retweeted"] = str(item['retweeted'])
                            s["source"] = str(item['source'])
                            #s += "\nuser," + item['user']
                            #s += "\nuser," + item['user']
                            if 'text' in item.keys():      
                                print(s)  
                                db.twitter_streaming.insert(s);
                    except (RuntimeError, TypeError, NameError, IOError)as e:
                            pass
                            
    except Exception as e:
        run();
        print(e)
print("RUN")
run();