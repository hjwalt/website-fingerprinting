def generateFeature(data):
    feature = []
    size = 0
    for packet in data['packets']:
        if(packet['direction'] == "request"):
            size += packet['size']
    feature.append(size)
    return feature