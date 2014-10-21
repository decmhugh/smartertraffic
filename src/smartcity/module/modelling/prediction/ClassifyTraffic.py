'''
Created on 3 Dec 2013

@author: declan
'''
from datetime import datetime, date
import os, gc, sys, pickle
from sklearn.svm import SVR
from sklearn.svm import LinearSVC
from sklearn.metrics import fbeta_score, make_scorer
from bson import json_util
from pandas import DataFrame as df
from pandas.core.series import TimeSeries
from pandas.stats.moments import ewma
from pymongo import Connection as mongoConn
from scipy import stats, spatial
from sklearn import cross_validation
from sklearn import linear_model
from sklearn import linear_model
from sklearn import svm
from sklearn.linear_model import RandomizedLogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from statsmodels.graphics.api import qqplot
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.graphics.tsaplots import plot_pacf
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from smartcity.module.utils import WeatherData as wd
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
from sklearn.metrics.metrics import explained_variance_score
from smartcity.module.modelling.prediction import spatialdata,\
    ClassifyAlgorithms



connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
weatherstore = None

def data_result(args):
    name = args.replace("/","_")
    dir = "pickle/" + name +  "/"
    path = "C:/Users/IBM_ADMIN/Documents/Disseration/Figures/"
    data = df().from_csv(dir + "data.csv")
    data = data.resample('B').dropna()
    return data

def process_lock(args,junction):
    print("===============================")
    print(args,">>>>>>")
    name = args.replace("/","_")
    dir = "pickle/" + name +  "/"
    path = "C:/Users/IBM_ADMIN/Documents/Disseration/Figures/" 
    
    cursor = db.max_neighbour.find({"_id":args})
    json_str =json_util.dumps(cursor)
    neighbour_list =json_util.loads(json_str)
    neighbour = neighbour_list[0]["max"]
    n_data = data_result(neighbour).fillna(0)
    
    
    global weatherstore
    if weatherstore is None:
        {}
        weatherstore = wd.getseriesweather()
        
    pkl = "pickle/peak/" + args.replace("/","_") +  "/"
    data = data_result(args).fillna(0)
    
    data["ILEINSTE8_dailyrainMM"] = weatherstore["ILEINSTE8"]["dailyrainMM"].fillna(0)
    data["ILEINSTE8_TemperatureC"] = weatherstore["ILEINSTE8"]["TemperatureC"].fillna(0)
    data["IDUBLINC2_dailyrainMM"] = weatherstore["IDUBLINC2"]["dailyrainMM"].fillna(0)
    data["IDUBLINC2_TemperatureC"] = weatherstore["IDUBLINC2"]["TemperatureC"].fillna(0)
    
    d = df({"STT":data["STT"],
            "W_ILT":data["ILEINSTE8_TemperatureC"],
            "W_ILR":data["ILEINSTE8_dailyrainMM"],
            "W_DLR":data["IDUBLINC2_dailyrainMM"],
            "W_DLT":data["IDUBLINC2_TemperatureC"],
            "S_MAX":n_data["STT"].shift(1)})
    
    d = d.resample('B').dropna()
    # Do the lagging
    d["STT1"]=d.shift(1)["STT"]
    d["STT2"]=d.shift(2)["STT"]
    d["STT3"]=d.shift(3)["STT"]
    d["STT5"]=d.shift(5)["STT"]
    
    d = d.dropna().fillna(0).astype(np.float)
    d.to_csv(pkl + "" + name + "sample.csv")
    target = d["STT"].values.copy()
    d.__delitem__("STT")
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(d, target, test_size=0.3, random_state=0)
    
    
    
    clflist = ClassifyAlgorithms.clflist()
    # Scoring
    mae = mean_absolute_error
    mse = mean_squared_error
    r2  = r2_score
    #C=0.01, penalty="l1", dual=False
    np.set_printoptions(precision=2)
    result = []
    scores_res = []
    for i,clf in enumerate(clflist):
        try:
            pname = ''.join(e for e in clf[1] if e.isalnum() or e is "_")
            p = clf[0].fit(X_train, y_train)
            scores = cross_validation.cross_val_score(
                                    p, X_test.astype(np.float), y_test.astype(np.float), cv=7)
            y_pred = clf[0].predict(X_test.astype(np.float))
            y_true = y_test.astype(np.float)
            sample = p.predict(d)
            sample_df = df({"predicted": sample,"target": target})
            sample_df.to_csv(pkl + "" + pname + ".predict.csv")
            sample_df.plot()
            try:
                if os.path.isfile(pkl + "" + pname + ".figure.jpg"):
                    os.remove(pkl + "" + pname + ".figure.jpg")
                plt.savefig(pkl + "" + pname + ".figure.jpg")
                plt.close()
            except (RuntimeError, TypeError, NameError):
                pass
                   
            mae = round(mean_absolute_error(y_true, y_pred), 2)
            mse = round(mean_squared_error(y_true, y_pred), 2)
            evs = round(explained_variance_score(y_true, y_pred), 2)
            r2 = round(r2_score(y_true, y_pred), 2)
            current = {
                      "clf":    clf[1],
                      "i":    i,
                      "scores_mae":     mae,
                      "scores_mse":     mse,
                      "scores_r2":      r2,
                      "scores_evs":     evs,
                      "std":d["STT1"].std(),
                      "quantile":d["STT1"].quantile(.8)
                      }
            
            scores_res.append(current)
            
            print("Accuracy MAE: " + str(mae))
            print("Accuracy MSE: " + str(mse))
            print("Accuracy R2 :" + str(r2))
            print("Accuracy EVS " + str(evs))
            insert = {"i":i,"_id":args,"clf" : clf[1],
                      "predicted" : list(y_pred),
                      "target": list(y_true)}
            result.append(insert)
            
            for the_file in os.listdir(pkl):
                file_path = os.path.join(pkl, the_file)
                try:
                    if os.path.isfile(file_path) and not "." in the_file:
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
                
            pickle.dump( clf[0], open(pkl + "" + pname + ".cls.pkl" , "wb" ) )
        except Exception as e:
            print(e)
    print("insert " + name)
    db.prediction_results.insert(
            {"_id":args,"result":result,"scores":scores_res})
    
    
             
    
def process(args,junction):
    pickle_dir = "pickle/peak/" + args.replace("/","_")
    print(pickle_dir)
    result = None
    
    if not os.path.isdir(pickle_dir):
        os.makedirs(pickle_dir)
    a = datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        process_lock(args,junction);
    except ValueError as error:
        print(error)
    b = datetime.now().strftime('%Y%m%d%H%M%S')
    with open("pickle/" + args.replace("/","_") + "/timestamp.txt", "w") as target:
        target.write("start:" + a)
        target.write("end:" + b)
        target.close()
    return result;  

def run():
    cursor = db.junctions.find()
    global weatherstore
    db.prediction_results.remove()
    #weatherstore = wd.getseriesweather()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in reversed(junctions):
        print(junction["_id"])
        process(junction["_id"],junction)
   
if __name__ == "__main__":
    #run()
    #for p in ["17/6/1","13/2/1","30/7/1","10/7/2","16/2/2","30/4/2"]:
    #for p in ["17/6/1"]:
    cursor = db.junctions.find()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in junctions:
        print(junction["_id"])
        process(junction["_id"],junction)

        
     

    