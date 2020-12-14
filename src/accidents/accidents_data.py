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

def ingest_and_clean(raw_fp = './Data/US_Accidents_June20.csv'):
    """
    """
    assert os.path.exists(raw_fp),"Raw file exists"
    assert raw_fp[-3:] == "csv", "File of type csv"

    df = pd.read_csv(raw_fp)
    return df

def RushHour(isRushHour, labels = ["Low Traffic", "Normal Traffic", "Rush Hour"]):
    """
    """
    assert isinstance(isRushHour,dict), "Rush Hour is a dictionary"
    assert all(0 <= v <= len(labels) for v in isRushHour.values()),"Rush Hour Dictionary has less labels"
    for k,v in list(isRushHour.items()):
        isRushHour[k] = labels[v]

    return isRushHour