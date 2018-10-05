import os, json, time
import numpy as np
from feature.packetSequence import generateFeature as generatePacketSequenceFeature

from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance

from sklearn import svm
from sklearn.externals.joblib import Memory
from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import train_test_split

from svm.svmTrain import get_data, twopowerrange, accuracy

gamma = 10
def radial_basis(x, y):
    distx = x.toarray()[0].tolist()
    disty = y.toarray()[0].tolist()
    return np.exp(-gamma * np.power(normalized_damerau_levenshtein_distance(distx, disty), 2))

def proxy_kernel(X, Y, K=radial_basis):
    """Another function to return the gram_matrix,
    which is needed in SVC's kernel or fit
    """
    gram_matrix = np.zeros((X.shape[0], Y.shape[0]))
    for i, x in enumerate(X):
        for j, y in enumerate(Y):
            gram_matrix[i, j] = K(x, y)
    return gram_matrix

processedpath = "data/processed"
svmprocesseddata = "data/svm/p2.txt"
svmtestdata = "data/svm/t2.txt"

# Feature Extration from JSON data
jsonfiles = [f for f in os.listdir(processedpath) if os.path.isfile(os.path.join(processedpath, f))]
jsonfiles.sort()

sliceSize = 100

trainTreshold = 20
testTreshold = 30

print "Extract feature"

with open(svmprocesseddata, 'w') as svmout:
    with open(svmtestdata, 'w') as testout:
        for filename in jsonfiles:
            jsonfilepath = os.path.join(processedpath, filename)
            with open(jsonfilepath) as f:
                data = json.load(f)

                data['packets'] = data['packets'][:sliceSize]

                feature = []
                feature.extend(generatePacketSequenceFeature(data))

                if(int(data['instance']) < trainTreshold):
                    svmout.write(data['subclass'] + ' '  + ' '.join(['%d:%s' % (i+1, el) for i,el in enumerate(feature[:sliceSize])]) + ' # ' + data['instance'] + '\n')
                elif(int(data['instance']) < testTreshold):
                    testout.write(data['subclass'] + ' '  + ' '.join(['%d:%s' % (i+1, el) for i,el in enumerate(feature[:sliceSize])]) + ' # ' + data['instance'] + '\n')
                else:
                    continue

print "Train and test"

starttime = time.time()

train_pathname = svmprocesseddata
test_pathname = svmtestdata

crange = twopowerrange(-2, 15)
grange = twopowerrange(-2, 5)

xtrain, ytrain = get_data(train_pathname)
xcrossvalidate, ycrossvalidate = get_data(test_pathname)

currentbestp = 0
currentbestc = 0
currentbestg = 0

for c in crange:
    for g in grange:
        gamma = g
        clf = svm.SVC(C = c, gamma = g, kernel = proxy_kernel)
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

endtime = time.time()

elapsedtime = endtime - starttime

elapsedhours = int(elapsedtime // 3600 % 24)
elapsedminutes = int(elapsedtime // 60 % 60)
elapsedseconds = int(elapsedtime % 60)

print "Training time: ", elapsedhours, " hours, ", elapsedminutes, " minutes, ", elapsedseconds, " seconds"
