import os
import matplotlib.pyplot as plt

def plotHdd(data, folder):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,10))
    
    data["hdd"].plot(ax=ax)
    
    ax.set_xlabel("Date")
    ax.set_ylabel(r"HDD ($\deg$F)")
    ax.legend(loc="best")
    
    plt.savefig(
        os.path.join(folder, "hdd.png"),
        bbox_inches = "tight",
        dpi = 300
    )
    plt.close()