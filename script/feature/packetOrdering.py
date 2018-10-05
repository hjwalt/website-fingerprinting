import numpy

def generateFeature(data):
    feature = []

    consecutivePacketsOutgoing = []
    consecutivePacketsIncoming = []
    for packet in data['packets']:
        if(packet['direction'] == "response"):
            consecutivePacketsIncoming.append(packet['consecutivePacket'])
        else:
            consecutivePacketsOutgoing.append(packet['consecutivePacket'])
    
    feature.append(numpy.std(consecutivePacketsOutgoing))
    feature.append(numpy.mean(consecutivePacketsOutgoing))
    feature.append(numpy.std(consecutivePacketsIncoming))
    feature.append(numpy.mean(consecutivePacketsIncoming))
    
    return feature