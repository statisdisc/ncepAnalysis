#Core Python modules
import numpy as np

# User-made modules
from src.objects.pathSetup import pathSetup
from src.utilities import download
from src.utilities.timeElapsed import timeElapsed

@timeElapsed
def main():
    folder = pathSetup(root=__file__)
    
    years = np.arange(1981,2021,1)
    data = download.downloadOrLoad(years, folder.data)
    print(data.head())
    print(data.info())
    print(data.describe())

if __name__ == "__main__":
    main()