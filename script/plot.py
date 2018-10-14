import os, json, time
import numpy as np

from svm.svmTrain import get_data, twopowerrange, accuracy

import matplotlib.pyplot as plt
from visual.plot import plot, transform

from sklearn.preprocessing import normalize

browser = "firefox"
paper = "3"

processedpath = "data/" + browser + "/processed"
svmprocesseddata = "data/" + browser + "/extracted/p" + paper + ".txt"
svmtestdata = "data/" + browser + "/extracted/t" + paper + ".txt"

train_pathname = svmprocesseddata

# Plot data
xtrain, ytrain = get_data(train_pathname)
filename = "data/" + browser + "/plot/p" + paper + "-all.png"
j = 5
for i in range(25):
    print "Plotting index ", i
    plotx, ploty = transform(xtrain[(20*i) + j])
    plt.plot(plotx, ploty)

plt.savefig(filename)
plt.clf()

# Plot data normalized
xtrain, ytrain = get_data(train_pathname)
xtrain = normalize(xtrain, axis=0)
filename = "data/" + browser + "/plot/p" + paper + "-all-normalized.png"
j = 5
for i in range(25):
    print "Plotting index ", i
    plotx, ploty = transform(xtrain[(20*i) + j])
    plt.plot(plotx, ploty)

plt.savefig(filename)
plt.clf()

# Plot one class
xtrain, ytrain = get_data(train_pathname)
for j in range(25):
    print "Plotting index ", j
    filename = "data/" + browser + "/plot/p" + paper + "-c" + str(j) + ".png"
    for i in range(20):
        plotx, ploty = transform(xtrain[(20 * j) + i])
        plt.plot(plotx, ploty)

    plt.savefig(filename)
    plt.clf()


# Plot one class normalized
xtrain, ytrain = get_data(train_pathname)
xtrain = normalize(xtrain, axis=0)
for j in range(25):
    print "Plotting index ", j
    filename = "data/" + browser + "/plot/p" + paper + "-c" + str(j) + "-normalized.png"
    for i in range(20):
        plotx, ploty = transform(xtrain[(20 * j) + i])
        plt.plot(plotx, ploty)

    plt.savefig(filename)
    plt.clf()
