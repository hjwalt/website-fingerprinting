from extractCommon import comparableAddress, addressInNetwork
import os, re
import datetime as dt
from scapy.all import rdpcap

def parsePcap(filename, sourceAddress, targetAddressList):
    subnetSource = comparableAddress(sourceAddress)
    
    filenamebase = os.path.basename(filename)
    filenamenoextension = re.sub(r'\.[a-zA-Z]+\Z', '', filenamebase)
    filenamesplit = filenamenoextension.split('-')

    fileclass = filenamesplit[0]
    filesubclass = filenamesplit[1]
    fileinstance = filenamesplit[2]

    requestCount = 0
    responseCount = 0

    packets = []
    
    consecutiveRequest = False
    consecutiveResponse = False

    consecutiveCount = 0

    for pkt in rdpcap(filename):
        #print str(dir(pkt))
        #print pkt.time
        #print pkt.name

        #print pkt.payload.time
        #print pkt.payload.src
        #print pkt.payload.dst
        #print pkt.payload.name
        #print pkt.payload.ttl

        #print pkt.payload.payload.name

        if pkt.name != 'Ethernet':
            continue

        if pkt.payload.name != 'IP':
            continue

        if pkt.payload.payload.name != 'TCP':
            continue
            
        srcIp = pkt.payload.src
        dstIp = pkt.payload.dst
        
        direction = "unknown"

        included = False
        for targetAddress in targetAddressList:
            subnetTarget = comparableAddress(targetAddress)
            if(addressInNetwork(comparableAddress(srcIp), subnetSource) and addressInNetwork(comparableAddress(dstIp), subnetTarget)):
                included = True
                direction = "request"
                requestCount += 1
                break
            elif(addressInNetwork(comparableAddress(dstIp), subnetSource) and addressInNetwork(comparableAddress(srcIp), subnetTarget)):
                included = True
                direction = "response"
                responseCount += 1
                break
        if not included:
            continue
        
        if(len(pkt.payload) < 60):
            continue

        currentConsecutvePacket = consecutiveCount

        if(direction == "request"):
            if(consecutiveRequest):
                consecutiveCount += 1
            else:
                consecutiveRequest = True
                consecutiveCount = 1
        
        if(direction == "response"):
            if(consecutiveResponse):
                consecutiveCount += 1
            else:
                consecutiveResponse = True
                consecutiveCount = 1

        row = {
            'size' : len(pkt.payload),
            'direction' : direction,
            'timestamp' : str(dt.datetime.utcfromtimestamp(pkt.time)),
            'consecutivePacket': currentConsecutvePacket
        }

        packets.append(row)
    
    data = {
        'packets' : packets,
        'class' : fileclass,
        'subclass' : filesubclass,
        'instance' : fileinstance,
        'request' : requestCount,
        'response' : responseCount
    }
    return data

