# -*- coding: utf-8 -*-
"""
TM2.4 SIRS versus Sepsis
Author: Marit Verboom
Date: 02/2022 - 05/22
"""

from datetime import datetime
import numpy as np 


def selectpatients(dataframe, patient_information):
    """
    Function to keep rows of a dataframe with a patient ID that is present in
    another dataframe.
    
    Parameters
    ----------
    dataframe : DataFrame containing parameter values per patient ID, including
        time of measurement.
    patient_information : Dataframe containing patient ID and opnamedatum.

    Returns
    -------
    dataframekeep : DataFrame based on original 'dataframe', containing only 
        data from patient IDs that are present in 'patient_information'

    """
    dataframe = dataframe
    patient_id = patient_information
    
    # Find rows where patient ID is in patient_information Dataframe
    dataframekeep = dataframe['Patient ID'].isin(patient_id['Patient ID'])      
    dataframekeep = dataframe[dataframekeep]                                    
    dataframekeep.reset_index(drop=True, inplace=True)                         
    return dataframekeep
            
          

def admissiondate(dataframe, patient_information):
    """
    Function to add date of admission to a dataframe (derived from 
                                                      patient_information)

    Parameters
    ----------
    dataframe : DataFrame containing parameter values per patient ID, 
        including time of measurement.
    patient_information : Dataframe containing patient ID and date of admission.

    Returns
    -------
    dataframe : DataFrame with added column 'Opnamedatum'

    """
    # Create new column for date of admittance to the PICU
    dataframe = dataframe
    dataframe['Admissiondate'] = ''                                             
    patient_information = patient_information
    count = 0

    # Add date of admission from patient_information to dataframe per patient ID
    for i in patient_information['Patient ID']:
        index = np.where(dataframe['Patient ID'] == i)
        for x in index:
            dataframe['Admissiondate'][x] = patient_information['Admissiondate'][count]
        count = count + 1
        
    return dataframe


def duringadmission(dataframe):
    """
    Function to keep only parameters that were measured during admittance to 
    the PICU instead of all measured data during every hospital visit.
    
    Parameters
    ----------
    dataframe: DataFrame containing parameter values per patient ID
    
    Returns
    -------
    dataframe: DataFrame containing only parameters measured during PICU stay 
        per patient ID
    """
    
    # Keep where time of measurement is after date of admission
    keep = np.where(dataframe['Time'] > dataframe['Admissiondate'])[0]         
    keep = dataframe.index.isin(keep)
    dataframe = dataframe[keep]
    dataframe.reset_index(drop=True, inplace=True)
    
    return dataframe


def timeaftersurgery(dataframe):
    """
    Function that calculates the time after surgery based on timestamps from 
    parameter measurement and date and time of admission.
    
    Parameters
    ----------
    dataframe: DataFrame containing parameters values per patient ID,
        including time of measurement and time of admittance to the PICU
        
    Returns
    -------
    dataframe: Same as input parameter, with added column 'Difference' 
        containing the time of measurement after admittance to the PICU in hours.
    """
    
    date_format_str = '%Y-%m-%d %H:%M:%S.%f'
    dataframe['Difference'] = ''

    for i in range(len(dataframe)):
        start = datetime.strptime(dataframe['Admissiondate'][i], date_format_str) # Starttime: date and time of admission
        end = datetime.strptime(dataframe['Time'][i], date_format_str)            # Endtime: date and time of measurement
        diff = end-start                                                          # Difference between start- and endtime
        diffhours = diff.total_seconds()/3600                                     # Convert to hours
        dataframe['Difference'][i] = diffhours                                    # Add to DataFrame 
    return dataframe


def time_after_surgery(dataframe, patient_information):
    """
    Function to calculate time after admittance to the PICU for measurements of
    parameters.
    
    Parameters
    ---------
    dataframe : DataFrame containing parameter values per patient ID, including
        time of measurement.
    patient_information : Dataframe containing patient ID and opnamedatum.

    Returns
    -------
    data: DataFrame containing parametervalues per patient ID of measurements
        during PICU stay, including time of measurement after admittance to the
        PICU in hours.
    """
    
    # Rename input variables
    data = dataframe
    ptinfo = patient_information
    
    # Use all created functions
    data = selectpatients(data, ptinfo)
    data = admissiondate(data, ptinfo)
    data = duringadmission(data)
    data = timeaftersurgery(data)
    
    return data