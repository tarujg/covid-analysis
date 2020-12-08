# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 16:57:21 2020

@author: 77243
"""

import pandas as pd
import numpy as np
from math import isnan
import matplotlib.pyplot as plt

month_enum = ["Jan","Feb","Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
selected_sites = ["CHULA VISTA", "EL CAJON LES", "KEARNY MESA", "OTAY MESA DVN", "PENDLETON"]

def get_days(month):
    '''
    :Purpose: return corresponding days of a month from month name abbreviation
    :prams: month
    :type: str
    :return: int
    '''
    days_enum = {"Jan" : 31,
                  "Feb" : 28,
                  "Mar" : 31,
                  "Apr" : 30,
                  "May" : 31,
                  "Jun" : 30, 
                  "Jul" : 31,
                  "Aug" : 31,
                  "Sep" : 30,
                  "Oct" : 31,
                  "Nov" : 30,
                  "Dec" : 31}
    return range(2, days_enum[month] + 1)

def month_to_num(month):
    '''
    :Purpose: return corresponding month number in str from month name abbreviation
    :prams: month
    :type: str
    :return: str
    '''
    num_enum = {"Jan" : "01",
                  "Feb" : "02",
                  "Mar" : "03",
                  "Apr" : "04",
                  "May" : "05",
                  "Jun" : "06", 
                  "Jul" : "07",
                  "Aug" : "08",
                  "Sep" : "09",
                  "Oct" : "10",
                  "Nov" : "11",
                  "Dec" : "12"}
    return num_enum[month]

def normalize_days(day):
    '''
    :Purpose: return month day number in 2 digits 
    :prams: day
    :type: int
    :return: str
    '''
    if day >= 10:
        return str(day)
    else:
        return "0" + str(day)

def get_features(d, selected_sites, year):
    '''
    :Purpose: get all features from a CSV file in a given year
    :prams: d
    :type: CSV file
    :return: dict
    :prams: selected_sites
    :type: list of str
    :prams: year
    :type: int
    :return: dict
    '''
    features = {}
    visited_sites = 0
    curr_info = {}
    curr_param = ""
    for index, data in d.iterrows():
        if data["Parameter"] != curr_param:
            if visited_sites < 5:
                curr_info = {}
            else:
                features[curr_param] = curr_info
            curr_param = data["Parameter"]
            visited_sites = 0
            curr_info = {}
            continue 
        if year == 2019:
            if data["SiteName"] not in selected_sites:
                continue
            curr_info[data["SiteName"]] = {"Avg":data["Avg"], "Max":data["Max"]}
            visited_sites += 1
        if year == 2020:
            if data["Site Name"] not in selected_sites:
                continue
            curr_info[data["Site Name"]] = {"Avg":data["Avg"], "Max":data["Max"]}
            visited_sites += 1
        #print(curr_info)
    return features

def get_2019_features(month_enum):
    '''
    :Purpose: get all features from CSV files in 2019
    :prams: month_enum
    :type: list of str
    :return: list
    '''
    features_2019 = []
    for month in month_enum[2:10]:
        for day in get_days(month):
            month_num = month_to_num(month)
            file_path = "http://jtimmer.digitalspacemail17.net/data/2019/" + month +"/yesterday_2019" + month_to_num(month) + normalize_days(day) +".CSV"
            csv_data = pd.read_csv(file_path, header = 4, encoding = "ISO-8859-1")
            d = csv_data[["Parameter", "SiteName", "Avg", "Max", "Hr. of Max"]]
            d["Parameter"].fillna(method = 'ffill',inplace = True)
            features = get_features(d, selected_sites, 2019)
            features_2019.append(features)
    return features_2019

def get_2020_features(month_enum):
    '''
    :Purpose: get all features from CSV files in 2020
    :prams: month_enum
    :type: list of str
    :return: list
    '''
    features_2020 = []
    for month in month_enum[2:9]:
        for day in get_days(month):
            month_num = month_to_num(month)
            file_path = "http://jtimmer.digitalspacemail17.net/data/2020/" + month +"/yesterday_2020" + month_to_num(month) + normalize_days(day) +".CSV"
            #print(file_path)
            csv_data = pd.read_csv(file_path, header = 4, encoding = "ISO-8859-1")
            d = csv_data[["Parameter", "Site Name", "Avg", "Max", "Hr. of Max"]]
            d["Parameter"].fillna(method = 'ffill',inplace = True)
            features = get_features(d, selected_sites, 2020)
            features_2020.append(features)
    
    for day in get_days("Oct"):
        file_path = "http://jtimmer.digitalspacemail17.net/data/" +"yesterday_2020" + month_to_num("Oct") + normalize_days(day) +".CSV"
        csv_data = pd.read_csv(file_path, header = 4, encoding = "ISO-8859-1")
        d = csv_data[["Parameter", "Site Name", "Avg", "Max", "Hr. of Max"]]
        d["Parameter"].fillna(method = 'ffill',inplace = True)
        features = get_features(d, selected_sites, 2020)
        features_2020.append(features)
    
    return features_2020
    
def get_normalized_features(features_2019, features_2020, site_names):
    '''
    :Purpose: get all normalized features from 2019 and 2020 features
    :prams: features_2019
    :type: list of dict
    :prams: features_2020
    :type: list of dict
    :return: list
    '''
    data_by_site_average = {key: [] for key in features_2020[0]}
    
    for data in features_2019:
        for param in data:
            for site in data[param]:
                for statics in data[param][site]:
                    if statics == "Avg":
                        if data[param][site][statics] != "M" and not isnan(float(data[param][site][statics])):
                            data_by_site_average[param].append(float(data[param][site][statics]))
                        else:
                            data_by_site_average[param].append(0)
                            
    for data in features_2020:
        for param in data:
            for site in data[param]:
                for statics in data[param][site]:
                    if statics == "Avg":
                        if data[param][site][statics] != "M" and not isnan(float(data[param][site][statics])):
                            data_by_site_average[param].append(float(data[param][site][statics]))
                        else:
                            data_by_site_average[param].append(0)
                            
    averages_average = [np.mean(data) for param, data in data_by_site_average.items()]
    std_average = [np.std(data, ddof = 1) for param, data in data_by_site_average.items()]
    
    standard_param_average = [0] * 474
    for index, param in enumerate(data_by_site_average):
        for index2, data in enumerate(data_by_site_average[param]):
            standard_param_average[index2 % 474] +=  (data - averages_average[index]) / (std_average[index] * 10)
    
    standard_param_average_sites = {key : [] for key in site_names}
    for index, param in enumerate(data_by_site_average):
        if index == 0:
            for index2, data in enumerate(data_by_site_average[param]):
                standard_param_average_sites[site_names[index2 % 5]].append((data - averages_average[index]) / (std_average[index] * 10))
        else:
            for index2, data in enumerate(data_by_site_average[param]):
                standard_param_average_sites[site_names[index2 % 5]][index2 // 5] += ((data - averages_average[index]) / (std_average[index] * 10))
    
    
    return standard_param_average, standard_param_average_sites