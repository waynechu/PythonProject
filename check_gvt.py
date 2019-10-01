import json
import os
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from pyssdb import pyssdb

CONFIG_FILE = 0

ARGUMENT_LIST = [
    [CONFIG_FILE, "-f", "<config_file_name>", True],
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

if __name__ == '__main__':

    args = GetArguments(sys.argv)

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(levelname)s: %(message)s", datefmt="%Y%m%d-%H%M%S")
    logger = logging.getLogger("agent")
    fileHandler = TimedRotatingFileHandler("output.txt", when="midnight", interval=1, backupCount=5)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(logging.Formatter("%(asctime)s-%(levelname)s: %(message)s", datefmt="%y/%m/%d-%H:%M:%S"), )
    logger.addHandler(fileHandler)

    conf = LoadConfig(args[CONFIG_FILE])
    confData = json.loads(conf)

    try:

        logging.info("Connecting to %s:%i(%i) ...", confData["SSDB"]["Host"], confData["SSDB"]["Port"], confData["SSDB"]["Timeout"])
        ssdbConf = pyssdb.Client(host = confData["SSDB"]["Host"], port = confData["SSDB"]["Port"], socket_timeout = confData["SSDB"]["Timeout"])
        logging.info("Connection established -- OK")

        if ("Passcode" in confData["SSDB"]):
            logging.info("Sending credential ...")
            ssdbConf.auth(confData["SSDB"]["Passcode"])
            logging.info("Credential authenticated -- OK")

        itemCount = ssdbConf.hsize("DNS-Group-Info")

        if itemCount > 0:
            groupInfoList = ssdbConf.hkeys("DNS-Group-Info", "", "", itemCount)
            for groupInfo in groupInfoList:
                if groupInfo.decode("utf-8") != "CDD_1135":
                    continue

                logger.info(groupInfo.decode("utf-8"))

                data = ssdbConf.hget("DNS-Group-Info", groupInfo.decode("utf-8"))

                zoneConf = json.loads(data.decode("utf-8"))
                zoneIdx = 0
                itemCount = 0
                for zone in zoneConf["zones"]:
                    zoneName = zone["name"]
                    zoneIdx = zoneIdx + 1
                    ipIdx = 0
                    dnsIP = []
                    for dnsInfo in zone["dns_info"]:
                        dnsIP.append(dnsInfo["server"]) 
                        ipIdx = ipIdx + 1
                        itemCount = itemCount + 1

                    if ipIdx == 2 and dnsIP[0] == "160.96.26.11" and dnsIP[1] == "160.96.236.131":
                        continue
                    if ipIdx == 2 and dnsIP[0] == "160.96.236.131" and dnsIP[1] == "160.96.26.11":
                        continue

                    if ipIdx == 1:
                        logger.info("    %d,%s,%s", zoneIdx, zoneName, dnsIP[0])
                    elif ipIdx == 2:
                        logger.info("    %d,%s,%s,%s", zoneIdx, zoneName, dnsIP[0], dnsIP[1])
                    else:
                        logger.info("    %d,%s", zoneIdx, zoneName)

    except Exception as ex:
        print(ex)

    finally:
        if ssdbConf != None:
            logging.info("Disconnecting from SSDB ...")
            ssdbConf.disconnect()
        logging.info("Finish -- OK")
