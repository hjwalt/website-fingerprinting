def generateFeature(data):
    feature = []
    count = 0
    for packet in data['packets']:
        if(packet['direction'] == "request"):
            count += 1
    feature.append(count)
    return feature