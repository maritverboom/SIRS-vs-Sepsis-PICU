# -*- coding: utf-8 -*-
"""
TM2.4 SIRS versus Sepsis
Author: Marit Verboom
Date: 02/2022 - 05/22
"""

import pandas as pd
import numpy as np

def sirs_table(medianvitals, lab_hematologie, patient_information):
    """
    Function to create DataFrame with per patient values for the parameters
    that are used in the SIRS criteria (HR, RR, Temp rect & leukocytes)

    Parameters
    ----------
    medianvitals : DataFrame containing  median parameter value per 10 minutes
        per patient
    lab_hematologie : DataFrame containing all laboratory parameters (hematology)
        per patient for their entire PICU stay
    patient_information : DataFrame containing patient information

    Returns
    -------
    sirsparam : DataFrame containing parameter values (median for vitals) per 
        10 minutes

    """
    vital = medianvitals[['Patient ID', 'Min', 'HR', 'RR', 'Temp rect']]    
    leuko = lab_hematologie.loc[lab_hematologie['Measurement'] == 'Leukocyten']
    leuko = leuko.loc[leuko['Difference'] < 24]
    
    # To find patients with both vital signs and leukocyten
    # all patients with leukos
    ptidunique = leuko['Patient ID'].unique()
    # all vital signs of patients with leukos
    sirsparam = vital.loc[vital['Patient ID'].isin(ptidunique)] 
    
    # Unique patients
    ptidunique = pd.DataFrame(ptidunique, columns=['Patient ID'])
    ptidunique = ptidunique.loc[ptidunique['Patient ID'].isin(sirsparam['Patient ID'])]

    
    # Add leuko to vitals
    sirsparam['Leuko'] = '' 
    sirsparam.reset_index(drop=True, inplace=True)
    
    # Add date of birth to DataFrame
    birthdate = pd.read_csv('birthdate.csv', sep=';', names = ['Patient ID',
                                                               'Birthdate'],
                            index_col=False)
    birthdate = birthdate.loc[birthdate['Patient ID'].isin(ptidunique['Patient ID'])]
    birthdate = birthdate.sort_values(['Patient ID'], ascending = True)
    birthdate.reset_index(drop=True, inplace=True)
    # To datetime format
    birthdate['Birthdate'] = pd.to_datetime(birthdate['Birthdate'],
                                            format = '%Y-%m-%d %H:%M:%S.%f')

    
    # Add date of admission to DataFrame
    adm = patient_information.loc[patient_information['Patient ID'].isin(ptidunique['Patient ID'])] #admission date of patients in ptunique
    adm = adm[['Patient ID', 'Admissiondate']]
    adm = adm.sort_values(['Patient ID'], ascending = True)
    adm.reset_index(drop=True, inplace=True)
    # To datetime format
    adm['Admissiondate'] = pd.to_datetime(adm['Admissiondate'],
                                          format = '%Y-%m-%d %H:%M:%S.%f')

       
    # Calculate age of patients in days
    age = pd.DataFrame(ptidunique, columns=['Patient ID'])
    age['Age'] =  adm['Admissiondate'] - birthdate['Birthdate']
    sirsparam['Age'] = ''
    
    # Add age of patient to sirsparam
    # For every patient
    for ptid in ptidunique['Patient ID']:
        # get index where patient is in DataFrame
        idx = sirsparam.index[sirsparam['Patient ID'] == ptid]
        age1 = age.loc[age['Patient ID'] == ptid]
        age2 = age1['Age']
        age2.reset_index(drop=True, inplace=True)
        age2 = age2.to_frame()
        start = idx[0]
        end = idx[-1]
        # Add age of patient to every row of specific patient
        sirsparam['Age'][start:end] = age2['Age'][0]
        
    # Add leuko to DataFrame, based on time of measurement
    leuko.reset_index(drop=True, inplace=True)
    leuko['Difference'] = leuko['Difference']*60 # to minutes
    ptidunique = leuko['Patient ID'].unique()
    
    # for every patient
    for ptid in ptidunique:
        pt_rows = leuko.loc[leuko['Patient ID'] == ptid]
        pt_rows.reset_index(drop=True, inplace=True)
        # get index where patient is in DataFrame
        idx = sirsparam.index[sirsparam['Patient ID'] == ptid]
        # for every index
        for j in idx: 
            for i in range(len(pt_rows['Patient ID'])):
                # check whether time of measurement leukocytes is before time
                # in DataFrame. If not, go to next measurement of leukocytes.
                if sirsparam['Min'][j] > pt_rows.at[i, 'Difference']:
                    # fill in leukocyte value in DataFrame
                    leuko_val = pt_rows.at[i, 'Value']
                    sirsparam['Leuko'][j] = leuko_val
                    
    return sirsparam


