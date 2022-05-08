# -*- coding: utf-8 -*-
"""
TM2.4 SIRS versus Sepsis
Author: Marit Verboom
Date: 02/2022 - 05/22
"""

import pandas as pd
import datetime
from time_after_surgery import admissiondate 
import numpy as np


def vitalsigns_pdms(vitals, patient_information):
    """
    Function to load .csv file containing vital parameters of all patients that 
    were once admitted to the PICU of the LUMC for the duration of their entire
    PICU stay. 
    
    Parameters
    ----------
    vitals: name of .csv file, 'ICKGsepsis.csv'
    patient_information: .csv file containing patient information, 'patients.csv'
    
    Returns
    -------
    patientfirst24hours: DataFrame containing all data per patient of the first
        24 hours of their stay
    patient_information: DataFrame containing patient information
    """
    # Load PDMS Data
    pdms_data = pd.read_csv(vitals, sep = ';', 
                            names = ['Nr', 'Patient ID', 'Datetime','HR', 'RR',
                                     'SpO2', 'SBP', 'DBP', 'MAP', 'Temp1',
                                     'Temp2', 'Temp rect', 'etCO2' ],
                            index_col=False)
    pdms_data = pdms_data.drop(columns='Nr')

    # keep all patients with CPB = 1 in patient_information
    patient_information = pd.read_csv(patient_information, sep = ';', 
                                      names = ['Patient ID', 'Gender',
                                               'Admissiondate', 'Cardio', 'OK',
                                               'CPB'], index_col=False)
    patient_information = patient_information.loc[patient_information['CPB'] == 1] 
    patient_information.reset_index(drop=True, inplace=True)

    # Keep data of patients that are in patient_information
    dataframekeep = pdms_data['Patient ID'].isin(patient_information['Patient ID'])
    dataframekeep = pdms_data[dataframekeep]
    dataframekeep.reset_index(drop=True, inplace=True)

    # Only keep data between 2019-07-21 - 2020-07-31 and entire 2021
    # Patients included in current study are selected between these timewindows
    dataframekeep['Datetime'] = pd.to_datetime(dataframekeep['Datetime'],
                                               format = '%d-%m-%Y %H:%M')
    dataframekeepfirst = dataframekeep.loc[(dataframekeep['Datetime'] >
                                            datetime.datetime(2019, 7, 21)) &
                                           (dataframekeep['Datetime'] <
                                            datetime.datetime(2020, 7, 31))]
    dataframekeepsecond = dataframekeep.loc[(dataframekeep['Datetime'] >
                                             datetime.datetime(2020, 12, 31)) &
                                            (dataframekeep['Datetime'] <
                                             datetime.datetime(2022, 1, 1))]
    dataframekeep = dataframekeepfirst.append(dataframekeepsecond)
    dataframekeep.reset_index(drop=True, inplace=True)

    # Add admissiondate to dataframe (time_after_surgery.py)
    pdms_dataframe_admission = admissiondate(dataframekeep, patient_information)

    # During admission (time_after_surgery.py)
    dataframeadmission = pdms_dataframe_admission.loc[(pdms_dataframe_admission['Datetime'] >
                                                       pdms_dataframe_admission['Admissiondate'] )]
    
    # Keep first 24h of data per patient = 24 * 60 = 1140 rows per patient
    patientsfirst24hours = dataframeadmission.groupby('Patient ID').head(1140)  
    patientsfirst24hours.reset_index(drop=True, inplace=True)
    
    return patientsfirst24hours, patient_information


def vitals_postsurgery(vitalsigns, hours):
    """
    Function that creates DataFrame containing data for x hours post-surgery.

    Parameters
    ----------
    vitalsigns : DataFrame containing all data per patient of the first
        24 hours of their stay
    hours : hours after surgery of moment of prediction

    Returns
    -------
    meanvitals : DataFrame containing mean of vitals at moment of prediction
        per patient.

    """
    parameters = ['HR', 'RR', 'Temp rect', 'SpO2', 'SBP', 'DBP', 'MAP', 'Temp1',
                  'etCO2']
    
    vitals_all = vitalsigns[['Patient ID', 'Datetime', 'Admissiondate', 'HR',
                             'RR', 'Temp rect', 'SpO2', 'SBP', 'DBP', 'MAP',
                             'Temp1', 'etCO2']] 
    
    # Convert admissiondate to datetime format
    vitals_all['Admissiondate'] = pd.to_datetime(vitals_all['Admissiondate'],
                                                 format = '%Y-%m-%d %H:%M:%S.%f')
    
    # Calculate difference between moment of measurement and admissiondate
    vitals_all['Difference'] = vitals_all['Datetime'] - vitals_all['Admissiondate']

    # Keep data of timewindow 2 hours before moment of prediction until moment
    # of prediction
    parameterhours = vitals_all.loc[(vitals_all['Difference'] >
                                     datetime.timedelta(hours=hours-2)) & 
                                    (vitals_all['Difference'] <
                                     datetime.timedelta(hours=hours))]
    
    # All patient IDs that are unique 
    patidunique = parameterhours['Patient ID'].unique()
    
    # Create new DataFrame with a row per patient    
    meanvitals = pd.DataFrame(patidunique, columns = ['Patient ID'])
       
    # For every vital parameter    
    for i in parameters: 
        meanvitals[i] = ''
        meanvital = []  
        # for every patient              
        for ptid in patidunique:
            # keep part of dataframe with data for patient
            keep = parameterhours.loc[parameterhours['Patient ID'] == ptid]
            keep.reset_index(drop=True, inplace=True)
            # create empty list for median of parameters
            med = []
            # For every 10 samples (=10 min), take median of the parameter
            # 2 hours of data, per 10 minutes = 120 minutes max
            for j in range(0, 120, 10):
                median = keep[i][j:j+9].median()
                med.append(median)
            # take mean of all median values and ignore NaN values    
            meanvital.append(np.nanmean(med)) 
        
        for k in range(len(meanvital)):
            meanvitals[i][k] = meanvital[k]
        
    return meanvitals
    
