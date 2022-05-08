# -*- coding: utf-8 -*-
"""
TM2.4 SIRS versus Sepsis
Author: Marit Verboom
Date: 02/2022 - 05/22
"""

import pandas as pd


def feature_table_chemie(dataframe, patient_information, hours):
    
    """
    Parameters
    ----------
    dataframe: DataFrame containing parametervalues per patient ID of measurements during
    PICU stay, including time of measurement after admittance to the PICU in hours.
    
    patient_information: patientinfo with columns Patient ID, Gender,
    Admissiondate, Cardio, OK, CPB.
        
    hours:  hours after admittance to the PICU for moment of prediction.
        
    Returns
    -------
    features: Dataframe containing maximal value per feature in first x hours after admittance to the PICU
    
    """
        
    dataframe = dataframe
    
    # Only keep values of first x hours of opname
    dataframe = dataframe.loc[dataframe['Difference'] <= hours]
    dataframe.reset_index(drop=True, inplace=True)
    
    # Create DataFrame for features
    ptid = patient_information['Patient ID']
    columns = ['Patient ID', 'CRP', 'Chloride', 'Calcium', 'Magnesium',
               'Fosfaat', 'Kreatinine', 'Ureum', 'Albumine']
    features = pd.DataFrame(columns=columns)
    features['Patient ID'] = ptid
    count = 0
    
    for i in ptid:
        keep = dataframe.loc[dataframe['Patient ID'] == i]
        
        # CRP
        CRP = keep.loc[keep['Measurement'].isin(['C-Reaktief Proteïne', 'C-Reactief Proteine'])]
        CRP.reset_index(drop=True, inplace=True)
        features['CRP'][count] = CRP['Value'].max()
        
        # Chloride
        chloride = keep.loc[keep['Measurement'].isin(['Chloride', 'Chloride (art)', 'Chloride(arterieel)'])]
        chloride.reset_index(drop=True, inplace=True)
        features['Chloride'][count] = chloride['Value'].max()
        
        # Calcium
        calcium = keep.loc[keep['Measurement'].isin(['Calcium', 'Calcium (art)', 'Calcium (arterieel)'])]
        calcium.reset_index(drop=True, inplace=True)
        features['Calcium'][count] = calcium['Value'].max()
        
        # Magnesium
        magnesium = keep.loc[keep['Measurement'].isin(['Magnesium', 'Magnesium (art)', 'Magnesium (arterieel)'])]
        magnesium.reset_index(drop=True, inplace=True)
        features['Magnesium'][count] = magnesium['Value'].max()
        
        # Fosfaat
        fosfaat = keep.loc[keep['Measurement'].isin(['Fosfaat', 'Fosfaat, anorganisch', 'Fosfaat (arterieel)'])]
        fosfaat.reset_index(drop=True, inplace=True)
        features['Fosfaat'][count] = fosfaat['Value'].max()
        
        # Kreatinine
        kreatinine = keep.loc[keep['Measurement'].isin(['Kreatinine', 'Kreatinine (art)', 'Kreatinine (arterieel)'])]
        kreatinine.reset_index(drop=True, inplace=True)
        features['Kreatinine'][count] = kreatinine['Value'].max()
        
        # Ureum
        ureum = keep.loc[keep['Measurement'].isin(['Ureum', 'Ureum (art)', 'Ureum (arterieel)'])]
        ureum.reset_index(drop=True, inplace=True)
        features['Ureum'][count] = ureum['Value'].max()
        
        #Albumine
        albumine = keep.loc[keep['Measurement'].isin(['Albumine', 'Albumine (art)', 'Albumine (arterieel)'])]
        albumine.reset_index(drop=True, inplace=True)
        features['Albumine'][count] = albumine['Value'].max()
        
        count = count + 1
            
    return features


