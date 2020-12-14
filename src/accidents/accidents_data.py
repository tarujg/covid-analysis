import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

isRushHour = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 
              6: 2, 7: 2, 8: 2, 9: 2, 10: 1, 11: 1,
              12: 1, 13: 1, 14: 2, 15: 2, 16: 2, 17: 2,
              18: 1, 19: 1, 20: 1, 21: 0, 22: 0, 23: 0}

def ingestion_and_clean(raw_fp = '../data/accidents/US_Accidents_June20.csv'):
    """
    Parameters
    ----------
    raw_fp : string
        Raw filepath of Complete US Accidents Dataset CSV file
    
    Returns
    -------
    Filters and keeps only San Diego County Data
    """
    assert os.path.exists(raw_fp),"Raw file exists"
    assert raw_fp[-3:] == "csv", "File of type csv allowed"

    df = pd.read_csv(raw_fp)
    df = filter_data(df)
    df = compute_features(df)
    return df

def filter_data(df):
    '''
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame of Complete US Accidents Dataset
    
    Returns
    -------
    Filters and keeps only San Diego County Data
    '''
    assert ('County' in df.columns),"County Entry doesn't exist in df"

    remove_cols = ['Astronomical_Twilight','Nautical_Twilight','Precipitation(in)', 'Wind_Chill(F)', 
                          'Number','End_Lng','End_Lat','Civil_Twilight','Source', 'ID','Street', 'Side',  
                          'Country', 'Timezone', 'Airport_Code','Distance(mi)','Description','State']

    assert (remove_col in df.columns for remove_col in remove_cols), "Column Doesn't exist"
    df = df.drop(columns=remove_cols)
    return df[df['County']=='San Diego']

def compute_features(df):
    '''
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame of good data
    
    Returns
    -------
    Updated df with new columns
    '''
    list_keys = ['Start_Time','End_Time','Hour','Zipcode','Start_Lat','Start_Lng']
    assert (key in df.columns for key in list_keys),"County Entry doesn't exist in df"


    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    df['End_Time'] = pd.to_datetime(df['End_Time'])
    df['Month'] = df['Start_Time'].dt.month
    df['Year'] = df['Start_Time'].dt.year
    df['Hour'] = df['Start_Time'].dt.hour
    df['Weekday'] = df['Start_Time'].dt.weekday
    df['Duration'] = (df['End_Time'] - df['Start_Time']).dt.total_seconds()/60
    df['RushHour'] = df['Hour'].map(RushHour(isRushHour))
    df['Zipcode'] = df['Zipcode'].apply(lambda x: x if len(x) == 5 else x.split('-')[0])

    df = df.rename(columns={'Start_Lat': 'Latitude', 'Start_Lng': 'Longitude'})
    return df

def RushHour(isRushHour, labels = ["Low Traffic", "Normal Traffic", "Rush Hour"]):
    '''
    Parameters
    ----------
    isRushHour: dict
        Mapping of hour of the day to level of rush
    labels: list
        String mapping to level of rush

    Returns
    -------
    Maps level of rush (i) to label[i]
    '''
    assert isinstance(isRushHour,dict), "Rush Hour is a dictionary"
    assert all(0 <= v <= len(labels) for v in isRushHour.values()),"Rush Hour Dictionary has less labels"
    for k,v in list(isRushHour.items()):
        isRushHour[k] = labels[v]

    return isRushHour