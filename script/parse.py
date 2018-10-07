from data.extractPcap import parseAndGenerateJson

browser = "tor"

path = "data/" + browser + "/raw"
processedpath = "data/" + browser + "/processed"

localSource = "192.168.0.0/16"
facebookTarget = ["0.0.0.0/32"]

parseAndGenerateJson(path, processedpath,localSource,facebookTarget)
