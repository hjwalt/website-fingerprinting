from extractCommon import comparableAddress, addressInNetwork
import os, re
import datetime as dt
import dpkt

def parsePcap(filename, sourceAddress, targetAddress):
    subnetSource = comparableAddress(sourceAddress)
    subnetTarget = comparableAddress(targetAddress)
    
    filenamebase = os.path.basename(filename)
    filenamenoextension = re.sub(r'\.[a-zA-Z]+\Z', '', filenamebase)
    filenamesplit = filenamenoextension.split('-')

    fileclass = filenamesplit[0]
    filesubclass = filenamesplit[1]
    fileinstance = filenamesplit[2]

    requestCount = 0
    responseCount = 0

    packets = []

    for ts, pkt in dpkt.pcap.Reader(open(filename)):
        eth = dpkt.ethernet.Ethernet(pkt) 

        if eth.type != dpkt.ethernet.ETH_TYPE_IP:
            continue

        ip = eth.data

        if ip.p != dpkt.ip.IP_PROTO_TCP:
            continue
        
        srcIp = '.'.join(str(x) for x in bytearray(ip.src))
        #dstIp = '.'.join(str(x) for x in bytearray(ip.dst))
        
        direction = "unknown"

        if(addressInNetwork(comparableAddress(srcIp), subnetSource)):
            direction = "request"
            requestCount += 1
        
        if(addressInNetwork(comparableAddress(srcIp), subnetTarget)):
            direction = "response"
            responseCount += 1

        if(direction == "unknown"):
            continue

        row = {
            'size' : ip.len,
            'direction' : direction,
            'timestamp' : str(dt.datetime.utcfromtimestamp(ts))
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
