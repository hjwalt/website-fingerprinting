from data.generateData import sniffData
from parser.extractPcap import parseAndGenerateJson

urlpath = "data/urls.txt"
className = "facebook"
instanceCount = 30
startingIndex = 20
endingIndex = 25

#sniffData(urlpath, className, instanceCount, startingIndex, endingIndex, 15, 60, 600)

path = "data/automated"
processedpath = "data/processed"

localSource = "192.168.0.0/16"
facebookTarget = ["31.13.0.0/16", "157.240.0.0/16"]

# Generate JSON Data
parseAndGenerateJson(path, processedpath,localSource,facebookTarget)
