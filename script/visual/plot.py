import numpy as np
import matplotlib.pyplot as plt

def transform(y):
    appy = []
    for i in range(y.T.shape[0]):
        appy.append(y.T[i,0])
    plotx = np.arange(len(appy))
    ploty = np.array(appy)
    return plotx, ploty

def plot(y, featureSize, filename):
    plotx, ploty = transform(y)
    plt.plot(plotx, ploty)
    plt.savefig(filename)
    plt.clf()