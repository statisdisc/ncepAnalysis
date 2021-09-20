#Core Python modules
import datetime
import os
import sys

# User-made modules
from src.objects.pathSetup import pathSetup
from src.utilities import download
from src.utilities.timeElapsed import timeElapsed

@timeElapsed
def main():
    folder = pathSetup(root=__file__)
    
    data = download.temp(2000)
    print(data.head())

if __name__ == "__main__":
    main()