import os, json, time
import numpy as np

from feature.packetCount import generateFeature as generatePacketCountFeature
from feature.incomingPacketCount import generateFeature as generateIncomingPacketCountFeature
from feature.outgoingPacketCount import generateFeature as generateOutgoingPacketCountFeature
from feature.incomingPacketCountFraction import generateFeature as generateIncomingPacketCountFractionFeature
from feature.outgoingPacketCountFraction import generateFeature as generateOutgoingPacketCountFractionFeature
from feature.packetOrdering import generateFeature as generatePacketOrderingFeature
from feature.outgoingPacketConcentration import generateFeature as generateOutgoingPacketConcentrationFeature

from sklearn import svm
from sklearn.externals.joblib import Memory
from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from scipy.spatial.distance import hamming, cityblock, euclidean

from svm.svmTrain import get_data, accuracy

processedpath = "data/processed"
svmprocesseddata = "data/extracted/p3.txt"
svmtestdata = "data/extracted/t3.txt"

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
                feature.extend(generatePacketCountFeature(data))
                feature.extend(generateIncomingPacketCountFeature(data))
                feature.extend(generateOutgoingPacketCountFeature(data))
                feature.extend(generateIncomingPacketCountFractionFeature(data))
                feature.extend(generateOutgoingPacketCountFractionFeature(data))
                feature.extend(generatePacketOrderingFeature(data))
                feature.extend(generateOutgoingPacketConcentrationFeature(data))
                
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

xtrain, ytrain = get_data(train_pathname)
xcrossvalidate, ycrossvalidate = get_data(test_pathname)

model = RandomForestClassifier(n_estimators=1000, oob_score = True)
model.fit(xtrain, ytrain)

train_leaf = zip(model.apply(xtrain), ytrain)
test_leaf = zip(model.apply(xcrossvalidate), ycrossvalidate)

trueCount = 0
falseCount = 0

for i, instance in enumerate(test_leaf):
    temp = []
    for item in train_leaf:
        d = hamming(item[0], instance[0])
        if d == 1.0:
            continue
        temp.append((d, instance[1], item[1]))
    tops = sorted(temp)[:10]
    
    if(tops[0][1] == tops[0][2]):
        trueCount += 1
    else:
        falseCount += 1

hammingAccuracy = float(trueCount) / (trueCount + falseCount)
print "Accuracy ", hammingAccuracy * 100, "%"

endtime = time.time()

elapsedtime = endtime - starttime

elapsedhours = int(elapsedtime // 3600 % 24)
elapsedminutes = int(elapsedtime // 60 % 60)
elapsedseconds = int(elapsedtime % 60)

print "Training time: ", elapsedhours, " hours, ", elapsedminutes, " minutes, ", elapsedseconds, " seconds"
