import os
import numpy as np
import matplotlib.pyplot as plt

def plotYearlyHdd(data, folder):
    
    def yearlyHddPlot(x, y, fit, err, order, chiSquaredReduced, color="black"):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,5))
    
        ax.fill_between(x, fit-err, fit+err, facecolor=color, alpha=0.5, linewidth=0)
        ax.plot(x, y, "-", color="#cccccc")
        ax.plot(x, y, "o", color="black", label="HDD")
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
    
    x = data.index.values
    y = data.hdd.values
    
    # Linear regression
    (grad, intercept), cov1 = np.polyfit(x, y, 1, cov=True)
    fit1 = np.polyval((grad, intercept), x)
    err1 = np.sqrt(cov1[0][0]*x**2 + cov1[1][1] + x*(cov1[0][1]+cov1[1][0]))
    chiSquared1 = np.sum((fit1 - y)**2 / err1**2)
    chiSquaredReduced1 = chiSquared1/(len(x) - 2)
    
    print(f"Gradient has a value of {grad:.2f} +/- {np.sqrt(cov1[0][0]):.2f} F/year")
    print(f"Intercept has a value of {intercept:.2f} +/- {np.sqrt(cov1[1][1]):.2f} F")
    print(f"Order 1 regression has chi-squared of {chiSquared1:.2f}, chi-squared-reduced of {chiSquaredReduced1:.2f}")
    yearlyHddPlot(x, y, fit1, err1, 1, chiSquaredReduced1)
    
    # Regression order 2
    coeffs2, cov2 = np.polyfit(x, y, 2, cov=True)
    fit2 = np.polyval(coeffs2, x)
    err2 = np.sqrt(
        cov2[0][0]*x**4 \
      + cov2[1][1]*x**2 \
      + cov2[2][2] \
      + 2*cov2[0][1]*x**3 \
      + 2*cov2[1][2]*x \
      + 2*cov2[2][0]*x**2 \
    )
    chiSquared2 = np.sum((fit2 - y)**2 / err2**2)
    chiSquaredReduced2 = chiSquared2/(len(x) - 2)
    
    print(f"Order 2 regression has chi-squared of {chiSquared2:.2f}, chi-squared-reduced of {chiSquaredReduced2:.2f}")
    yearlyHddPlot(x, y, fit2, err2, 2, chiSquaredReduced2, color="blue")


def plotHddCumsum(data, folder, id=""):
    print(f"Plotting cumulative sum of HDD, id: {id}")
    
    data["hdd-cumsum"] = data["hdd"].cumsum()
    
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