# NCEP Analysis
Package for downloading temperature data from the National Center for Environmental Prediction and using it to analyse trends in the temperature and the heating degree days which determine which days are likely to require homes to be heated.

## Setup
[Download and install Python 3.8 or higher.](https://www.python.org/downloads/)

Use the Python package manager ```pip``` or ```pip3``` to install *requirements.txt*.

```pip install -r requirements.txt```

## Usage
Once the repository is clones, navigate to the *ncepAnalysis/* directory and run ```python main.py``` or ```python3 main.py``` depending on your Python alias. This script will download data (if necessary) to *ncepAnalysis/data/* and output plots to *ncepAnalysis/outputs/*.

## Example outputs

A plot of temperature timeseries (grey) with a rolling mean of 10 years (blue) and rolling mean of 30 years (orange).

<img src="/outputs/temperature/rolling-mean-all.png" width="80%">


A plot of total yearly heating degree days (which is indicitive of the amount of central heating required for households) and a regression-based fit line.

<img src="/outputs/hdd/hdd-order-1.png" width="80%">


20 simulations of a random walk model and the mean walk path (black) which should tend to zero as the number of simulations tends to infinity.

<img src="/outputs/random-walk/random-walk-bias-0p0.png" width="80%">
