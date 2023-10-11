import pandas as pd
import numpy as np

def sma(df, value_column, window_size):
    '''
    Simple Moving Average (SMA):
    SMA (arithmetic moving average) provides a smoothed representation 
    of a dataset by averaging a set of data points over a specified period.
    '''
    df['SimpleMeanAvg'] = df[value_column].rolling(window=window_size).mean()
    df['SimpleMedianAvg'] = df[value_column].rolling(window=window_size).median()
    return df

def cumma(df, value_column): 
    '''
    Cumulative Moving Average (CumMA):
    CumMA takes the average of all data points up to the current point. 
    It provides a cumulative view of the data and is useful for tracking long-term trends.
    '''
    df['CumMA'] = df[value_column].expanding().mean()
    return df 

def cenma(df, value_column, window): 
    '''
    Centered Moving Average (CenMA):
    CenMA calculates the average of data points within a centered window, meaning that the window size is an even number. 
    This can reduce the lag seen in simple moving averages.
    '''
    if window % 2 == 0:
        df['meanCenMA'] = df[value_column].rolling(window=window, center=True).mean()
        df['medianCenMA'] = df[value_column].rolling(window=window, center=True).median()
    else:
        raise ValueError("Window size must be an even number for Centered Moving Average (CenMA).")
    return df

def ema(df, value_column, span):
    '''
    Exponential Moving Average (EMA):
    EMA gives more weight to recent data points, making it more responsive to short-term changes.
    '''
    df['ExpMeanAvg'] = df[value_column].ewm(span=span, adjust=False).mean()
    return df

def wma(df, value_column, window):
    '''
    Weighted Moving Average (WMA):
    WMA assigns different weights to different data points within the moving average window.
    This allows you to emphasize certain data points more than others, making it more adaptable to specific patterns in your data.
    '''
    weights = np.arange(1, window + 1)
    df['ExpMeanAvg'] = df[value_column].rolling(window=window).apply(lambda x: np.sum(x * weights) / np.sum(weights))
    return df

def tma(df, value_column, sma_window, tma_window): 
    '''
    Triangular Moving Average (TMA):
    TMA is a double-smoothed SMA that smooths the data twice, reducing the lag compared to a simple moving average. 
    Useful for smoothing out data with seasonality.
    '''
    df['meanSMA_TMA'] = df[value_column].rolling(window=sma_window).mean().rolling(window=tma_window).mean()
    df['medianSMA_TMA'] = df[value_column].rolling(window=sma_window).mean().rolling(window=tma_window).median()
    return df

def hma(df, value_column, wma_window, hma_window): 
    '''
    Hull Moving Average (HMA):
    HMA attempts to address the lag in moving averages by using weighted moving averages of three different time frames. 
    It is designed to be more responsive to price changes.
    '''
    wma1 = 2 * df[value_column].rolling(window=wma_window).mean()
    wma2 = df[value_column].rolling(window=hma_window).mean()
    df['HMA'] = np.sqrt(hma_window) * (wma1 - wma2)
    return df

def vwma(df, price_value_column, trade_volume_column, window):
    ''' 
    Volume Weighted Moving Average (VWMA): 
    VWMA is a moving average that takes into account the trading volume of each data point, giving more weight to periods with higher trading volume.
    '''
    volume = df[trade_volume_column]
    df['VWMA'] = (df[price_value_column] * volume).rolling(window=window).sum() / volume.rolling(window=window).sum()
    return df

def ama(df, value_column, fast_window, slow_window): 
    ''' 
    Adaptive Moving Average (AMA):
    AMA is a moving average that adjusts the length of the moving average based on market volatility. 
    Shorter moving averages are used in volatile markets, while longer moving averages are used in less volatile markets.
    '''
    volatility = df[value_column].diff().abs().rolling(window=fast_window).mean()
    volatility = volatility.fillna(1)
    df['volatility'] = volatility
    df['AMA'] = df[value_column]
    df['AMA'] = np.where(volatility > 1, df[value_column].rolling(window=fast_window).mean(), df['AMA'])
    df['AMA'] = np.where(volatility <= 1, df[value_column].rolling(window=slow_window).mean(), df['AMA'])
    return df

def kama(df, value_column, window, fast_alpha, slow_alpha):
    '''
    Kaufman's Adaptive Moving Average (KAMA):
    KAMA adjusts the smoothing period based on market volatility. 
    This method is designed to adapt to both trending and ranging markets.
    - fast_alpha determines how quickly the KAMA responds to changes in market conditions. If you expect more frequent market changes or are trading in a shorter time frame, choose a smaller fast_alpha (e.g., 2).
    - slow_alpha controls the responsiveness of KAMA over a longer time frame. Larger slow_alpha values (e.g., 30) makes the KAMA less responsive to recent data, making it suitable for capturing longer-term trends and filtering out short-term noise.
    '''
    def calculate_er(series):
        return series.diff().abs().sum() / series.diff().abs().sum()

    er = df[value_column].rolling(window=window).apply(calculate_er)
    fast_alpha = 2 / (fast_alpha + 1)
    slow_alpha = 2 / (slow_alpha + 1)
    df['KAMA'] = df[value_column]
    df['KAMA'] = np.where(er > 0, (fast_alpha * df['value'] + (1 - fast_alpha) * df['KAMA']), df['KAMA'])
    df['KAMA'] = np.where(er <= 0, (slow_alpha * df['value'] + (1 - slow_alpha) * df['KAMA']), df['KAMA'])
    return df
