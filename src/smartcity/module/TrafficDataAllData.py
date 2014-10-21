'''
Created on 3 Dec 2013

@author: declan
'''
from pymongo import Connection as mongoConn
import os,csv
import numpy as np

connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic

    
def process(filename):
    db = connection.traffic
    with open("extracted/" + filename) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',' )
        for row in csvreader:
            if len(np.array(row)) > 7:
                data = {"datetime":row[0],"route":row[1],"link":row[2],"direction":row[3],
                        "point_a":row[4],"point_b":row[5],"stt":row[6],"acc_stt":row[7],}
                db.traffic_all.insert(data)  
                    
if __name__ == "__main__":
    import datetime
    for root, _, files in os.walk("extracted/"):
        for file_name in files:
            print(file_name,datetime.datetime.now())
            process(file_name)

    