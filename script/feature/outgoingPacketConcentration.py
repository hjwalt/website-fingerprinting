import numpy

def generateFeatureFromPackets(packets):
    feature = []
    dataLength = len(packets)
    chunkSize = 20
    chunkCount = dataLength / chunkSize
    outgoingPacketCountInChunk = []
    for i in range(chunkCount):            
        currentChunkCount = 0
        for j in range(chunkSize):
            dataIndex = (i * chunkSize) + j
            if(packets[dataIndex]['direction'] == "request"):    
                currentChunkCount += 1
        outgoingPacketCountInChunk.append(currentChunkCount)
    feature.append(numpy.std(outgoingPacketCountInChunk))
    feature.append(numpy.mean(outgoingPacketCountInChunk))
    feature.append(numpy.median(outgoingPacketCountInChunk))
    feature.append(numpy.max(outgoingPacketCountInChunk))
    return feature

def generateFeature(data):
    return generateFeatureFromPackets(data['packets'])