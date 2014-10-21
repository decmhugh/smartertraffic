'''
Created on 3 Dec 2013

@author: declan
'''
from datetime import datetime, date
import os, gc, sys, geopy,csv

from bson import json_util
from pandas import DataFrame as df

from smartcity.module.utils import WeatherData as wd
from smartcity.module.utils import junctionhelper as jh


def weather_corr():
    path = os.path.dirname(os.path.realpath(__file__))
    data = df().from_csv(path + "/weather_correlation_lagged.csv")   
    return data      

if __name__ == "__main__":
    data = weather_corr()
    print(data)
    
    
        
     

    