def all_vitals(vitalsigns, patient_information):
    """
    Function to calculate median parameter value per 10 minutes of data for 
    first 24 hours of PICU admission. The output can be used for the detection
    of SIRS criteria.

    Parameters
    ----------
    vitalsigns : DataFrame containing all data per patient of the first
        24 hours of their stay
    patient_information : patient_information: DataFrame containing patientinfo
    
    Returns
    -------
    medianvitals : DataFrame containing  median parameter value per 10 minutes
        per patient

    """
    parameters = ['HR', 'RR', 'Temp rect', 'SpO2', 'SBP', 'DBP', 'MAP',
                  'Temp1', 'etCO2']
    
    vitals_all = vitalsigns[['Patient ID', 'Datetime', 'Admissiondate', 'HR',
                             'RR', 'Temp rect', 'SpO2', 'SBP', 'DBP', 'MAP', 
                             'Temp1', 'etCO2']] 
    
    # Convert admissiondate to datetime format
    vitals_all['Admissiondate'] = pd.to_datetime(vitals_all['Admissiondate'],
                                                 format = '%Y-%m-%d %H:%M:%S.%f')
    vitals_all['Difference'] = vitals_all['Datetime'] - vitals_all['Admissiondate']
    
    # Calculate difference between moment of measurement and admissiondate
    parameterhours = vitals_all.loc[(vitals_all['Difference'] >
                                     datetime.timedelta(hours=1)) &
                                    (vitals_all['Difference'] <
                                     datetime.timedelta(hours=24))]
    
    # All patient IDs that are unique and sort in ascending number
    patidunique = parameterhours['Patient ID'].unique()
    patidunique = np.sort(patidunique) 
    
    # Create new DataFrame with 144 rows per patient
    # 24 hours, with 6 times 10 minutes per hour, 6 * 24 = 144
    medianvitals = pd.DataFrame(patidunique, columns = ['Patient ID'])
    medianvitals = pd.concat([medianvitals]*144, ignore_index=True)
    # Creating empty column for minute value
    medianvitals['Min'] = ''
    
    # initial count
    count = 0
    # for every 10 minutes in 24 hours, fill in minute values 
    for i in range(10, 1450, 10): #1450; 24 hours
        medianvitals['Min'][count:(count+len(patidunique))] = i
        count = count + len(patidunique)  
    
    # Sort DataFrame on patient ID and ascending minutes of stay
    medianvitals = medianvitals.sort_values(['Patient ID', 'Min'], ascending = (True, True))
    medianvitals.reset_index(drop=True, inplace=True)
              
    # For every vital parameter  
    for i in parameters: 
        medianvitals[i] = ''
        # inital count
        count = 0
        # for every patient
        for ptid in patidunique:
            # keep parameters of patient
            keep = parameterhours.loc[parameterhours['Patient ID'] == ptid]
            keep.reset_index(drop=True, inplace=True)
            med = []
            # For every 10 samples (=10 min), take median HR
            for j in range(0, 1440, 10):
                median = keep[i][j:j+9].median()
                med.append(median)
            # add 144 median values of patient to DataFrame    
            medianvitals[i][count:(count+144)] = med
            # modify count to new patient
            count = count + 144
        
    return medianvitals
  
def mean_vitals(vitals, patient_information, hours):
    """

    Parameters
    ----------
    vitals: name of .csv file, 'ICKGsepsis.csv'
    patient_information: .csv file containing patient information, 'patients.csv'
    hours : hours after surgery of moment of prediction

    Returns
    -------
    meanvital : DataFrame containing mean vitals per patient at moment
        of prediction
    medianvitals : DataFrame containing median vital value per patient per 10
        minutes of first 24 hours of stay at PICU

    """
    
    # Use created functions
    vitalsigns, patient_information = vitalsigns_pdms(vitals, patient_information)
    meanvitals = vitals_postsurgery(vitalsigns, hours) 
    medianvitals = all_vitals(vitalsigns, patient_information)
    
    return meanvitals, medianvitals
    





   


