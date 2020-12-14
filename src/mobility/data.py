import pandas as pd
import os
from matplotlib import pyplot as plt

def read_mobility_data(path):
    '''
    Parameters
    ----------
    path : string
        path to mobility data
    Returns
    -------
    DataFrame od data read from csv
    '''
    
    file_path = path+"Region_Mobility_Report_CSVs/2020_US_Region_Mobility_Report.csv"
    assert os.path.exists(file_path), "File does not exist"
    return pd.read_csv(file_path)

def ingest_filter_data(df):
    '''
    Parameters
    ----------
    df : pandas DataFrame
        dataframe containing mobility data for All of US
    Returns
    -------
    DataFrame with only San Diego data filtering data with necessary attributes
    '''
    assert isinstance(df,pd.DataFrame),"Type should be a pandas dataframe"
    assert ('sub_region_1' and 'sub_region_2' in df.columns), "sub-region columns missing"
    SD_data = df.loc[(df['sub_region_1']=='California') \
                   & (df['sub_region_2']=='San Diego County')]

    # Remove region-based columns
    SD_data = SD_data.drop(SD_data.filter(regex='region|code|area').columns, axis=1)
    # Rename columns by removing unnecessary text
    SD_data = SD_data.rename(columns=lambda x: str(x).split('_')[0])
    # Compute new feature for the dataframe
    SD_data['date'] = pd.to_datetime(SD_data.date)

    return SD_data

def make_figure(df, cols=['transit','residential','workplaces','grocery'],
                   colors=['#219ebc', '#023047', '#fb8500', '#ffb703']):
    '''
    Parameters
    ----------
    df : pandas Dataframe
        Containing data for the evaluated time-frame
    cols : list
        List of columns we want to plot
    colors: string
        list of colors we want to use for the plots
    Returns
    -------
    None
    '''
    assert all(col in df.columns for col in cols), "Columns don't exist in DataFrame"
    assert len(cols) <= len(colors), "Insufficient Colors for plots"

    fig = plt.figure(facecolor='w',figsize=(10,6),dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    for idx,key in enumerate(cols):
        df.plot(x='date',y=key, label=key, ax=ax, legend=True, color = colors[idx % len(colors)])
    
    ax.set_title('Changes in mobility')
    ax.set_xlabel('')
    ax.set_ylabel('Percent change from baseline', fontsize=12)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    plt.legend(cols,loc='lower left', bbox_to_anchor=(1, 0.5))
    plt.show()