def feature_table_hematologie(dataframe, patient_information, hours):
    
    """
    Parameters
    ----------
    dataframe: DataFrame containing parametervalues per patient ID of measurements during
    PICU stay, including time of measurement after admittance to the PICU in hours.
    
    patient_information: patientinfo with columns Patient ID, Gender,
    Admissiondate, Cardio, OK, CPB.
        
    hours:  hours after admittance to the PICU for moment of prediction.
        
    Returns
    -------
    features: Dataframe containing maximal value per feature in first x hours after admittance to the PICU
    
    """
    dataframe = dataframe
    
    # Only keep values of first x hours of opname
    dataframe = dataframe.loc[dataframe['Difference'] <= hours]
    dataframe.reset_index(drop=True, inplace=True)
    
    # Create DataFrame for features
    ptid = patient_information['Patient ID']
    columns = ['Patient ID', 'Hemoglobine', 'Hematocriet', 'Erytrocyten', 'Trombocyten',
               'Leukocyten', 'Lymfocyten']
    features = pd.DataFrame(columns=columns)
    features['Patient ID'] = ptid
    count = 0
    
    #key = ['Hemoglobine', 'Hematocriet', 'Erytrocyten', 'Trombocyten',
           #'Leukocyten', 'Lymfocyten']
    
    for i in ptid:
        keep = dataframe.loc[dataframe['Patient ID'] == i]
        
        # Hemoglobine
        hb  = keep.loc[keep['Measurement'].isin(['Hemoglobine', 'Hemoglobine (art)', 'Hemoglobine (arterieel)'])]
        hb.reset_index(drop=True, inplace = True)
        features['Hemoglobine'][count] = hb['Value'].min()
        
        # Hematocriet
        hema  = keep.loc[keep['Measurement'].isin(['Hematocriet', 'Hematocriet (art)', 'Hematocriet (arterieel)'])]
        hema.reset_index(drop=True, inplace = True)
        features['Hematocriet'][count] = hema['Value'].min()
        
        # Erytrocyten
        ery = keep.loc[keep['Measurement'].isin(['Erytrocyten', 'Erytrocyten (art)', 'Erytrocyten (arterieel'])]
        ery.reset_index(drop=True, inplace=True)
        features['Erytrocyten'][count] = ery['Value'].min()
        
        # Trombocyten
        trombo = keep.loc[keep['Measurement'].isin(['Trombocyten', 'Trombocyten (art)', 'Trombocyten (arterieel)'])]
        trombo.reset_index(drop=True, inplace=True)
        features['Trombocyten'][count] = trombo['Value'].min()
        
        # Leukocyten
        leuko = keep.loc[keep['Measurement'].isin(['Leukocyten', 'Leukocyten (art)', 'Leukocyten (arterieel)'])]
        leuko.reset_index(drop=True, inplace=True)
        features['Leukocyten'][count] = leuko['Value'].max()
        
        # Lymfocyten
        lymfo = keep.loc[keep['Measurement'].isin(['Lymfocyten', 'Lymfocyten (art)', 'Lymfocyten (arterieel'])]
        lymfo.reset_index(drop=True, inplace=True)
        features['Lymfocyten'][count] = lymfo['Value'].max()
                
        count = count + 1
        
    return features

