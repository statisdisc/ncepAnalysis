import os
import matplotlib.pyplot as plt

def plotRollingMean(data, folder):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,10))
    
    data = data.loc['1991-01-01':'1992-01-01']
    
    # data["temperature"]           .plot(ax=ax, linewidth=0.5, color="#999999")
    data["temperature-rolling-10"].plot(ax=ax, linewidth=1.0, color="blue")
    data["temperature-rolling-30"].plot(ax=ax, linewidth=1.0, color="orange")
    
    ax.set_xlabel("Date")
    ax.set_ylabel(r"Temperature ($\deg$F)")
    ax.legend(loc="best")
    
    plt.savefig(
        os.path.join(folder, "rolling-mean.png"),
        bbox_inches = "tight",
        dpi = 300
    )
    plt.close()