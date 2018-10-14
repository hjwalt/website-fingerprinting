import os, json, time
import numpy as np

from feature.packetCount import generateFeature as generatePacketCountFeature
from feature.incomingPacketCount import generateFeature as generateIncomingPacketCountFeature
from feature.outgoingPacketCount import generateFeature as generateOutgoingPacketCountFeature
from feature.incomingPacketCountFraction import generateFeature as generateIncomingPacketCountFractionFeature
from feature.outgoingPacketCountFraction import generateFeature as generateOutgoingPacketCountFractionFeature
from feature.packetOrdering import generateFeature as generatePacketOrderingFeature
from feature.outgoingPacketConcentration import generateFeature as generateOutgoingPacketConcentrationFeature
from feature.edgePacketConcentration import generateFeature as generateEdgePacketConcentrationFeature
from feature.packetPerSecond import generateFeature as generatePacketPerSecondFeature
from feature.outgoingPacketConcentrationSubset import generateFeature as generateOutgoingPacketConcentrationSubsetFeature
from feature.packetPerSecondSubset import generateFeature as generatePacketPerSecondSubsetFeature
from feature.interArrivalTime import generateFeature as generateInterArrivalTimeFeature

from sklearn import svm
from sklearn.externals.joblib import Memory
from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from scipy.spatial.distance import hamming, cityblock, euclidean

from svm.svmTrain import get_data, accuracy

browser = "firefox"

processedpath = "data/" + browser + "/processed"
svmprocesseddata = "data/" + browser + "/extracted/p3.txt"
svmtestdata = "data/" + browser + "/extracted/t3.txt"

# Feature Extration from JSON data
jsonfiles = [f for f in os.listdir(processedpath) if os.path.isfile(os.path.join(processedpath, f))]
jsonfiles.sort()

sliceSize = 750
featureSliceSize = 750

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
                feature.extend(generateEdgePacketConcentrationFeature(data))
                feature.extend(generatePacketPerSecondFeature(data))
                feature.extend(generateOutgoingPacketConcentrationSubsetFeature(data))
                feature.extend(generatePacketPerSecondSubsetFeature(data))
                feature.extend(generateInterArrivalTimeFeature(data))
                
                if(int(data['instance']) < trainTreshold):
                    svmout.write(data['subclass'] + ' '  + ' '.join(['%d:%s' % (i+1, el) for i,el in enumerate(feature[:featureSliceSize])]) + ' # ' + data['instance'] + '\n')
                elif(int(data['instance']) < testTreshold):
                    testout.write(data['subclass'] + ' '  + ' '.join(['%d:%s' % (i+1, el) for i,el in enumerate(feature[:featureSliceSize])]) + ' # ' + data['instance'] + '\n')
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

feature_label = [
    "Total Packet Count",
    "Incoming Packet Count",
    "Outgoing Packet Count",
    "Incoming Packet Fraction",
    "Outgoing Packet Fraction",
    "Outgoing Packet Ordering Standard Deviation",
    "Outgoing Packet Ordering Mean",
    "Incoming Packet Ordering Standard Deviation",
    "Incoming Packet Ordering Mean",
    "Outgoing Packet Concentration Standard Deviation",
    "Outgoing Packet Concentration Mean",
    "Outgoing Packet Concentration Median",
    "Outgoing Packet Concentration Max",
    "Starting Packet Concentration Incoming",
    "Starting Packet Concentration Outgoing",
    "Ending Packet Concentration Incoming",
    "Ending Packet Concentration Outgoing",
    "Packet Per Second Standard Deviation",
    "Packet Per Second Mean",
    "Packet Per Second Median",
    "Packet Per Second Min",
    "Packet Per Second Max",
]

for i in range(20):
    feature_label.extend([
        "Subset " + str(i) + " Outgoing Packet Concentration Standard Deviation",
        "Subset " + str(i) + " Outgoing Packet Concentration Mean",
        "Subset " + str(i) + " Outgoing Packet Concentration Median",
        "Subset " + str(i) + " Outgoing Packet Concentration Max"
    ])

for i in range(20):
    feature_label.extend([    
        "Subset " + str(i) + " Packet Per Second Standard Deviation",
        "Subset " + str(i) + " Packet Per Second Mean",
        "Subset " + str(i) + " Packet Per Second Median",
        "Subset " + str(i) + " Packet Per Second Min",
        "Subset " + str(i) + " Packet Per Second Max",
    ])
    
feature_label.extend([
    "Inter Arrival Time Max",
    "Inter Arrival Time Mean",
    "Inter Arrival Time Standard Deviation",
    "Inter Arrival Time 75 Percentile"
])

feature_rank = []
for i in range(model.feature_importances_.shape[0]):
    feature_rank.append({"importance":model.feature_importances_[i], "label":feature_label[i]})

def takeSecond(elem):
    return elem["importance"]

feature_rank.sort(key=takeSecond, reverse=True)


justifySize = 15

print "rank".ljust(justifySize), "importance".ljust(30), "label".ljust(30)
for i in range(len(feature_label)):
    print str(i+1).ljust(justifySize), str(feature_rank[i]["importance"]).ljust(30), feature_rank[i]["label"].ljust(30)

endtime = time.time()

elapsedtime = endtime - starttime

elapsedhours = int(elapsedtime // 3600 % 24)
elapsedminutes = int(elapsedtime // 60 % 60)
elapsedseconds = int(elapsedtime % 60)

print "Training time: ", elapsedhours, " hours, ", elapsedminutes, " minutes, ", elapsedseconds, " seconds"