def sirs_criteria(sirstable):
    """
    Function to determine which patients meet SIRS criteria based on HR, RR, 
    rectal temperature and leukocytes (corrected for age).

    Parameters
    ----------
    sirstable : DataFrame containing parameter values (median for vitals) per 
        10 minutes

    Returns
    -------
    sirs : DataFrame with scoring per patient
    patients_sirs : DataFrame containing patient ID of every patient that meets
        SIRS criteria

    """
    
    patients = sirstable
    
    # Where patients age is not empty
    patients = patients.loc[patients['Age'].notnull()]
    
    #replace empty strings with NaN
    patients = patients.replace(r'^\s*$', np.nan, regex=True) 
    patients = patients[patients['Age'].notna()]
    patients.reset_index(drop=True, inplace=True)
    
    # SIRS criteria
    # normal values per age group
    normval = np.array([[7, 100, 180, 50, 0, 34, 59],
                        [31, 100, 180, 40, 5, 19.5, 79],
                       [730, 90, 180, 34, 5, 17.5, 75],
                       [1825, 0, 140, 22, 6, 15.5, 74],
                       [4380, 0, 130, 18, 4.5, 13.5, 83],
                       [6570, 0, 110, 14, 4.5, 11, 90]])
    criteria = pd.DataFrame(normval, columns=['Age', 'Heartrate lower',
                                              'Heartrate upper', 'Resprate',
                                              'Leuko lower', 'Leuko upper',
                                              'SBP'])
    # Age of patient to timedelta format (in days)
    criteria['Age'] = pd.to_timedelta(criteria['Age'], unit='d')
    
    # Create empty DataFrame with patient per row
    sirs = patients['Patient ID']
    sirs = pd.Series.to_frame(sirs)
    sirs['Temp rect'] = ''
    sirs['Leuko'] = ''
    sirs['HR'] = ''
    sirs['RR'] = ''
    sirs['Sum'] = '' 
    sirs['Label'] = '' 
    
    # for every patient
    for i in range(len(patients)):
        # if patient younger than 7 days old
        if patients['Age'][i] < criteria['Age'][0]: 
            if patients['Temp rect'][i] < 36.0 or patients['Temp rect'][i] > 38.5:
                sirs['Temp rect'][i] = 1
            if patients['Leuko'][i] < criteria['Leuko lower'][0] or patients['Leuko'][i] > criteria['Leuko upper'][0]:
                sirs['Leuko'][i] = 1
            if patients['HR'][i] < criteria['Heartrate lower'][0] or patients['HR'][i] > criteria['Heartrate upper'][0]:
                sirs['HR'][i] = 1
            if patients['RR'][i] > criteria['Resprate'][0]:
                sirs['RR'][i] = 1
                
        # if patient in oldest age group        
        elif patients['Age'][i] > criteria['Age'][5]:
            if patients['Temp rect'][i] < 36.0 or patients['Temp rect'][i] > 38.5:
                sirs['Temp rect'][i] = 1
            if patients['Leuko'][i] < criteria['Leuko lower'][5] or patients['Leuko'][i] > criteria['Leuko upper'][5]:
                sirs['Leuko'][i] = 1
            if patients['HR'][i] < criteria['Heartrate lower'][5] or patients['HR'][i] > criteria['Heartrate upper'][5]:
                sirs['HR'][i] = 1
            if patients['RR'][i] > criteria['Resprate'][5]:
                sirs['RR'][i] = 1
        
        else:
            for j in range(1,5,1):
                # check patients age group
                if patients['Age'][i] > criteria['Age'][j] and patients['Age'][i] < criteria['Age'][j+1]:
                    if patients['Temp rect'][i] < 36.0 or patients['Temp rect'][i] > 38.5:
                        sirs['Temp rect'][i] = 1
                    if patients['Leuko'][i] < criteria['Leuko lower'][j] or patients['Leuko'][i] > criteria['Leuko upper'][j]:
                        sirs['Leuko'][i] = 1
                    if patients['HR'][i] < criteria['Heartrate lower'][j] or patients['HR'][i] > criteria['Heartrate upper'][j]:
                        sirs['HR'][i] = 1
                    if patients['RR'][i] > criteria['Resprate'][j]:
                        sirs['RR'][i] = 1
  
    # Replace empty values with NaN value and then to 0
    sirs = sirs.replace(r'^\s*$', np.nan, regex=True)
    sirs = sirs.fillna(0)
    
    # Take sum of sirscriteria 
    sirs['Sum'] = sirs['Temp rect'] + sirs['Leuko'] + sirs['HR'] + sirs['RR']
    
    # If sum is greater than 1 and at least on of leuko or temp rect is 
    # abnormal, patient meets SIRS criteria
    sirsyes = sirs[sirs.Sum >= 1] 
    sirsyes = sirsyes[(sirsyes['Leuko'] == 1) | (sirsyes['Temp rect'] == 1)]
    
    # Get patients that meet SIRS criteria
    patients_sirs = sirsyes['Patient ID'].unique()
    patients_sirs = pd.DataFrame(patients_sirs, columns=['Patient ID'])
   
    return sirs, patients_sirs
            
            