def feature_table_bloedgas(dataframe, patient_information, hours):
    """
    Parameters
    ----------
    dataframe: DataFrame containing parametervalues per patient ID of measurements during
    PICU stay, including time of measurement after admittance to the PICU in hours.
    
    patient_information: patientinfo with columns Patient ID, Gender,
    Admissiondate, Cardio, OK, CPB.
        
    hours:  hours after admittance to the PICU for moment of prediction.
        
    Returns
    -------
    features: Dataframe containing maximal value per feature in first x hours after admittance to the PICU
    
    """
    dataframe = dataframe
    
    # Only keep values of first x hours of opname
    dataframe = dataframe.loc[dataframe['Difference'] <= hours]
    dataframe.reset_index(drop=True, inplace=True)
    
    # Create DataFrame for features
    ptid = patient_information['Patient ID']
    columns = ['Patient ID', 'pH', 'pCO2', 'pO2', 
               'sO2', 'SpO2', 'Natrium', 'Kalium', 'Chloride',
               'Glucose', 'Lactaat']
    features = pd.DataFrame(columns=columns)
    features['Patient ID'] = ptid
    
    count = 0
       
    for i in ptid:
        keep = dataframe.loc[dataframe['Patient ID'] == i]
        
        # pH
        pH = keep.loc[keep['Measurement'].isin(['pH', 'pH (art)', 'pH (arterieel)'])]
        pH.reset_index(drop=True, inplace=True)
        features['pH'][count] = pH['Value'].max()
        
        # pCO2
        pCO2 = keep.loc[keep['Measurement'].isin(['pCO2', 'pCO2 (art)', 'pCO2 (arterieel)'])]
        pCO2.reset_index(drop=True, inplace=True)
        features['pCO2'][count] = pCO2['Value'].max()
        
        # pO2
        pO2 = keep.loc[keep['Measurement'].isin(['pO2', 'pO2 (art)', 'pO2 (arterieel)'])]
        pO2.reset_index(drop=True, inplace=True)
        features['pO2'][count] = pO2['Value'].max()
        
        # sO2
        sO2 = keep.loc[keep['Measurement'].isin(['sO2', 'sO2 (art)', 'sO2 (arterieel)'])]
        sO2.reset_index(drop=True, inplace=True)
        features['sO2'][count] = sO2['Value'].max()
        
        # SpO2
        SpO2 = keep.loc[keep['Measurement'].isin(['SpO2', 'SpO2 (art)', 'SpO2 (arterieel)'])]
        SpO2.reset_index(drop=True, inplace=True)
        features['SpO2'][count] = SpO2['Value'].max()
        
        
        # Natrium
        Natrium = keep.loc[keep['Measurement'].isin(['Natrium', 'Natrium (art)', 'Natrium (arterieel)'])]
        Natrium.reset_index(drop=True, inplace=True)
        features['Natrium'][count] = Natrium['Value'].max()
        
        # Kalium
        Kalium = keep.loc[keep['Measurement'].isin(['Kalium', 'Kalium (art)', 'Kalium (arterieel)'])]
        Kalium.reset_index(drop=True, inplace=True)
        features['Kalium'][count] = Kalium['Value'].max()
        
        # Chloride
        Chloride = keep.loc[keep['Measurement'].isin(['Chloride', 'Chloride (art)', 'Chloride (arterieel)'])]
        Chloride.reset_index(drop=True, inplace=True)
        features['Chloride'][count] = Chloride['Value'].max()
        
        # Glucose
        Glucose = keep.loc[keep['Measurement'].isin(['Glucose', 'Glucose (art)', 'Glucose (arterieel)'])]
        Glucose.reset_index(drop=True, inplace=True)
        features['Glucose'][count] = Glucose['Value'].max()
        
        # Lactaat
        Lactaat = keep.loc[keep['Measurement'].isin(['Lactaat', 'Lactaat (art)', 'Lactaat (arterieel)'])]
        Glucose.reset_index(drop=True, inplace=True)
        features['Lactaat'][count] = Lactaat['Value'].max()
        
        count = count + 1
        
    return features  

def feature_table(labchem, labhemat, labbloedgas, patient_information, hours):
    """
    Function to create a DataFame of all laboratory parameters per patient at 
    moment of desired SIRS versus sepsis prediction

    Parameters
    ----------
    labchem : DataFrame with  laboratory chem parameters per patient
    labhemat : DataFrame containing laboratory hemat parameters per patient
    labbloedgas : DataFrame containing laboratory bloodgas parameters per patient
    patient_information : DataFrame containing patient information
    hours : hours after admittance to the PICU for moment of prediction
    
    Returns
    -------
    features : DataFrame containing all laboratory parameters per patient at 
        moment of prediciton.

    """
    
    #Use created functions
    labchem = feature_table_chemie(labchem, patient_information, hours)
    labhemat = feature_table_hematologie(labhemat, patient_information, hours)
    labbloedgas = feature_table_bloedgas(labbloedgas, patient_information, hours)
    
    
    labbloedgas = labbloedgas.set_index('Patient ID')   
    labchem = labchem.set_index('Patient ID')
    labhemat = labhemat.set_index('Patient ID')  
    
    # Add dataframes together
    dfx = pd.concat([labbloedgas, labchem], axis = 1)
    features = pd.concat([dfx, labhemat], axis=1)
              
    return features
