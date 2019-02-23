import json
import os
import logging
import sys
import time
import sched
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from pyssdb import pyssdb

CONF_AGENT_STATUS = "DNS-Agent-Status"
CONF_AGENT_SYNC = "DNS-Agent-Sync"

CONFIG_FILE = 1

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

def ReadConfigFile(filename):

    fd = open(filename)
    data = fd.read()
    fd.close()

    return data

def ConfigDebugLog(config):

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(levelname)s: %(message)s", datefmt="%y/%m/%d-%H:%M:%S")
    logger = logging.getLogger("agent")
    if ("DEBUG" in config) and ("LogFile" in config["DEBUG"]):
        fileHandler = TimedRotatingFileHandler(config["DEBUG"]["LogFile"], when="midnight", interval=1, backupCount=5)
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(logging.Formatter("%(asctime)s-%(thread)s-%(levelname)s: %(message)s", datefmt="%y/%m/%d-%H:%M:%S"), )
        logger.addHandler(fileHandler)
    return logger

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
                logger.info("Connecting to %s:%i (%i)...", self.host, self.port, self.timeout)
                self.ssdb = pyssdb.Client(host = self.host, port = self.port, socket_timeout = self.timeout)
                logger.info("Sending credential ...")
                self.ssdb.auth(self.passCode)
            except Exception as ex:
                logger.exception("Connect exception: %s", ex.args[0])
                self.Disconnect()

    def Disconnect(self):
        if self.ssdb != None:
            try:
                self.ssdb.disconnect()
            except Exception as ex:
                logger.exception("Disconnect exception: %s", ex.args[0])
            self.ssdb = None
        else:
            logger.warning("SSDB instence is None")

    def GetAgentCount(self):
        if self.ssdb != None:
            try:
                return self.ssdb.hsize(CONF_AGENT_STATUS)
            except Exception as ex:
                logger.exception("Get agent count exception: %s", ex.args[0])
        else:
            logger.error("SSDB instence is None")

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

                        logger.info("%20s : %s (%s, %s)", agentName.decode("utf-8"), updateTimeStr, statusStr, syncMsg)

            except Exception as ex:
                logger.exception("Check agent status exception: %s", ex.args[0])
        else:
            logger.error("SSDB instence is None")

def AgentCheckRoutine(config):

    confDB = ConfSSDB(config["SSDB"]["Host"], config["SSDB"]["Port"], config["SSDB"]["Timeout"], config["SSDB"]["Passcode"])

    serverList = None
    interval = 0

    if "TASK" in config:
        if "ServerList" in config["TASK"]:
            serverList = config["TASK"]["ServerList"]
        if "Interval" in config["TASK"]:
            interval = config["TASK"]["Interval"]

    confDB.CheckAgentStatus(serverList = serverList)

    logger.info("Disconnecting from SSDB ...")
    confDB.Disconnect()

    # Reschedule the routine at 30 minutes later
    if interval != 0:
        scheduler.enterabs(datetime.now().timestamp() + interval, 0, AgentCheckRoutine, argument=(config,))


if __name__ == '__main__':

    # Get arguments and load configure file
    args = GetArguments(sys.argv)
    content = ReadConfigFile(args[CONFIG_FILE])
    config = json.loads(content)

    # Config debug log
    logger = ConfigDebugLog(config)    

    # Initial scheduler
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enterabs(datetime.now().timestamp(), 0, AgentCheckRoutine, argument=(config,))
    scheduler.run()

