# -*- coding: utf-8 -*-
"""
TM2.4 SIRS versus Sepsis
Author: Marit Verboom
Date: 02/2022 - 05/22
"""
# Import modules
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import model_selection

# Created functions
from cleaning import lab_imputation
from selection import selection
from random_forest_opt import random_forest_opt
from ROCcurves import ROC_all

#%%

def rf_cv(features):    
    # Label (y) and parameters (X)
    y = features['Label']
    X = features.drop(columns=['Label'])
     
    # Create empty DataFrames and figure
    score, sens, spec, tprs, aucs = [], [], [], [], []
    fig, ax = plt.subplots()
    
    # Create DataFrame with a column per parameter
    important_features = pd.DataFrame(X.columns)
    important_features.columns = ['Specs']
        
    # 5-fold cross validation
    cv5_fold = model_selection.StratifiedKFold(n_splits=5) 
    
    for index_train, index_test in cv5_fold.split(X,y):
        label = np.array(y)
        train = X.iloc[index_train]
        train_label = label[index_train]
        test = X.iloc[index_test]
        test_label = label[index_test]
        
        # Imputation for train- and testset independently 
        train = lab_imputation(train)
        test = lab_imputation(test)
        
        # Parameter selection
        train, test, features_select = selection(train, test, train_label)
        
        # Random Forest optimalization
        rfmodel, score_test, sens_test, spec_test, features_select = random_forest_opt(train, test, 
                                                                                         train_label, test_label,
                                                                                         features_select)                                                                               
        # Store scores
        score.append(score_test)
        sens.append(sens_test)
        spec.append(spec_test)
       
        # Plot ROC curves
        tprs, aucs = ROC_all(rfmodel, test, test_label, tprs, aucs, fig, ax,
                             "Receiver operating characteristics")
       
        # Save used features and importance  
        important_features = pd.merge(important_features, features_select, how="outer", on=["Specs"])
        
    return score, sens, spec, tprs, aucs, important_features 
        

