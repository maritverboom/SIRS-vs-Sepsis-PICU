# -*- coding: utf-8 -*-
"""
TM2.4 SIRS versus Sepsis ICKG
Author: Marit Verboom
Date: 02/2022 - 05/2022
"""
# Load modules
import pandas as pd

# Load created functions
from time_after_surgery import time_after_surgery
from lab_features import feature_table
from cleaning import lab_cleaning
from pdmsdata import mean_vitals
from SIRScriteria import sirs_table, sirs_criteria


def main_preprocessing(patientinfo, hours):
    
    
    """
    Function for the preprocessing of laboratory data and vital parameters 
    derived from eiter LUMC dataplaform or PDMS.

    Parameters
    ----------
    patientinfo : Name of .csv file containing patientinfo with columns Patient
        ID, Gender, Admissiondate, Cardio, OK, CPB.
    hours : hours after admission to the PICU for moment of prediction. 

    Returns
    -------
    features_cleaned: DataFrame containing all feature values per patient ID 
        after preprocessing
    patients_sirs: DataFrame containing all patient IDs of patients that meet
        SIRS criteria 

    """

    # Load patient information
    patient_information = pd.read_csv(patientinfo, sep = ';',
                                      names = ['Patient ID', 'Gender',
                                               'Admissiondate', 'Cardio', 'OK',
                                               'CPB'], index_col=False)
    # Keep patients with CPB
    patient_information = patient_information.loc[patient_information['CPB'] == 1] 
    patient_information.reset_index(drop=True, inplace=True)
    
    # Load laboratory parameters 
    lab_hematologie = pd.read_csv('Lab_Hematologie.csv', sep = ';',
                                  names = ['Patient ID', 'Measurement',
                                           'Value' , 'Unit', 'Time'])
    lab_bloedgas = pd.read_csv('Lab_Bloedgas.csv',  sep = ';',
                               names = ['Patient ID', 'Measurement', 'Value' ,
                                        'Unit', 'Time'])
    lab_chemie = pd.read_csv('Lab_Chemie.csv',  sep = ';',
                             names = ['Patient ID', 'Measurement', 'Value' ,
                                      'Unit', 'Time'])
    
    
    # Create dataframes containing only patients with patient ID in 
    # patient_information and add column with time after surgery
    lab_chemie = time_after_surgery(lab_chemie, patient_information)
    lab_bloedgas = time_after_surgery(lab_bloedgas, patient_information)
    lab_hematologie = time_after_surgery(lab_hematologie, patient_information)
    
    
    # Import and preprocessing of vital parameters from PDMS (pdmsdata.py)
    features_vitals, medianvitals = mean_vitals('ICKGsepsis.csv',
                                                'patients.csv', hours)

     
    # Create featuretable for moment of prediction (lab_features.py)
    features_lab = feature_table(lab_chemie, lab_hematologie, lab_bloedgas,
                                 patient_information, hours)
    features_lab.reset_index(inplace=True)
    
    # Create table with sirs values of first 24 hours of patient 
    # (SIRScriteria.py)
    sirstable = sirs_table(medianvitals, lab_hematologie, patient_information)
    
    # Which patients to include (patients that meet SIRS criteria 
    # (SIRScriteria.py))
    sirs, patients_sirs = sirs_criteria(sirstable)
    
    # Keep data of patients that do have data in features_vitals
    features_lab = features_lab.loc[features_lab['Patient ID'].isin(features_vitals['Patient ID'])]
      
    # Add vital parameters and features_lab together to feature table
    features = pd.merge(features_lab, features_vitals, on='Patient ID', how='outer')
    
    # Remove patients and features with too many missing values (cleaning.py)
    features_cleaned = lab_cleaning(features)
    
    # Patients with SIRS that are in features_cleaned
    patients_sirs = patients_sirs.loc[patients_sirs['Patient ID'].isin(features_cleaned['Patient ID'])]
    patients_sirs.reset_index(drop=True, inplace=True)

    # Only keep features of patients with sirs
    features_cleaned = features_cleaned.loc[features_cleaned['Patient ID'].isin(patients_sirs['Patient ID'])]
    features_cleaned = features_cleaned.sort_values(by=['Patient ID'])
    features_cleaned.reset_index(drop=True, inplace=True)
        
    return features_cleaned, patients_sirs, sirs

