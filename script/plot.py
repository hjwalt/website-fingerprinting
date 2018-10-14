import os, json, time
import numpy as np

from svm.svmTrain import get_data, twopowerrange, accuracy

import matplotlib.pyplot as plt
from visual.plot import plot, transform

browser = "firefox"
paper = "3"

processedpath = "data/" + browser + "/processed"
svmprocesseddata = "data/" + browser + "/extracted/p" + paper + ".txt"
svmtestdata = "data/" + browser + "/extracted/t" + paper + ".txt"

train_pathname = svmprocesseddata
test_pathname = svmtestdata

xtrain, ytrain = get_data(train_pathname)

filename = "data/" + browser + "/plot/all-p" + paper + ".png"

for i in range(25):
    print "Plotting index ", i
    plotx, ploty = transform(xtrain[20*i])
    plt.plot(plotx, ploty)

plt.savefig(filename)
plt.clf()