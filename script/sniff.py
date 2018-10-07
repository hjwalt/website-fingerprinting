from data.generateData import sniffData, sniffTor

from tbselenium.tbdriver import TorBrowserDriver

browser = TorBrowserDriver("/home/dev/tor-browser")
browser.profile.set_preference("browser.cache.disk.enable", False)
browser.profile.set_preference("browser.cache.memory.enable", False)
browser.profile.set_preference("browser.cache.offline.enable", False)
browser.profile.set_preference("network.http.use-cache", False)
browser.profile.set_preference("network.cookie.cookieBehavior", 2)
browser.load_url("https://facebook.com")

exit()

urlpath = "data/urls.txt"
className = "facebook"
instanceCount = 30
startingIndex = 0
endingIndex = 25

sniffTor(urlpath, className, instanceCount, startingIndex, endingIndex, 15, 60, 600)

