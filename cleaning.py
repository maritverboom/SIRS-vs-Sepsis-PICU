# -*- coding: utf-8 -*-
"""
TM2.4 SIRS versus Sepsis
Author: Marit Verboom
Date: 02/2022 - 05/22
"""

# Import modules
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

#%%

def lab_cleaning(dataframe):
    """
    Function to clean DataFrame in case of too many missing values

    Parameters
    ----------
    dataframe : DataFrame to clean

    Returns
    -------
    dataframe : Cleaned DataFrame

    """
    # Drop features with less than 70% values
    dataframe = dataframe.dropna(thresh = 0.7*len(dataframe), axis=1)
    
    # Drop patients with less than 70% of feature values
    dataframe = dataframe.dropna(thresh = 0.8*(len(dataframe.columns)))
    
    return dataframe

def lab_imputation(dataframe):
    # SHOULD BE CHANGED! NEW SAMPLE (TEST) SHOULD BE IMPUTED BASED ON TRAIN SET 
    # rf_cv.py !!!
    imputer = IterativeImputer(random_state=42)
    imputed = imputer.fit_transform(dataframe)
    dataframe = pd.DataFrame(imputed, columns=dataframe.columns)
    round(dataframe, 2)
    
    return dataframe

