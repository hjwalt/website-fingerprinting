def generateFeature(data):
    feature = []
    count = 0
    for packet in data['packets']:
        if(packet['direction'] == "response"):
            count += 1
    fraction = float(count) / len(data["packets"])
    feature.append(fraction)
    return feature