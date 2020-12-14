from src.accidents.accidents_data import *
import pandas as pd

try:
    from matplotlib import pyplot as plt
except ImportError:
    print('Importing matplotlib failed. Plotting will not work.')

def prepare_series(df, field='RushHour',  timestamp='2019-09-09', freq = 'W'):
    """
    Prepare a pd.Series to have index name 'ds' and name 'y' for fbprophet

    Parameters
    ----------
    df: pd.DataFrame 
        The accidents dataset prepared
    field: string
        Field of dataframe to plot 
    timestamp: 
        Minimum timestamp starting which data is to be selected
    freq: 'W' or 'D'
        Frequency with which we want to group the data based on 'Start_Time'
    Returns
    -------
    Same series with name and index name changed
    """
    assert isinstance(df, pd.DataFrame), "df should be a dataframe"
    assert ('Start_Time' in df.columns), "Start_Time is not present in columns"

    return df[df['Start_Time'] > pd.Timestamp(timestamp)].groupby([pd.Grouper(key='Start_Time',freq=freq),field]).size().unstack().fillna(0)

def custom_plot(df, colors = ['#219ebc', '#023047', '#fb8500', '#ffb703'], 
                ax=None, xlabel='', ylabel='Number of Accidents', title = 'Accidents by Traffic Density', figsize=(10, 6)):
    """
    Plot the custom function

    Parameters
    ----------
    df: pd.DataFrame output of prepare_series
    colors: list of colors to be used for the plots
    ax: Optional matplotlib axes on which to plot.
    xlabel: Optional label name on X-axis
    ylabel: Optional label name on Y-axis
    title: Optional custom Title for the plot
    figsize: Optional tuple width, height in inches.
    
    Returns
    -------
    None
    """
    if ax is None:
        fig = plt.figure(facecolor='w', figsize=figsize, dpi=260)
        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()
    
    for idx,key in enumerate(df.columns):
        df[key].plot(x='Time the year', y=ylabel, label=key, ax=ax, legend=True, color = colors[idx % len(colors)])
        
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.tick_params(
        which='both',
        bottom='off',
        left='off'
    )
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    plt.legend(list(df.columns),loc='lower left', bbox_to_anchor=(1, 0.5))
    fig.tight_layout()
    plt.show()

def make_figures(accident_df):
    """
    Helper function that includes all graphs in notebook
    """
    accidents_by_rush_hour = prepare_series(accident_df, field='RushHour',  timestamp='2019-09-09', freq = 'W')

    custom_plot(accidents_by_rush_hour)