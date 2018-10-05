def generateFeature(data):
    feature = []
    for packet in data['packets']:
        currentFeature = 0
        if(packet['direction'] == "response"):
            currentFeature += int(packet['size'])
        else:
            currentFeature -= int(packet['size'])
        feature.append(currentFeature)
    return feature