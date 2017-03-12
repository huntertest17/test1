import re,os,sys
import pandas as pd
import numpy as np
import xgboost as xgb
import scipy
import datetime
from pylab import *
from copy import deepcopy
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.preprocessing import Imputer
from xgboost.sklearn import XGBClassifier
from sklearn.neighbors import  KNeighborsRegressor
import sqlite3

class SQ:#{{{
    dbName = 'data.db'

    def __init__(self):
        self.conn=sqlite3.connect(self.dbName)
        self.c= self.conn.cursor()

    def __del__(self):
        self.c.close()
        self.conn.close()

    def getRaw(self,query, params):
        self.c.execute(query, params)
        data = self.c.fetchall()
        return data

    def get(self,symbol):
        self.c.execute("select * from %s" % symbol)
        rL=pd.DataFrame(self.c.fetchall(), columns=['date','open','high','low','close','volume','adjclose'])
        rL.date = rL.date.astype(int).apply(datetime.datetime.fromordinal)
        rL.index = rL.date
        return rL

#}}}

def indStochasticOsc(d,period=14):#{{{
    oL = []
    for i in range(len(d)-period):
        mx = max(d[i:i+period])
        mn = min(d[i:i+period])
        oL.append((d[i] - mn)/(mx-mn))
    t = pd.Series(oL)
    t.index = d.index[:len(t)]
    return t

#}}}

S = SQ()



