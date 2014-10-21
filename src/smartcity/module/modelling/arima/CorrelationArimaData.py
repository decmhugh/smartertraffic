'''
Created on 3 Dec 2013

@author: declan
'''
from pymongo import Connection as mongoConn
import os,gc,sys
import numpy as np
from datetime import datetime, date
from pandas.core.series import TimeSeries
from sklearn import cross_validation
from pandas import DataFrame as df
from sklearn import linear_model
from bson import json_util
import pandas as pd
from sklearn import svm
from scipy import stats
import statsmodels.formula.api as sm
from statsmodels.graphics.api import qqplot
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pandas.tools.plotting import autocorrelation_plot
from pandas.tools.plotting import lag_plot
from pandas.tools.plotting import bootstrap_plot
from sklearn.preprocessing import normalize

connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
col = ["Lag -" + str(a) for a in range(1,16)]
table = df(columns=col)
links = []
def addrow(df, row):
    return df.append(pd.DataFrame(row), ignore_index=True)

def process_lock(args):
    global table
    name = args.replace("/","_")
    dir = "pickle/" + name +  "/"
    path = "C:/Users/IBM_ADMIN/Documents/Disseration/Figures/"
    data = df().from_csv(dir + "data.csv")
    
    result = db.peak_weekday.find({"_id":args}).sort("_id", -1) 
    hour = [0,0]
    data = data.dropna()
    for res in result:
        h = res["item"][0]["hour"]
        hour[0] = str(h) + ":00"
        hour[1] = str((h)) + ":59"
        print(hour)
    try:
        data = data.between_time(hour[0],hour[1]).resample('B').dropna()
    except Exception: 
        data = data.resample('B').dropna()
    
    ts1 = pd.Series(data["STT"].values.squeeze())
    #result = autocorrelation_plot(ts1)
    lagged = pd.concat([ts1.shift(a) for a in range(0,20)], axis=1).dropna()
    row = [np.corrcoef(lagged[0].values,lagged[a].values)[0,1] 
                        for a in range(1,16)]
    #row.insert(0, args) 
    global col  
    print(table)  
    table = table.append(row, ignore_index=True)   
    print(table)    
    #table.concat(row, ignore_index=True)
    
    #plt.savefig(path + "autocorrelogram_pandas_" + name)
    #plt.savefig(dir + "autocorrelogram_pandas_" + name)
    
    #bootstrap_plot(ts1, size=10, samples=40, color='grey')
    #plt.savefig(path + "bootstrap_plot_pandas_" + name)
    #plt.savefig(dir + "bootstrap_plot_pandas_" + name)
    
    #plt.show()
    print("-----------SCORE-----------------------------")
    print(args,">>>")
    print(hour,">>>")
    #result = sm.ols(formula="STT ~ Lag_1 + Lag_2 + Lag_3 + Lag_4 + Lag_5 + Lag_6", data=d).fit()
    #print(result.summary())
    
    
             
    
def process(args):
    pickle_dir = "pickle/" + args.replace("/","_")
    print(pickle_dir)
    result = None
    if not os.path.isdir(pickle_dir):
        os.makedirs(pickle_dir)
    a = datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        process_lock(args);
        
    except ValueError as error:
        print(error)
    b = datetime.now().strftime('%Y%m%d%H%M%S')
    with open("pickle/" + args.replace("/","_") + "/timestamp.txt", "w") as target:
        target.write("start:" + a)
        target.write("end:" + b)
        target.close()
    return result;  

def run():
    global table
    np.set_printoptions(precision=2,suppress=True)
    cursor = db.junctions.find()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in junctions[:1]:
        try:
            process(junction["_id"])
        except (RuntimeError, TypeError, NameError) as error:
            print(junction["_id"],error)
    table.to_csv("correlation_lagged.csv")
   
if __name__ == "__main__":
    run()
    #for p in ["17/6/1"]:
    #    process_lock(p)
    #process_lock("18/2/1")
        
     

    