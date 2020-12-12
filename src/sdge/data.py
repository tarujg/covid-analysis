
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

def make_figure(data19,data20,customer):
    '''
    

    Parameters
    ----------
    data19 : list
        2019 electricity consumption across months
    data20 : list
        2020 electricity consumption across months
    customer: string
        customer class being analysed

    Returns
    -------
    None

    '''
    
    x = np.arange(12)
    plt.bar(x-0.4,data19,width=0.4,align='edge',color="#219EBC")
    
    x = np.arange(9)
    plt.bar(x,data20,width=0.4,align='edge',color="#FB8500")
    
    plt.title(customer,fontsize=15)
    plt.xticks(np.arange(12),['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    plt.ylabel("Average Power (MWh) ",fontsize=10)
    plt.legend(['2019','2020'],bbox_to_anchor=(1.05, 1), loc='upper left')
