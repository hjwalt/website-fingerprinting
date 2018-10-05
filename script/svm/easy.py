#!/usr/bin/env python

import sys, os
from svmTrain import svmTrain
from subprocess import *

if len(sys.argv) <= 1:
	print('Usage: {0} training_file [testing_file]'.format(sys.argv[0]))
	raise SystemExit

# svm, grid, and gnuplot executable files

execute_testing = len(sys.argv) > 2

train_pathname = sys.argv[1]
test_pathname = ""

if(execute_testing):
	test_pathname = sys.argv[2]

svmTrain(train_pathname, execute_testing, test_pathname)
