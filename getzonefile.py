import json
import os
import logging
import sys
from pyssdb import pyssdb
import dns.zone

CONFIG_FILE  = 1
OUTPUT_DIR   = 2
OUTPUT_COUNT = 3

ARGUMENT_LIST = [
    [CONFIG_FILE, "-f", "<config_file_name>", True],
    [OUTPUT_DIR, "-o", "<output_directory>", True],
    [OUTPUT_COUNT, "-c", "<output_count>", False]
]

def PrintUsage():

    print("\n", __file__, "\n")
    for argItem in ARGUMENT_LIST:
        if argItem[3] == True:
            print("    ", argItem[1], argItem[2])
        else:
            print("    ", argItem[1], argItem[2], "[OPTIONAL]")
    print("")

def GetArguments(argv):

    arguments = dict()
    idx, argc = 0, len(argv)

    while idx < argc:
        for argItem in ARGUMENT_LIST:
            if (argv[idx] == argItem[1]) and (idx < argc - 1):
                idx = idx + 1
                arguments[argItem[0]] = argv[idx]
        idx = idx + 1

    for argItem in ARGUMENT_LIST:
        if (argItem[3] == True) and (argItem[0] not in arguments):
            PrintUsage()
            exit(0)

    return arguments

def LoadConfig(filename):

    fd = open(filename)
    data = fd.read()
    fd.close()

    return data


def DisplayZoneContent(zoneString, originName):

    zone = dns.zone.from_text(zoneString, origin = originName)

    for (name, ttl, rdata) in zone.iterate_rdatas():
        logging.info("%10s %8d %3d %s", name.to_text(), ttl, rdata.extended_rdatatype(), rdata.to_text())


if __name__ == '__main__':

    args = GetArguments(sys.argv)

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(thread)06d-%(levelname)s: %(message)s", datefmt="%Y%m%d-%H%M%S")

    confData = LoadConfig(args[CONFIG_FILE])
    agentConf = json.loads(confData)

    if OUTPUT_COUNT in args:
        outputCount = args[OUTPUT_COUNT]
    else:
        outputCount = 0

    try:

        logging.info("Connecting to %s:%i(%i) ...", agentConf["SSDB"]["Host"], agentConf["SSDB"]["Port"], agentConf["SSDB"]["Timeout"])
        confSSDB = pyssdb.Client(host = agentConf["SSDB"]["Host"], port = agentConf["SSDB"]["Port"], socket_timeout = agentConf["SSDB"]["Timeout"])

        logging.info("Sending credential ...")
        confSSDB.auth(agentConf["SSDB"]["Passcode"])

        zoneCount = confSSDB.hsize("DNS-Zones")
        logging.info("Total zone file: %d", zoneCount)

        if outputCount != 0:
            zoneCount = outputCount

        zoneNameList = confSSDB.hkeys("DNS-Zones", "", "", zoneCount)

        for zoneName in zoneNameList:
            zoneContent = confSSDB.hget("DNS-Zones", zoneName.decode("utf-8"))
            outputFile = os.path.join(args[OUTPUT_DIR], zoneName.decode("utf-8") + "zone")
            logging.info("  Output %s to %s", zoneName.decode("utf-8"), outputFile)
    
            zonefd = open(outputFile, mode = "wt")
            zonefd.write(zoneContent.decode("utf-8"))
            zonefd.close()

            DisplayZoneContent(zoneContent.decode("utf-8"), zoneName.decode("utf-8"))

            logging.info("-------------------------------------------------------------------------")

    except Exception as ex:
        print(ex)

    finally:
        if confSSDB != None:
            logging.info("Disconnecting from SSDB ...")
            confSSDB.disconnect()
