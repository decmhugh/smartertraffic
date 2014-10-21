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
from smartcity.module.modelling.arima import RangeData

    


connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic

classifier_list = [
       linear_model.LinearRegression(),
       linear_model.ElasticNet(),
       linear_model.PassiveAggressiveRegressor()
       ]

def process_lock(args):
    
    data = df().from_csv("pickle/" + args.replace("/","_") +  "/" + "data.csv")
    data = data.resample('B').dropna()
    #data = df({"STT":[1,2,3,4,5,6,7,5,3,2,2,2],"S":[1,2,3,4,5,6,7,5,3,2,2,2]})
    #plt.plot(data["STT"].values)
    d = df({"STT":data["STT"].values,
            "STT1":data.shift(1)["STT"],
            "STT2":data.shift(2)["STT"],
            "STT3":data.shift(3)["STT"],
            "STT4":data.shift(4)["STT"],
            "STT5":data.shift(5)["STT"]})
    d = d.dropna().astype(int)
    x = d.copy()
    x.__delitem__("STT")
    #print(x)
    #d.plot(figsize=(12,8));
    #plt.plot(RangeData.range(d))  
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    fig = plot_acf(d["STT"].values.squeeze(), lags=40, ax=ax1)
    #fig = plot_pacf(d, lags=40, ax=ax1)
    #d.plot()
    plt.show()
    #ax2 = fig.add_subplot(212)
    #fig = plot_pacf(d.index.values, lags=40, ax=ax2)
    #print("Get training data")
    #X_train, X_test, y_train, y_test = cross_validation.train_test_split(
    #            x, d["STT"].values, test_size=0.4, random_state=0)
    
    #print(X_train.shape, y_train.shape)
    #print(X_test.shape, y_test.shape)

    print("-----------SCORE-----------------------------")
    print(args,">>>")
    result = sm.ols(formula="STT ~ STT1 + STT2 + STT3", data=d).fit()
    print(result.summary())
    #fig = plt.figure(figsize=(12,8))
    #ax1 = fig.add_subplot(211)
    #linear_model.
    #fig = sm.graphics.tsa.plot_acf(d["STT"].values, lags=40, ax=ax1)
    #ax2 = fig.add_subplot(212)
    #fig = sm.graphics.tsa.plot_pacf(d["STT"].values, lags=40, ax=ax2)

    #print("Get Classifier")
    #clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
    #print("Get Score")
    #print(clf.score(X_test, y_test))
    #predicted = clf.predict(X_test)
    #print(predicted)
    #scores = cross_validation.cross_val_score(clf, X_test, y_test, cv=6)
    #print(scores)
    #print(scores.std())
    #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    #print("Explained Variance Score: %0.2f" % explained_variance_score(y_test, predicted))
    #print("Mean Absolute Squared: %0.2f" % mean_absolute_error(y_test, predicted))
    #print("Mean Squared Squared: %0.2f" % mean_squared_error(y_test, predicted))
    
    
             
    
def process(args):
    pickle_dir = "pickle/" + args.replace("/","_")
    print(pickle_dir)
    result = None
    if not os.path.isdir(pickle_dir):
        os.makedirs(pickle_dir)
    a = datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        process_lock(args);
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
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in junctions:
        process(junction["_id"])
   
if __name__ == "__main__":
    #for p in ["17/6/1","13/2/1","30/7/1","10/7/2","16/2/2","30/4/2"]:
    process_lock("9/9/1")
        
     

    