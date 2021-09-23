import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plotRandomWalk(folder, simulations=20, iterations=300, bias=0.):
    '''
    Plot random walk paths and their standard deviations.
    
    :param folder: The output directory of the plots.
    :param simulations: Total random walk simulations to average over.
    :param iterations: Total walk iterations per simulation.
    :param bias: Bias for positive or negative steps.
        bias >= 1.0 guarantees positive step
        bias <=-1.0 guarantees negative step
        bias == 0.0 is no bias (default)
    :return: None
    '''
    # Create random walk simulations
    iteration = np.arange(1, iterations+1, 1)
    walks = np.random.random((simulations, iterations))
    walks = np.sign(2*(walks - 0.5) + bias)
    walksSummed = np.cumsum(walks, axis=-1)
    walksMean = np.mean(walksSummed, axis=0)
    
    
    # Plot the random walks
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,5))
    
    for walk in walksSummed:
        ax.step(iteration, walk,  alpha=0.5, linewidth=0.5)
    
    ax.axhline(0, color="grey", linestyle="--", linewidth=1.0)
    ax.plot(iteration, walksMean, color="black",   linewidth=3.0, label="Mean walk path")
    
    ax.set_xlim(np.min(iteration), np.max(iteration))
    ax.set_xlabel("Walk iteration")
    ax.set_ylabel("Walk distance from origin")
    ax.set_title(f"Random walk, bias={bias}")
    ax.legend(loc="best")
    
    plt.savefig(
        os.path.join(folder, f"random-walk-bias-{str(bias).replace('.','p')}.png"),
        bbox_inches = "tight",
        dpi = 300
    )
    plt.close()
    
    
    
    # Compute the standard deviations of the walk paths
    walksStd = []
    for walk in walksSummed:
        data = pd.DataFrame(columns=["walk-summed"], data=walk)
        data["walk-summed-std"] = data["walk-summed"].rolling(window=len(walk), min_periods=1).std()
        
        walksStd.append(data["walk-summed-std"].to_numpy())
    walksStdMean = np.mean(walksStd, axis=0)
    
    # Plot the random walks standard deviation
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,5))
    
    for walk in walksStd:
        ax.step(iteration, walk,  alpha=0.5, linewidth=0.5)
    
    ax.axhline(0, color="grey", linestyle="--", linewidth=1.0)
    ax.plot(iteration, walksStdMean, color="black",   linewidth=3.0, label="Mean st. dev. of walk path")
    
    ax.set_xlim(np.min(iteration), np.max(iteration))
    ax.set_xlabel("Walk iteration")
    ax.set_ylabel(r"Walk distance")
    ax.set_title(f"Random walk st. dev., bias={bias}")
    ax.legend(loc="best")
    
    plt.savefig(
        os.path.join(folder, f"random-walk-std-bias-{str(bias).replace('.','p')}.png"),
        bbox_inches = "tight",
        dpi = 300
    )
    plt.close()