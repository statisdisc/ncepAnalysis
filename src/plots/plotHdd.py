import os
import numpy as np
import matplotlib.pyplot as plt

def plotYearlyHdd(data, folder):
    '''
    Plot the yearly total heating degree days and fit trendlines.
    
    :param data: Pandas dataframe object with a "hdd" column and years as the indices.
    :param folder: The output directory of the plots.
    :return: None
    '''
    def yearlyHddPlot(x, y, fit, err, order, chiSquaredReduced, folder="", color="black"):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,5))
    
        ax.fill_between(x, fit-err, fit+err, facecolor=color, alpha=0.5, linewidth=0)
        ax.plot(x, y, "-", color="#cccccc")
        ax.plot(x, y, "o", color="black", label="Yearly HDD")
        ax.plot(x, fit, "-", color=color, linewidth=3., label=fr"Order {order} fit, $\chi^2_\nu=${chiSquaredReduced:.2f}")
        
        ax.set_xlim(np.min(x), np.max(x))
        ax.set_xlabel("Date")
        ax.set_ylabel(r"Total Yearly HDD ($^\circ$F)")
        ax.legend(loc="best")
        
        plt.savefig(
            os.path.join(folder, f"hdd-order-{order}.png"),
            bbox_inches = "tight",
            dpi = 300
        )
        plt.close()
    
    data = data[["hdd"]].groupby(data["winter-season"]).sum()
    
    x = data.index.values
    y = data.hdd.values
    
    # Linear regression
    (grad, intercept), cov1 = np.polyfit(x, y, 1, cov=True)
    fit1 = np.polyval((grad, intercept), x)
    
    # Compute the one-standard-deviation bound for the fitted curve
    err1 = np.sqrt(cov1[0][0]*x**2 + cov1[1][1] + x*(cov1[0][1]+cov1[1][0]))
    
    # Chi-squared test: https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
    chiSquared1 = np.sum((fit1 - y)**2 / err1**2)
    
    # Reduced chi-squared test: https://en.wikipedia.org/wiki/Reduced_chi-squared_statistic
    # A value close to 1 indicates an ideal fit
    # A value orders of magnitude larger than 1 indicates a poor fit or under-estimated errors
    # A value orders of magnitude less than 1 indicates over-fitting
    chiSquaredReduced1 = chiSquared1/(len(x) - 2)
    
    print(f"Gradient has a value of {grad:.2f} +/- {np.sqrt(cov1[0][0]):.2f} F/year")
    print(f"Intercept has a value of {intercept:.2f} +/- {np.sqrt(cov1[1][1]):.2f} F")
    print(f"Order 1 regression has chi-squared of {chiSquared1:.2f}, chi-squared-reduced of {chiSquaredReduced1:.2f}")
    yearlyHddPlot(x, y, fit1, err1, 1, chiSquaredReduced1, folder=folder)
    
    # Regression order 2
    coeffs2, cov2 = np.polyfit(x, y, 2, cov=True)
    fit2 = np.polyval(coeffs2, x)
    
    # Compute the one-standard-deviation bound for the fitted curve
    err2 = np.sqrt(
        cov2[0][0]*x**4 \
      + cov2[1][1]*x**2 \
      + cov2[2][2] \
      + 2*cov2[0][1]*x**3 \
      + 2*cov2[1][2]*x \
      + 2*cov2[2][0]*x**2 \
    )
    
    # Chi-squared test: https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
    chiSquared2 = np.sum((fit2 - y)**2 / err2**2)
    
    # Reduced chi-squared test: https://en.wikipedia.org/wiki/Reduced_chi-squared_statistic
    # A value close to 1 indicates an ideal fit
    # A value orders of magnitude larger than 1 indicates a poor fit or under-estimated errors
    # A value orders of magnitude less than 1 indicates over-fitting
    chiSquaredReduced2 = chiSquared2/(len(x) - 3)
    
    print(f"Order 2 regression has chi-squared of {chiSquared2:.2f}, chi-squared-reduced of {chiSquaredReduced2:.2f}")
    yearlyHddPlot(x, y, fit2, err2, 2, chiSquaredReduced2, folder=folder, color="blue")


def plotHddCumsum(data, folder, id=""):
    '''
    Plot the cumulative sum of total heating degree days.
    
    :param data: Pandas dataframe object with a "hdd" column and datetime as the indices.
    :param folder: The output directory of the plots.
    :return: None
    '''
    print(f"Plotting cumulative sum of HDD, id: {id}")
    
    # Compute the cumulative sum
    data["hdd-cumsum"] = data["hdd"].cumsum()
    data["hdd-std"] = data["hdd"].rolling(window=len(data.index), min_periods=1).std()
    data["hdd-cumsum-std"] = data["hdd-cumsum"].rolling(window=len(data.index), min_periods=1).std()
    
    
    # Plot the cumulative sum
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,5))
    
    data["hdd-cumsum"].plot(ax=ax, color="black")
    
    ax.set_ylim(min(0, data["hdd-cumsum"].min()), data["hdd-cumsum"].max())
    ax.set_xlabel("Date")
    ax.set_ylabel(r"Cumulative sum of HDD ($^\circ$F)")
    ax.legend(loc="best")
    ax.grid()
    
    plt.savefig(
        os.path.join(folder, f"hdd-cumsum-{id}.png"),
        bbox_inches = "tight",
        dpi = 300
    )
    plt.close()
    
    
    # Plot the rolling standard deviation
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,5))
    
    data["hdd-cumsum-std"].plot(ax=ax, color="black")
    
    ax.set_ylim(min(0, data["hdd-cumsum-std"].min()), data["hdd-cumsum-std"].max())
    ax.set_xlabel("Date")
    ax.set_ylabel(r"Cumulative sum of HDD ($^\circ$F)")
    ax.legend(loc="best")
    ax.grid()
    
    plt.savefig(
        os.path.join(folder, f"hdd-cumsum-std-{id}.png"),
        bbox_inches = "tight",
        dpi = 300
    )
    plt.close()