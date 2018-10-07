from data.extractPcap import parseAndGenerateJson

browser = "firefox"

path = "data/" + browser + "/raw"
processedpath = "data/" + browser + "/processed"

localSource = "192.168.0.0/16"
facebookTarget = ["31.13.0.0/16", "157.240.0.0/16"]

parseAndGenerateJson(path, processedpath,localSource,facebookTarget)
