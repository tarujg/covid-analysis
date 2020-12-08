# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 17:14:55 2020

@author: 77243
"""

import matplotlib.pyplot as plt
import numpy as np

def get_graphs(standard_param_average, standard_param_average_sites, site_names):
    '''
    :Purpose: get all graphs generated from normalized 2019 and 2020 features
    :prams: standard_param_average
    :type: list
    :return: None
    '''
    
    ## Average different plot
    plt.figure(figsize=(40,10))
    diff = np.array([data_2020 - data_2019 for data_2020, data_2019 in zip(standard_param_average[237:], standard_param_average[:237])])
    x_range = np.arange(237)
    above = np.ma.masked_array(diff, diff > 0)
    below = np.ma.masked_array(diff, diff < 0)
    plt.bar(x_range, above, color =  "#219EBC")
    plt.bar(x_range, below, color = "#FB8500")
    plt.xticks(np.arange(0, 237, step=30), ["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],fontsize = 20)
    plt.yticks(fontsize = 20)
    plt.xlabel("Date", fontsize = 40)
    plt.ylabel("Normalized Index Difference", fontsize = 40)
    plt.title("The difference of Average Pollutant Index between 2020 and 2019", fontsize = 40)
    plt.legend(fontsize = 30)
    plt.savefig("general_average_difference.png")
    plt.show()
    
    ## Average boxplot of 2019 and 2020
    data = [standard_param_average[:237], standard_param_average[237:]]
    plt.figure(figsize=(10,6))
    box = plt.boxplot(data, showfliers = False, notch=True, patch_artist=True, medianprops=dict(color="black"))
    colors = ["#219EBC", "#FB8500"]
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    plt.xticks(np.arange(1,3), ["2019","2020"])
    plt.title('Boxplot of Average Pollutant Index')
    plt.savefig("box_general_average.png")
    plt.show()
    
            
    ## Average boxplot of different areas in 2020
    data = [standard_param_average_sites[site_names[i]][237:] for i in range(5)]
    plt.figure(figsize=(10,6))
    box = plt.boxplot(data, showfliers = False, notch=True, patch_artist=True, medianprops=dict(color="green"))
    colors = ["#8ECAE6","#219EBC", "#023047", "#ffb703","#FB8500"]
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    plt.xticks(np.arange(1,6), site_names)
    plt.title('Boxplot of Average Pollutant Index in Different Areas')
    plt.savefig("Box_AQI_areas.png")
    plt.show()