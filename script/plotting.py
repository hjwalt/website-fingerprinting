import os, json, time
import numpy as np

from svm.svmTrain import get_data, twopowerrange, accuracy

import matplotlib.pyplot as plt
from visual.plot import plot, transform

processedpath = "data/processed"
svmprocesseddata = "data/svm/p2.txt"
svmtestdata = "data/svm/t2.txt"

# Feature Extration from JSON data
sliceSize = 100

train_pathname = svmprocesseddata
test_pathname = svmtestdata

xtrain, ytrain = get_data(train_pathname)

filename = "data/plot/all-p2.png"

for i in range(25):
    print "Plotting index ", i
    plotx, ploty = transform(xtrain[20*i], 100)
    plt.plot(plotx, ploty)

plt.savefig(filename)
plt.clf()