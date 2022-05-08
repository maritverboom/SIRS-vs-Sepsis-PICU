# -*- coding: utf-8 -*-
"""
TM2.4 SIRS versus Sepsis ICKG
Author: Marit Verboom
Date: 02/2022 - 05/2022

Main file for the prediction of SIRS versus sepsis on the PICU. The output of 
the algorithm shows whether a child on the PICU suffers from either SIRS or
sepsis  after congenital cardiac surgery with the use of a cardiobpulmonary 
bypass. Based on Random Forest algorithm.
"""

# Import modules
import numpy as np
import pandas as pd

# Import created functions
from main_preprocessing import main_preprocessing
from ROCcurves import ROC_mean
from rf_cv import rf_cv 
from bar_plots import bar_plots

#%% Pipeline6

# Preprocessing
features_cleaned, patients_sirs, sirs_crit = main_preprocessing('patients.csv', 12)

# manually add labels based on EPD
labels = pd.read_csv('labels.csv', sep = ';', names = ['Patient ID', 'Label'],
                     index_col=False)

# add labels (random until labels are known), 0: SIRS○, 1: Sepsis
features_cleaned['Label'] = labels['Label']

# Random Forest with 5-fold cross validation
score, sens, spec, tprs, aucs, important_features = rf_cv(features_cleaned)

# ROC curve
ROC_mean(tprs, aucs, 'ROC')

# Score
mean_auc = np.mean(aucs)
mean_acc = np.mean(score)
mean_sens = np.mean(sens)
mean_spec = np.mean(spec)

# Plot feature importance score
bar_plots(important_features, title='')
