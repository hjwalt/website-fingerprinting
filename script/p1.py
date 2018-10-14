import os, json, time

from feature.cumulativePacket import generateFeature as generateCumulativePacketFeature
from feature.incomingPacketCount import generateFeature as generateIncomingPacketCountFeature
from feature.outgoingPacketCount import generateFeature as generateOutgoingPacketCountFeature
from feature.incomingPacketSize import generateFeature as generateIncomingPacketSizeFeature
from feature.outgoingPacketSize import generateFeature as generateOutgoingPacketSizeFeature
from svm.svmTrain import svmTrain2, twopowerrange

browser = "firefox"

processedpath = "data/" + browser + "/processed"
svmprocesseddata = "data/" + browser + "/extracted/p1.txt"
svmtestdata = "data/" + browser + "/extracted/t1.txt"

# Feature Extration from JSON data
jsonfiles = [f for f in os.listdir(processedpath) if os.path.isfile(os.path.join(processedpath, f))]
jsonfiles.sort()

sliceSize = 104

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
                feature.extend(generateIncomingPacketCountFeature(data))
                feature.extend(generateOutgoingPacketCountFeature(data))

                feature.extend(generateIncomingPacketSizeFeature(data))
                feature.extend(generateOutgoingPacketSizeFeature(data))

                feature.extend(generateCumulativePacketFeature(data))
                if(int(data['instance']) < trainTreshold):
                    svmout.write(data['subclass'] + ' '  + ' '.join(['%d:%s' % (i+1, el) for i,el in enumerate(feature[:sliceSize])]) + ' # ' + data['instance'] + '\n')
                elif(int(data['instance']) < testTreshold):
                    testout.write(data['subclass'] + ' '  + ' '.join(['%d:%s' % (i+1, el) for i,el in enumerate(feature[:sliceSize])]) + ' # ' + data['instance'] + '\n')
                else:
                    continue

print "Train and test"

starttime = time.time()

p1crange = twopowerrange(11, 18)
p1grange = twopowerrange(-3, 4)

#svmTrain(svmprocesseddata, True, svmtestdata)
svmTrain2(svmprocesseddata, svmtestdata, crange=p1crange, grange=p1grange)

endtime = time.time()

elapsedtime = endtime - starttime

elapsedhours = int(elapsedtime // 3600 % 24)
elapsedminutes = int(elapsedtime // 60 % 60)
elapsedseconds = int(elapsedtime % 60)

print "Training time: ", elapsedhours, " hours, ", elapsedminutes, " minutes, ", elapsedseconds, " seconds"
