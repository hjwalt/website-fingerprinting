from data.generateData import sniffData, sniffTor

urlpath = "data/urls.txt"
className = "facebook"
instanceCount = 30
startingIndex = 0
endingIndex = 25

sniffTor(urlpath, className, instanceCount, startingIndex, endingIndex, 15, 60, 600)

