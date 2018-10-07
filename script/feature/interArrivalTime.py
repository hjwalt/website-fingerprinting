import numpy
import time

def generateFeatureFromPackets(packets):
    feature = []

    lastArrival = -1
    interArrivalTime = []

    for packet in packets:
        #2018-09-15 16:00:30.099882
        timeStampTime = 0
        try:
            timeStampTime = time.strptime(packet['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
        except:
            timeStampTime = time.strptime(packet['timestamp'], "%Y-%m-%d %H:%M:%S")

        timeFloat = time.mktime(timeStampTime)
        if(lastArrival != -1):
            interArrivalTime.append(timeFloat - lastArrival)

        lastArrival = timeFloat
    
    feature.append(numpy.max(interArrivalTime))
    feature.append(numpy.mean(interArrivalTime))
    feature.append(numpy.std(interArrivalTime))
    feature.append(numpy.percentile(interArrivalTime, 75))
        
    return feature

def generateFeature(data):
    return generateFeatureFromPackets(data['packets'])