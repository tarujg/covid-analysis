
import pandas as pd

def read_sdge_data(path,year,quarter,type="ELEC"):
    '''
    Parameters
    ----------
    path : string
        path to SDGE data
    type : string
        Either electricity "ELEC" or "GAS" data. The default is "ELEC".
    year : string
        
    quarter : string
        "Q1","Q2","Q3","Q4"

    Returns
    -------
    DataFrame od data read from csv
    '''
    
    assert type in ["ELEC","GAS"]
    assert isinstance(year,str)
    assert quarter in ["Q1","Q2","Q3","Q4"]
    
    return pd.read_csv(path+"SDGE-{}-{}-{}.csv".format(type,year,quarter))


def get_avgkwh_per_customer_month(data):
    '''
    Parameters
    ----------
    data : DataFrame
        Contains the SDGE data.

    Returns
    -------
    avgkwh_cm : dict
        Dictionary containing the sum of average kWh per month per type of customer
    '''
    
    assert isinstance(data,pd.DataFrame)
    
    months = data["Month"].unique()
    customer = data["CustomerClass"].unique()
    avgkwh = data["AveragekWh"]
    
    avgkwh_cm = {}
    
    for m in months:
        for c in customer:
            akwh = avgkwh[data["Month"] == m][data["CustomerClass"]==c]
            avgkwh_cm[str(m)+str(c)] = sum(akwh)
            
    return avgkwh_cm

