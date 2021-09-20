import os
import urllib.request
import numpy as np
import pandas as pd

######################################### Functions ################################
def getTempData(year):
    print(f"Getting data for year {year}")
    Edds={}

    for j in ["Cooling", "Heating"]:
        file = urllib.request.urlopen(f"https://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_data/{year}/Population.{j}.txt")
        
        ind = 0
        for line in file:
            if ind == 3:
                dateStr = line.decode("utf-8")
                dates = pd.date_range(
                    pd.to_datetime(dateStr.split("|")[ 1]).date(),
                    pd.to_datetime(dateStr.split("|")[-1]).date(),
                    freq = "D"
                )
            
            if ind == 13:
                Edds[j] = np.array([float(i) for i in line.decode("utf-8").split("|")[1:]])
            
            ind = ind + 1
    
    dfOut = pd.DataFrame(index=dates, columns=["Temperature"], data=65-Edds["Heating"]+Edds["Cooling"])
    return dfOut

def downloadOrLoad(years, folder):
    years = np.array(years).astype(int)
    file = os.path.join(folder, f"data-{years[0]}-{years[-1]}.pkl")
    
    if os.path.isfile(file):
        return pd.read_pickle(file)
    else:
        dataframeTemp = pd.DataFrame()
        for i in range(years.size):
            dataframeTemp = dataframeTemp.append(getTempData(years[i]))
        
        dataframeTemp.to_pickle(file)
        return dataframeTemp

################################### End Functions ####################################


if __name__ == "__main__":

    dfTemp = downloadOrLoad(np.arange(1981,2021,1), sys.path[0])