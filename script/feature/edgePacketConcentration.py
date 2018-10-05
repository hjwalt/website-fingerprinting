import numpy

def generateFeature(data):
    feature = []
    dataLength = len(data["packets"])
    chunkSize = 30
    firstIncoming = 0
    firstOutgoing = 0
    lastIncoming = 0
    lastOutgoing = 0
    for i in range(chunkSize):
        firstIndex = i
        lastIndex = dataLength - i -1

        if(data["packets"][firstIndex]['direction'] == "request"):    
            firstOutgoing += 1
        else:
            firstIncoming += 1

        if(data["packets"][lastIndex]['direction'] == "response"):    
            lastOutgoing += 1
        else:
            lastIncoming += 1
    feature.append(firstIncoming)
    feature.append(firstOutgoing)
    feature.append(lastIncoming)
    feature.append(lastOutgoing)
    return feature