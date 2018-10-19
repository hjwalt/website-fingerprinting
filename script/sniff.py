from data.generateData import sniffData, sniffTor

from tbselenium.tbdriver import TorBrowserDriver

urlpath = "data/urls.txt"
className = "facebook"
instanceCount = 30
startingIndex = 15
endingIndex = 16

sniffData(urlpath, className, instanceCount, startingIndex, endingIndex, 15, 60, 600)

