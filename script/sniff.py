from data.generateData import sniffData, sniffTor

from tbselenium.tbdriver import TorBrowserDriver

urlpath = "data/urls.txt"
className = "facebook"
instanceCount = 30
startingIndex = 0
endingIndex = 25

sniffTor(urlpath, className, instanceCount, startingIndex, endingIndex, 30, 60, 600)

