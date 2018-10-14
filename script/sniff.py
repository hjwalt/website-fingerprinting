from data.generateData import sniffData, sniffTor

from tbselenium.tbdriver import TorBrowserDriver

urlpath = "data/urls.txt"
className = "facebook"
instanceCount = 30
startingIndex = 8
endingIndex = 11

sniffTor(urlpath, className, instanceCount, startingIndex, endingIndex, 30, 60, 600)

