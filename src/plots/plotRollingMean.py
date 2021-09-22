import os
import matplotlib.pyplot as plt

def plotRollingMean(data, folder, id="", showOriginalData=False):
    print(f"Plotting rolling mean, id: {id}")
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,6))
    
    if showOriginalData:
        data["temperature"].plot(ax=ax, linewidth=0.5, color="#999999")
    
    data["temperature-rolling-10"].plot(ax=ax, linewidth=1.0, color="blue")
    data["temperature-rolling-30"].plot(ax=ax, linewidth=1.0, color="orange")
    
    ax.set_xlabel("Date")
    ax.set_ylabel(r"Temperature ($^\circ$F)")
    ax.legend(loc="best")
    
    plt.savefig(
        os.path.join(folder, f"rolling-mean-{id}.png"),
        bbox_inches = "tight",
        dpi = 300
    )
    plt.close()