import pandas as pd
from io import StringIO

def ingest_and_clean(raw_fp):
    '''
    Parameters
    ----------
    raw_fp : string
        path to tax certification data
    
    Returns
    -------
    DataFrame od data read from csv
    '''
    with open(raw_fp) as f:
        raw_str = f.read()

    raw_str = raw_str.replace('"0017-', '"2017-')
    raw_str = raw_str.replace('"7201-', '"2017-')
    raw_str = raw_str.replace('"7202-', '"2027-')
    raw_str = raw_str.replace('"0018-', '"2018-')
    raw_str = raw_str.replace('"0019-', '"2019-')
    raw_str = raw_str.replace('"1019-', '"2019-')
    raw_str = raw_str.replace('"0020-', '"2020-')

    df = pd.read_csv(
        StringIO(raw_str),
        parse_dates=[
            'date_account_creation',
            'date_cert_expiration',
            'date_business_start'
        ]
    )
    verify_good_data(df)
    return df

def verify_good_data(df):
    '''
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame of good data
    
    Returns
    -------
    Nothing is everything is good; otherwise it raises an error
    '''
    try:
        pd.to_datetime(df['date_account_creation'])
        pd.to_datetime(df['date_business_start'])
    except pd.errors.OutOfBoundsDatetime as e:
        print(e)
        raise e

def aggregate_on(df, column, period='W'):
    """
    Return a numerial time pd.Series with freq=period based on counts
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame of good data
    column : str
        column name to aggregate on
    period : str
        time period code name
    
    Returns
    -------
    A pd.Series time series with DateTime index
    """
    return df.resample(period, on=column).size()