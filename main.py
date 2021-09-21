#Core Python modules
import numpy as np

# User-made modules
from src.objects.pathSetup import pathSetup
from src.plots.plotRollingMean import plotRollingMean
from src.utilities import download
from src.utilities.timeElapsed import timeElapsed

def addRollingMean(data, column, years=1):
    # Note, you cannot use f"{years}y" or f"{12*years}m" because a month/year can vary in length
    # E.g. 28 days vs 31 days in a month, 365 days vs 366 days in a year 
    period = f"{int(365.2425*years)}d"
    data[f"{column}-rolling-{years}"] = data.rolling(period, min_periods=1)[column].mean()
    return data



@timeElapsed
def main():
    folder = pathSetup(root=__file__)
    
    years = np.arange(1981,2021,1)
    data = download.downloadOrLoad(years, folder.data)
    
    data = addRollingMean(data, "Temperature", years=10)
    data = addRollingMean(data, "Temperature", years=30)
    
    plotRollingMean(data, folder.outputs)
    
    print(data.head(10))
    print(data.tail(10))
    print(data.info())
    # print(data.describe())

if __name__ == "__main__":
    main()