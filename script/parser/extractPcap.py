from parser.extractPcapScapy import parsePcap as parsePcapScapy
from parser.extractPcapDpkt import parsePcap as parsePcapDpkt
import os, re, json

justifySize = 15

def parseAndGenerateJson(path, processedpath, sourceip, targetip):
    filesinpath = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    filesinpath.sort()

    print "class".ljust(justifySize), "subclass".ljust(justifySize), "instance".ljust(justifySize), "packet count"
    for filename in filesinpath:
        filefullpath = os.path.join(path, filename)
        
        # get new file name with json extension
        jsonfilename = re.sub(r'\.[a-zA-Z]+\Z', '.json', filename)
        jsonfilepath = os.path.join(processedpath, jsonfilename)

        parsed = parsePcapScapy(filefullpath, sourceip, targetip)

        print parsed['class'].ljust(justifySize), parsed['subclass'].ljust(justifySize), parsed['instance'].ljust(justifySize), len(parsed['packets'])

        with open(jsonfilepath, 'w') as outfile:
            json.dump(parsed, outfile, indent = 2)
