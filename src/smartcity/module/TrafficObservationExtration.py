import bz2
import os

import attrdict
import urllib3
from datetime import datetime
from bs4 import BeautifulSoup

# check for extraction directories existence
if not os.path.isdir('downloaded'):
    os.makedirs('downloaded')

if not os.path.isdir('extracted'):
    os.makedirs('extracted')

def persistTrafficData(a):
    #if os.path.isfile("extracted/" + a):
    filename = a
    date = filename[4:12]
    
    argv = attrdict.AttrDict()
    argv.filename = a
    argv.date = date
    #del GisConvert
    #if "201310" in a:
    import smartcity.module.TransformTrafficData as tranformData
    import smartcity.module.WeatherCrawlExtract as wc
    
    date = datetime.strptime(date,"%Y%m%d")        
    w = wc.crawlWeatherForDate(date)
    g = tranformData.processfile(argv)
    
    del g
    del w
    del argv
    
http = urllib3.PoolManager()
archiveDirectory = "http://www.dublinked.ie/datastore/local/DCC/trips/archive/"
http_pool = urllib3.connection_from_url(archiveDirectory)
stream = http_pool.urlopen('GET',archiveDirectory)
text = stream.data


# retrieve list of URLs from the webservers
soup = BeautifulSoup(text)
res = soup.find_all('a',href=True)
links = []
for n in res:
    if "." in n['href']:
        links.append(n['href'])

# only parse urls
for filename in links: 
    if '.' in filename:
        
        # download the file
        archiveFile = archiveDirectory + filename
        outputFile = "downloaded/" + filename
        print("Start ",datetime.now())
        # check if file already exists on disk
        if os.path.isfile(outputFile) is not True:
            print("Skipping " + archiveFile)
            print("Downloading ",archiveFile)
            http_pool = urllib3.connection_from_url(archiveFile)
            rcsv = http_pool.urlopen('GET',archiveFile)
            # save data to disk
            output = open(outputFile,'wb')
            
            output.write(rcsv.data)
            output.close()
            
            
        if os.path.isfile("extracted/" + filename + ".csv") is not True:
            zfobj = bz2.BZ2File(outputFile, 'rb')
            try:
                #save extracted file
                f = open("extracted/" + filename + ".csv",'wb')
                f.write(zfobj.read())
                f.close()
                
            except (RuntimeError, TypeError, NameError) as error:
                print("Error: ",error)        
            finally:
                zfobj.close()
                
            persistTrafficData(filename + ".csv")
        print("End ",datetime.now())
        exit()
 
