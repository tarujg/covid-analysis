import numpy as np
from fbprophet import Prophet
from src.econ.data import *

try:
    from matplotlib import pyplot as plt
    from matplotlib.dates import (
        MonthLocator,
        num2date,
        AutoDateLocator,
        AutoDateFormatter,
        DateFormatter
    )
    from matplotlib.ticker import FuncFormatter

    from pandas.plotting import deregister_matplotlib_converters
    deregister_matplotlib_converters()
except ImportError:
    logger.error('Importing matplotlib failed. Plotting will not work.')


def prepare_ts(s):
    """
    Prepare a pd.Series to have index name 'ds' and name 'y' for fbprophet

    Parameters
    ----------
    s : pd.Series
        A datetime indexed pd.Series
    
    Returns
    -------
    Same series with name and index name changed
    """
    s = s.rename_axis('ds')
    out = s.rename('y').reset_index()
    return out


def make_prophet(s, prior=0.5):
    """
    Make a Prophet object and initialize the analysis

    Parameters
    ----------
    s : pd.Series
        A datetime indexed pd.Series
    prior : float
        The scale given to prior trend
    
    Returns
    -------
    A prophet model object and the forecast time series
    """
    if 'W' in s.index.freq.name:
        weekly_seasonality=False
        daily_seasonality=False
    if 'D' in s.index.freq.name:
        weekly_seasonality=True
        daily_seasonality=False
    m = Prophet(
        changepoint_range=1, changepoint_prior_scale=prior,
        weekly_seasonality=weekly_seasonality,
        daily_seasonality=daily_seasonality
    )
    m.fit(prepare_ts(s))

    future = m.make_future_dataframe(periods=0)
    forecast = m.predict(future)
    return m, forecast





def pf_custom_plot(
    m, fcst, ax=None, uncertainty=True, plot_cap=True, xlabel='ds', ylabel='y',
    figsize=(10, 6), custom_date_formatter=None
):
    """
    Plot the Prophet forecast with more customizations

    Parameters
    ----------
    m: Prophet model.
    fcst: pd.DataFrame output of m.predict.
    ax: Optional matplotlib axes on which to plot.
    uncertainty: Optional boolean to plot uncertainty intervals, which will
        only be done if m.uncertainty_samples > 0.
    plot_cap: Optional boolean indicating if the capacity should be shown
        in the figure, if available.
    xlabel: Optional label name on X-axis
    ylabel: Optional label name on Y-axis
    figsize: Optional tuple width, height in inches.

    Returns
    -------
    A matplotlib figure.
    """
    if ax is None:
        fig = plt.figure(facecolor='w', figsize=figsize)
        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()
    fcst_t = fcst['ds'].dt.to_pydatetime()
    ax.plot(
        m.history['ds'].dt.to_pydatetime(), m.history['y'],
        'k.', alpha=0.25, label='Actual Value'
    )
    ax.plot(fcst_t, fcst['yhat'], ls='-', c='#0072B2', alpha=0.8, label='Predicted')
    if 'cap' in fcst and plot_cap:
        ax.plot(fcst_t, fcst['cap'], ls='--', c='k')
    if m.logistic_floor and 'floor' in fcst and plot_cap:
        ax.plot(fcst_t, fcst['floor'], ls='--', c='k')
    if uncertainty and m.uncertainty_samples:
        ax.fill_between(fcst_t, fcst['yhat_lower'], fcst['yhat_upper'],
                        color='#0072B2', alpha=0.2, label='Uncertainty Interval')
    # Specify formatting to workaround matplotlib issue #12925
    locator = AutoDateLocator(interval_multiples=False)
    formatter = AutoDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    if custom_date_formatter:
        ax.xaxis.set_major_formatter(custom_date_formatter)
    # ax.grid(True, which='major', c='gray', ls='-', lw=1, alpha=0.2)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    return fig


