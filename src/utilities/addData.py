import numpy as np

def addRollingMean(data, column, years=1):
    # Note, you cannot use f"{years}y" or f"{12*years}m" because a month/year can vary in length
    # E.g. 28 days vs 31 days in a month, 365 days vs 366 days in a year 
    period = f"{int(365.2425*years)}d"
    data[f"{column}-rolling-{years}"] = data.rolling(period, min_periods=1)[column].mean()
    return data

def addHdd(data):
    data["hdd"] = 65 - data["temperature"]
    return data

def addWinterSeason(data):
    data["winter-season"] = np.nan
    
    years = data.groupby(data.index.year).sum().index
    
    for year in years[:-1]:
        data.loc[f"15-11-{year}":f"15-03-{year+1}", "winter-season"] = year
    
    # Note that Pandas does not allow for converting to integer columns when nan values are present
    # Therefore the winter-season column is of type float64.
    return data