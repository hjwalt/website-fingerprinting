import numpy
from outgoingPacketConcentration import generateFeatureFromPackets as generatePacketConcentrationFeature

def split(l, n):
    subsetSize = len(l) / n
    for i in range(n):
        yield l[(subsetSize * i):((subsetSize * i) + subsetSize)]

def generateFeature(data):
    feature = []
    dataSubset = split(data['packets'], 20)
    for subset in dataSubset:
        feature.extend(generatePacketConcentrationFeature(subset))
    return feature