def add_changepoints_to_plot(
    ax, m, fcst, threshold=0.01, cp_color='r', cp_linestyle='--', trend=True,
    cp_vlines=True
):
    """Add markers for significant changepoints to prophet forecast plot.
    Example:
    fig = m.plot(forecast)
    add_changepoints_to_plot(fig.gca(), m, forecast)
    Parameters
    ----------
    ax: axis on which to overlay changepoint markers.
    m: Prophet model.
    fcst: Forecast output from m.predict.
    threshold: Threshold on trend change magnitude for significance.
    cp_color: Color of changepoint markers.
    cp_linestyle: Linestyle for changepoint markers.
    trend: If True, will also overlay the trend.
    Returns
    -------
    a list of matplotlib artists
    """
    artists = []
    if trend:
        artists.append(ax.plot(fcst['ds'], fcst['trend'], c=cp_color, label='Trend Line'))
    signif_changepoints = m.changepoints[
        np.abs(np.nanmean(m.params['delta'], axis=0)) >= threshold
    ] if len(m.changepoints) > 0 else []
    if cp_vlines:
        for cp in signif_changepoints:
            artists.append(ax.axvline(x=cp, c=cp_color, ls=cp_linestyle))
    return artists


def make_figure_overall(econ_df):
    """
    Plot the first analysis graph with all data

    Parameters
    ----------
    econ_df : pd.DataFrame
        DataFrame of good data
    """
    ts = aggregate_on(econ_df, 'date_account_creation', period='W')
    model, forecasts = make_prophet(ts)

    fig = pf_custom_plot(
        model, forecasts, uncertainty=True,
        xlabel='', ylabel='Number of Accounts Opened',
        figsize=(8, 5)
    )
    add_changepoints_to_plot(fig.gca(), model, forecasts, cp_color='#FB8500', cp_vlines=False)
    plt.title('Number of Business Accounts Opened by Week Since 2008', {'fontsize': 15})
    plt.ylabel('Number of Accounts Opened', fontsize=13)
    fig.gca().legend(bbox_to_anchor=(1.04,0), loc="lower left", prop={'size': 12})
    fig.savefig('figures/econ-1.png', bbox_inches='tight', dpi=200)


def make_figure_group(indf, groupname):
    """
    Plot the rest analysis graphs with group data

    Parameters
    ----------
    econ_df : pd.DataFrame
        DataFrame of good data
    groupname : str
        Name of group to graph
    """
    model, forecasts = make_prophet(indf, prior=0.8)

    fig = pf_custom_plot(
        model, forecasts, uncertainty=True,
        xlabel='', ylabel='Number of Accounts Opened',
        figsize=(8, 3), custom_date_formatter=DateFormatter('%b-%y')
    )
    add_changepoints_to_plot(fig.gca(), model, forecasts, cp_color='#FB8500', cp_vlines=False)
    plt.title(f'{groupname}', {'fontsize': 15})
    plt.ylabel('Number of Accounts Opened', fontsize=12)
    fig.gca().legend(
        loc='upper center', bbox_to_anchor=(0.5, -0.18),
        fancybox=True, shadow=True, ncol=4
    )
    plt.show()
    fig.savefig(f'figures/econ-{indf.name}.png', bbox_inches='tight', dpi=200)


def make_figures(econ_data_fp):
    """
    Helper function that includes all graphs in notebook
    """
    econ_df = ingest_and_clean(econ_data_fp)
    make_figure_overall(econ_df)

    creations_by_ownership = (
        econ_df[econ_df.date_account_creation >= pd.Timestamp('2018-01-01')]
        .groupby([
            pd.Grouper(key='date_account_creation', freq='W'),
            'ownership_type'
        ])
        .size().unstack().fillna(0)
    )
    make_figure_group(creations_by_ownership['CORP'], 'Corporations')
    make_figure_group(creations_by_ownership['LLC'], 'LLCs')
    make_figure_group(creations_by_ownership['SCORP'], '"S" Corporations')
    make_figure_group(creations_by_ownership['SOLE'], 'Sole Ownerships')
