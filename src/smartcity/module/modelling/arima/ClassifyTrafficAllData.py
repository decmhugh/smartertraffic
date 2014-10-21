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
from smartcity.module.utils import WeatherData as wd
from pandas.stats.moments import ewma
from sklearn import linear_model
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import RandomizedLogisticRegression

connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic
weatherstore = None
def process_lock(args,junction):
    print("===============================")
    print(args,">>>>>>")
    name = args.replace("/","_")
    dir = "pickle/" + name +  "/"
    path = "C:/Users/IBM_ADMIN/Documents/Disseration/Figures/" 
    global weatherstore
    if weatherstore is None:
        weatherstore = wd.getseriesweather()
    
    
    data = df().from_csv("pickle/" + args.replace("/","_") +  "/" + "data.csv")
    data["IDUBLINC2_dailyrainMM"] = weatherstore["IDUBLINC2"]["dailyrainMM"]
    data["IDUBLINC2_TemperatureC"] = weatherstore["IDUBLINC2"]["TemperatureC"]
    data["ILEINSTE8_dailyrainMM"] = weatherstore["ILEINSTE8"]["dailyrainMM"]
    data["ILEINSTE8_TemperatureC"] = weatherstore["ILEINSTE8"]["TemperatureC"]
    data["ICODUBLI2_dailyrainMM"] = weatherstore["ICODUBLI2"]["dailyrainMM"]
    data["ICODUBLI2_TemperatureC"] = weatherstore["ICODUBLI2"]["TemperatureC"]
    data = data.resample('B').dropna()
    d = df({"STT":data["STT"],
            "STT1":data.shift(1)["STT"],
            "STT2":data.shift(2)["STT"],
            "STT3":data.shift(3)["STT"],
            "STT10":data.shift(5)["STT"],
            "ICODUBLI2_dailyrainMM":data["ICODUBLI2_dailyrainMM"],
            "ICODUBLI2_dailyrainMM":data["ICODUBLI2_dailyrainMM"],
            "ILEINSTE8_TemperatureC":data["ILEINSTE8_TemperatureC"],
            "ILEINSTE8_dailyrainMM":data["ILEINSTE8_TemperatureC"],
            "IDUBLINC2_TemperatureC":data["IDUBLINC2_TemperatureC"],
            "IDUBLINC2_dailyrainMM":data["IDUBLINC2_dailyrainMM"]})
    d = d.dropna().astype(int)
    target = d["STT"].values.copy()
    d.__delitem__("STT")
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(d, target, test_size=0.4, random_state=0)
    clflist = [
           [linear_model.LinearRegression(copy_X=True, fit_intercept=True, normalize=False),
            "LinearRegression(copy_X=True, fit_intercept=True, normalize=False)"],
           [linear_model.RidgeCV(),
            "linear_model.RidgeCV()"],
           [linear_model.Lasso(),
            "Lasso()"],
           [linear_model.PassiveAggressiveRegressor(),
            "PassiveAggressiveRegressor()"],
           [linear_model.ElasticNet(alpha=0.1, rho=0.7),
            "ElasticNet(alpha=0.1, rho=0.7)"],
           [linear_model.BayesianRidge(),
            "BayesianRidge()"],
           [linear_model.ARDRegression(),
            "ARDRegression()"]
           ]

    #C=0.01, penalty="l1", dual=False
    np.set_printoptions(precision=2)
    #plt.plot(target)
    for i,clf in enumerate(clflist):
        p = clf[0].fit (X_train, y_train)
        scores = cross_validation.cross_val_score(clf[0], X_test.astype(np.float), y_test.astype(np.float), cv=7)
        predicted = clf[0].predict(d)
        features_coef = []
        feature_importances = []
        if hasattr(clf[0], 'coef_'):
            a = ['{:.2}'.format(a) for a in clf[0].coef_]
            features_coef = {"columns":list(d.columns),"values":a}
            print(features_coef)
        if hasattr(clf[0], 'feature_importances_'):
            a = ['{:.2}'.format(a) for a in clf[0].feature_importances_]
            feature_importances = {"columns":list(d.columns),"values":a}
            print(feature_importances)
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        result = {"i":i,"_id":("" + str(i) + "_" + args),"clf" : clf[1],
                  "features_coef" : features_coef,"feature_importances" : feature_importances}
        db.prediction_results.remove({"_id":("" + str(i) + "_" + args)});
        db.prediction_results.insert(result);
    
    
             
    
def process(args,junction):
    pickle_dir = "pickle/" + args.replace("/","_")
    print(pickle_dir)
    result = None
    
    if not os.path.isdir(pickle_dir):
        os.makedirs(pickle_dir)
    a = datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        process_lock(args,junction);
        #print(result)
        #pickle.dump(result, open(pickle_dir + "/result.res", 'wb'))
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
    #weatherstore = WeatherData.getseriesweather()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in junctions:
        process(junction["_id"],junction)
   
if __name__ == "__main__":
    run()
    #for p in ["17/6/1","13/2/1","30/7/1","10/7/2","16/2/2","30/4/2"]:
    #for p in ["30/4/2"]:
    #    process_lock(p)
        
     

    