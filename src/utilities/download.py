import urllib.request
import numpy as np
import pandas as pd

######################################### Function #################################
def temp(yrIn):

    Edds={}

    for j in ['Cooling', 'Heating']:

        file = urllib.request.urlopen('https://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_data/'+str(yrIn)+'/Population.'+j+'.txt')
        ind =0

        for line in file:

        if ind == 3:
            dateStr = line.decode("utf-8")
            dates = pd.date_range( pd.to_datetime(dateStr.split('|')[1]).date(),pd.to_datetime(dateStr.split('|')[-1]).date(),freq='D')

        if ind == 13:
            Edds[j] = np.array([float(i) for i in line.decode("utf-8").split('|')[1:] ])
        ind = ind +1
    
    dfOut = pd.DataFrame(index = dates, columns = ['Temperature'], data =65 - Edds['Heating'] + Edds['Cooling'])
    return dfOut
################################### End Functions ####################################


if __name__ == '__main__':

    years = np.arange(1981,2021,1).astype(int)
    dfTemp = pd.DataFrame()

    for i in range(years.size):
        dfTemp = dfTemp.append(DLTemp(years[i]))