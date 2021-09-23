#Core Python modules
import numpy as np

# User-made modules
from src.objects.pathSetup import pathSetup
from src.plots.plotHdd import plotHddCumsum, plotYearlyHdd
from src.plots.plotRandomWalk import plotRandomWalk
from src.plots.plotRollingMean import plotRollingMean
from src.utilities import addData
from src.utilities import download
from src.utilities.timeElapsed import timeElapsed


@timeElapsed
def main():
    '''
    Download temperature data from the National Center for Environmental Prediction
    and use it to analyse trends in the temperature and the heating degree days
    which determine which days are likely to require homes to be heated.
    '''
    folder = pathSetup(root=__file__)
    
    print("\nDownloading and/or loading the temperature data")
    years = np.arange(1981,2021,1)
    data = download.downloadOrLoad(years, folder.data)
    
    print("\nProcessing temperature data")
    data = addData.addRollingMean(data, "temperature", years=10)
    data = addData.addRollingMean(data, "temperature", years=30)
    data = addData.addHdd(data)
    data = addData.addWinterSeason(data)
    
    print("\nData processing completed, data summary:")
    print(data.head())
    print(data.tail())
    print(data.info())
    print(data.describe())
    
    print("\nPlotting rolling means of temperature data")
    plotRollingMean(data, folder.outputs_temp, id="all", showOriginalData=True)
    plotRollingMean(data.loc["1990-01-01":"2020-12-31"], folder.outputs_temp, id="rolling-only")
    for year in years:
        plotRollingMean(data.loc[f"{year}-01-01":f"{year}-12-31"], folder.outputs_temp, id=year)
    
    print("\nPlotting total winter heating degree days")
    plotYearlyHdd(data, folder.outputs_hdd)
    
    print("\nPlotting cumulative winter heating degree days for each year")
    for season, df in data[["hdd"]].groupby(data["winter-season"]):
        plotHddCumsum(df, folder.outputs_hdd, id=int(season))
    
    print("\nPlotting random walk simulations")
    plotRandomWalk(folder.outputs_rw)
    plotRandomWalk(folder.outputs_rw, bias=-0.5)
    plotRandomWalk(folder.outputs_rw, bias= 0.5)
    

if __name__ == "__main__":
    main()