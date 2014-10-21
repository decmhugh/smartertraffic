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
from sklearn import neural_network
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
import pickle
from smartcity.module.modelling.prediction import spatialdata
#from smartcity.module.p import Spatial


    
def clflist():
    return [
           [linear_model.LinearRegression(fit_intercept=False, normalize=False),
            "LinearRegression_(copy_X=True, fit_intercept=True, normalize=True)"],
           [linear_model.LinearRegression(fit_intercept=True, normalize=True),
            "LinearRegression_(copy_X=True, fit_intercept=True, normalize=True)"],
           [linear_model.BayesianRidge(),
            "BayesianRidge_()"],
           [linear_model.PassiveAggressiveRegressor(),
            "PassiveAggressiveRegressor_()"],
           [linear_model.LogisticRegression(),
            "LogisticRegression_()"],
           [neural_network.rbm.BernoulliRBM(),
            "LogisticRegression_()"],
           [SVR(C=1.0, cache_size=200, coef0=0.0, kernel='rbf'),
            "SVR_()"]
           ]
    