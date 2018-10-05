def generateFeature(data):
    feature = []
    cumulative = 0
    for packet in data['packets']:
        if(packet['direction'] == "response"):
            cumulative += int(packet['size'])
        else:
            cumulative -= int(packet['size'])
        feature.append(cumulative)
    return feature