import json
import os
import logging
import sys
from datetime import datetime
from pyssdb import pyssdb

CONF_AGENT_STATUS = "DNS-Agent-Status"
CONF_AGENT_SYNC = "DNS-Agent-Sync"

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

class ConfSSDB:
    def __init__(self, host, port, timeout = 10, passCode = None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.passCode = passCode
        self.ssdb = None
        self.Connect()

    def Connect(self):
        if self.ssdb == None:
            try:
                logging.info("Connecting to %s:%i (%i)...", self.host, self.port, self.timeout)
                self.ssdb = pyssdb.Client(host = self.host, port = self.port, socket_timeout = self.timeout)
                logging.info("Sending credential ...")
                self.ssdb.auth(self.passCode)
            except Exception as ex:
                logging.warning("Connect exception: %s", ex.args[0])
                self.Disconnect()

    def Disconnect(self):
        if self.ssdb != None:
            try:
                self.ssdb.disconnect()
            except Exception as ex:
                logging.warning("Disconnect exception: %s", ex.args[0])
            self.ssdb = None
        else:
            logging.warning("SSDB instence is None")

    def GetAgentCount(self):
        if self.ssdb != None:
            try:
                return self.ssdb.hsize(CONF_AGENT_STATUS)
            except Exception as ex:
                logging.warning("Get agent count exception: %s", ex.args[0])
        else:
            logging.warning("SSDB instence is None")

    def CheckAgentStatus(self, serverList = None):
        if self.ssdb != None:
            try:
                agentCount = self.GetAgentCount()

                agentNameList = self.ssdb.hkeys(CONF_AGENT_STATUS, "", "", agentCount)

                for agentName in agentNameList:

                    if (serverList == None) or (agentName.decode("utf-8") in serverList):

                        updateTimestamp = int(self.ssdb.hget(CONF_AGENT_STATUS, agentName).decode("utf-8"))
                        updateTimeStr = datetime.fromtimestamp(updateTimestamp).strftime("%Y/%m/%d %H:%M:%S")
                        if datetime.now().timestamp() - updateTimestamp > 600:
                            statusStr = "Out-of-date"
                        else:
                            statusStr = "Active"

                        if self.ssdb.hget(CONF_AGENT_SYNC, agentName) == b"Sync":
                            syncMsg = "Sync"
                        else:
                            syncMsg = "Error"

                        logging.info("%20s : %s (%s, %s)", agentName.decode("utf-8"), updateTimeStr, statusStr, syncMsg)

            except Exception as ex:
                logging.warning("Check agent status exception: %s", ex.args[0])
        else:
            logging.warning("SSDB instence is None")

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(thread)06d-%(levelname)s: %(message)s", datefmt="%Y%m%d-%H%M%S")

    # Get arguments and load configure file
    args = GetArguments(sys.argv)
    content = LoadConfig(args[CONFIG_FILE])
    agentConf = json.loads(content)

    confDB = ConfSSDB(agentConf["SSDB"]["Host"], agentConf["SSDB"]["Port"], agentConf["SSDB"]["Timeout"], agentConf["SSDB"]["Passcode"])

    if "ServerList" in agentConf["SSDB"]:
        serverList = agentConf["SSDB"]["ServerList"]
    else:
        serverList = None

    confDB.CheckAgentStatus(serverList)

    logging.info("Disconnecting from SSDB ...")
    confDB.Disconnect()
