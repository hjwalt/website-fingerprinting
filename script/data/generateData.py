import thread, threading, inspect, ctypes, time, subprocess, shlex

from scapy.all import sniff
from selenium import webdriver

class BrowserThread(threading.Thread):
    def __init__(self, name, url):
        threading.Thread.__init__(self)
        self.name = name
        self.url = url

    def terminate(self):
        self.browser.quit()

    def run(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)
        profile.set_preference("network.cookie.cookieBehavior", 2)
        self.browser = webdriver.Firefox(profile)
        self.browser.get(self.url)

def generateData(url, filename, delay):
    print "Starting capture"
    thread1 = subprocess.Popen(shlex.split("tcpdump 'tcp' -w " + filename))

    thread2 = BrowserThread("Thread-2", url)
    thread2.start()

    time.sleep(delay)

    print "Terminating threads"

    thread2.terminate()
    thread2.join()

    thread1.terminate()

    print "Ending capture"

def sniffData(urlpath, className, instanceCount, startingIndex, endingIndex, instanceWait, instanceDelay, urlDelay):
    with open(urlpath) as f:
        i = 0
        for url in f:
            if(i < startingIndex):
                i += 1
                continue
            print "Generating data for ", url
            for j in range(0, instanceCount):
                generateData(url, "data/automated/" + className + "-" + str(i) + "-" + str(j) + ".pcapng", instanceWait)
                time.sleep(instanceDelay)
            time.sleep(urlDelay)
            i += 1
            if(i == endingIndex):
                break
