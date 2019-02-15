import json
import os
import logging
import sys
from datetime import datetime
from pyssdb import pyssdb

CONFIG_FILE = 1
OUTPUT_DIR  = 2

ARGUMENT_LIST = [
    [CONFIG_FILE, "-f", "<config_file_name>", True]
]

def PrintUsage():

    print("\n", __file__, "\n")
    for argItem in ARGUMENT_LIST:
        if argItem[3] == True:
            print("    ", argItem[1], argItem[2])
        else:
            print("    ", argItem[1], argItem[2], "[OPTIONAL]")

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

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(thread)06d-%(levelname)s: %(message)s", datefmt="%Y%m%d-%H%M%S")

    confData = LoadConfig(args[CONFIG_FILE])
    agentConf = json.loads(confData)

    logging.info("Connecting to %s:%i (%i)...", agentConf["SSDB"]["Host"], agentConf["SSDB"]["Port"], agentConf["SSDB"]["Timeout"])
    confSSDB = pyssdb.Client(host = agentConf["SSDB"]["Host"], port = agentConf["SSDB"]["Port"], socket_timeout = agentConf["SSDB"]["Timeout"])

    logging.info("Sending credential ...")
    confSSDB.auth(agentConf["SSDB"]["Passcode"])

    agentCount = confSSDB.hsize("DNS-Agent-Status")
    logging.info("Total agent count: %d", agentCount)

    agentNameList = confSSDB.hkeys("DNS-Agent-Status", "", "", agentCount)

    for agentName in agentNameList:
        if ("ServerList" not in agentConf["SSDB"]) or (agentName.decode("utf-8") in agentConf["SSDB"]["ServerList"]):
            agentStatus = confSSDB.hget("DNS-Agent-Status", agentName)
            updateTimestamp = int(agentStatus.decode("utf-8"))
            if abs(datetime.now().timestamp() - updateTimestamp) > 600:
                statusStr = "Inactive"
            else:
                statusStr = "Active"
            updateTimeStr = datetime.fromtimestamp(updateTimestamp).strftime("%Y/%m/%d %H:%M:%S")

            agentSync = confSSDB.hget("DNS-Agent-Sync", agentName)
            if agentSync == b"Sync":
                status = "Sync"
            else:
                status = "Error"
            logging.info("%25s : %5s, %s (%s)", agentName.decode("utf-8"), status, updateTimeStr, statusStr)

    logging.info("Disconnecting from SSDB ...")
    confSSDB.disconnect()
