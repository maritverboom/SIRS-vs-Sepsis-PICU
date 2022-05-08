# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 14:22:39 2022

@author: mverboom1
"""

import pandas as pd
from sklearn import preprocessing 

def scaling(data_train, data_test):
    '''This is a function to scale the data with a robust scaler. The median 
    of the data is removed and the data is scaled according to an 
    interquantile range, ranging from the 25th to the 75th quantile.'''
    # Scale the data (train on train set)
    scaler = preprocessing.RobustScaler()   
    scaler.fit(data_train)  

    # Perform scaling on both train and testset, returing scaled dataframe
    data_train = pd.DataFrame(scaler.transform(data_train), columns = data_train.columns)
    data_test = pd.DataFrame(scaler.transform(data_test), columns= data_test.columns) 
    
    return data_train, data_test