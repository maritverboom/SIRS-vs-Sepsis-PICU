# -*- coding: utf-8 -*-
"""
TM2.4 SIRS versus Sepsis
Author: Marit Verboom
Date: 02/2022 - 05/22
"""

# Import modules
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import f_classif
import pandas as pd

def selection(data_train, data_test, labels_train):
    """
    Function to select the top x percent of features based on an ANOVA f-test.

    Parameters
    ----------
    data_train : training data (parameters)
    data_test : testing data (parameters)
    labels_train : training data (labels)

    Returns
    -------
    data_train : DataFrame of training data containing top x features 
    data_test : DataFrame of testing data containing top x features
    features : features remaining after feature selection

    """  
    
    # Univariate feature selection based on train data
    fselect = SelectPercentile(f_classif, 90)
    fselect.fit(data_train, labels_train)

    # Names of features that are selected
    dfscores = pd.DataFrame(fselect.scores_)
    dfcolumns = pd.DataFrame(data_train.columns)
    featureScores = pd.concat([dfcolumns,dfscores],axis=1)
    featureScores.columns = ['Specs','Scores'] 
    features = featureScores.nlargest(int(0.9*len(featureScores)),'Scores')
          
    # Transform both train- and testdata (only keep selected features)
    data_train = fselect.transform(data_train)
    data_test = fselect.transform(data_test)
   
    return data_train, data_test, features