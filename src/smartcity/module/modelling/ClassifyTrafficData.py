'''
Created on 3 Dec 2013

@author: declan
'''
from pymongo import Connection as mongoConn
import os,gc,sys
import numpy as np
from datetime import datetime, date
from matplotlib import pylab as plt
from pandas.core.series import TimeSeries
from pandas import DataFrame as df
from pandas.stats.moments import ewma
from sklearn import linear_model
import json,pickle
from bson import json_util
import memcache
from sklearn.externals import joblib
import pandas as pd

from sympy import *


mem = memcache.Client(["localhost:11211"])
connection = mongoConn('mongodb://localhost:27017/')
db = connection.traffic

classifier_list = [
       linear_model.LinearRegression(),
       linear_model.ElasticNet(),
       linear_model.PassiveAggressiveRegressor()
       ]

def process_lock(args):
    
    dframe = df()

    t_list = list(['STT1','STT2','STT3','Rain','Wind','Temperature','Rain1','Wind1','Temperature1'])
            
    train_df = df().from_csv("pickle/" + args.replace("/","_") +  "/" + "training_data.csv")
    test_df = df().from_csv("pickle/" + args.replace("/","_") +  "/" + "testing_data.csv")
    train_features = train_df[t_list].values
    train_labels = train_df["STT"].values
    test_features = test_df[t_list].values
    test_labels = test_df["STT"].values
    
    
    #classifier_list = [Pipeline([
    ##  ('feature_selection', LinearSVC(penalty="l1")),
    #  ('classification', RandomForestClassifier())
    #])]
    result_list = []
    for classifier in classifier_list:
        clf = classifier
        classz = clf.__class__.__name__;
        print(classz)
        
        clf.fit(train_features, train_labels) 
        #print("Predict test", len(np.array(test_features)))
        result = clf.predict(test_features)
        print("\n_____________________________________")
        print("Classifier : " + classz)

        #f1score = metrics.f1_score(test_features, np.array(result))
        #acc_score = metrics.accuracy_score(test_features, np.array(result))
        #r2_score = metrics.r2_score(test_features, np.array(result))
        score = np.mean(clf.score(test_features, test_labels));
        #print("f1-score:   %0.3f" % score)

        #if hasattr(clf, 'coef_'):
        #    print("density: %f" % density(clf.coef_))
        #    for i, category in enumerate(t_list):
        #        print(category,clf.coef_[i])

        #print("TimeSeries test")
        ts = TimeSeries(np.array(test_labels),test_df.index) 
        #print("Result test")
        ts1 = TimeSeries(np.array(result),test_df.index) 
        dframe = df({"actual":ts,
                     "predicted":ts1,
                     "Rain":test_df["Rain"].values,
                     "Temperature":test_df["Temperature"].values})
        residuals = np.mean((clf.predict(test_features) - test_labels) ** 2);
        
        
       

        print ("Residual sum of squares: %.2f" % residuals)
        print ('Variance score: %.2f' % score)
        #print ('F1 score: %.2f' % f1score)
        #print ('R2 score: %.2f' % r2_score)
        #print ('Accuracy score: %.2f' % acc_score)
        print ('Coef' , clf.coef_)
       
        dframe.plot()
        cls_file = "pickle/" + args.replace("/","_") +  "/" + classz +".cls"
        joblib.dump(clf, cls_file) 
        plt.savefig("pickle/" + args.replace("/","_") + "/img_" + args.replace("/","_") + "_" + classz +".jpg")
        for i, item in enumerate(t_list):
            print(item,clf.coef_[i]);
        result_list.append({
             "classifier":classz,
             "residuals":residuals,
             "variancescore":score,
             "coef":clf.coef_,
             "success": "true"
             })
    result_list = sorted(result_list, key=lambda k: k['residuals']) 
    return {"args":args,
            "neighbours":[],
            "model":t_list,
            "results":result_list
             }
             
    
def process(args):
    pickle_dir = "pickle/" + args.replace("/","_")
    print(pickle_dir)
    result = None
    if not os.path.isdir(pickle_dir):
        os.makedirs(pickle_dir)
    a = datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        result = process_lock(args);
        print(result)
        pickle.dump(result, open(pickle_dir + "/result.res", 'wb'))
    except ValueError as error:
        print(error)
    b = datetime.now().strftime('%Y%m%d%H%M%S')
    with open("pickle/" + args.replace("/","_") + "/timestamp.txt", "w") as target:
        target.write("start:" + a)
        target.write("end:" + b)
        target.close()
    return result;  

def run():
    pd.options.display.float_format = '${:,.2f}'.format
    cursor = db.junctions.find()
    json_str =json_util.dumps(cursor)
    junctions =json_util.loads(json_str)
    junctions = sorted(junctions, key=lambda k: k['route']) 
    for junction in junctions:
        process(junction["_id"])
   
if __name__ == "__main__":
    run()
        
     

    