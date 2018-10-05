#!/usr/bin/env python

from sklearn import svm
from sklearn.externals.joblib import Memory
from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import train_test_split
import numpy as np

def get_data(pathname):
    data = load_svmlight_file(pathname)
    return data[0], data[1]

def twopowerrange(start, end):
	result = []
	for i in range(start, end):
		result.append(2 ** i)
	return result

standardkernel = "rbf"
standardcrange = twopowerrange(-5, 15)
standardgrange = twopowerrange(-15, 3)

def accuracy(yactual, ypredict):
	compare = yactual == ypredict
	return np.mean(compare)

def svmTrain2(train_pathname, test_pathname, crange = standardcrange, grange = standardgrange, kernel = standardkernel):
	xtrain, ytrain = get_data(train_pathname)
	xcrossvalidate, ycrossvalidate = get_data(test_pathname)

	currentbestp = 0
	currentbestc = 0
	currentbestg = 0

	for c in crange:
		for g in grange:
			clf = svm.SVC(C = c, gamma = g, kernel = kernel)
			clf.fit(xtrain, ytrain)
			ycrosspredict = clf.predict(xcrossvalidate)
			pcrossvalidate = accuracy(ycrossvalidate, ycrosspredict)
			print "Training with c ", c, " and g ", g, " resulting in accuracy ", pcrossvalidate
			if(pcrossvalidate > currentbestp):
				currentbestp = pcrossvalidate
				currentbestc = c
				currentbestg = g
				print "Cross Validation Accuracy : ", currentbestp * 100, "%"

	print "SVM C                     : ", currentbestc
	print "SVM Gamma                 : ", currentbestg
	print "SVM Accuracy              : ", currentbestp * 100, "%"
