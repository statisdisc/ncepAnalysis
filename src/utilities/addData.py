import numpy as np

def addRollingMean(data, column, years=1):
    '''
    Compute the rolling mean of a pandas data column over a timescale in years
    
    :param data: Pandas dataframe object with datetime index column.
    :param column: The column name to apply the rolling mean to, str.
    :param years: Number of years to average over, int float.
    :return: The dataframe with a new rolling mean column added.
    '''
    # Note, you cannot use f"{years}y" or f"{12*years}m" because a month/year can vary in length
    # E.g. 28 days vs 31 days in a month, 365 days vs 366 days in a year 
    period = f"{int(365.2425*years)}d"
    data[f"{column}-rolling-{years}"] = data.rolling(period, min_periods=1)[column].mean()
    return data

def addHdd(data):
    '''
    Compute the heating degree days from the temperature in Fahrenheit
    
    :param data: Pandas dataframe object with datetime index column.
    :return: The dataframe with a new heating degree days column added.
    '''
    data["hdd"] = 65 - data["temperature"]
    return data

def addWinterSeason(data):
    '''
    Evaluate whether a row in a column lies within a winter season.
    E.g. Any date within 15-11-2018 and 15-03-2019 would lie in the 2018 winter season.
    
    :param data: Pandas dataframe object with datetime index column.
    :return: The dataframe with a winter-season column added.
    '''
    data["winter-season"] = np.nan
    
    years = data.groupby(data.index.year).sum().index
    
    for year in years[:-1]:
        data.loc[f"15-11-{year}":f"15-03-{year+1}", "winter-season"] = year
    
    # Note that Pandas does not allow for converting to integer columns when nan values are present
    # Therefore the winter-season column is of type float64.
    return data