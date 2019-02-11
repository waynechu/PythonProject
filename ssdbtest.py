import json
import os
import logging
import sys
from pyssdb import pyssdb

CONFIG_FILE = "ConfigFile"

def GetArguments(argv):

    parameters = {CONFIG_FILE: ""}
    idx, argc = 0, len(argv)

    while idx < argc:
        if (argv[idx] == "-f") and (idx < argc - 1):
            idx = idx + 1
            parameters[CONFIG_FILE] = argv[idx]
        idx = idx + 1

    if (parameters[CONFIG_FILE] == ""):
        print("Usage:")
        print("    python ssdbtest.py -f <config_file_name>")
        exit(0)
    else:
        return parameters

def LoadConfig(filename):

    fd = open(filename)
    data = fd.read()
    fd.close()

    return data

if __name__ == '__main__':

    parameters = GetArguments(sys.argv)

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(thread)06d-%(levelname)s: %(message)s", datefmt="%Y%m%d-%H%M%S")

    confData = LoadConfig(parameters[CONFIG_FILE])
    agentConf = json.loads(confData)

    confSSDB = pyssdb.Client(host = agentConf["SSDB"]["Host"], port = agentConf["SSDB"]["Port"])

    confSSDB.auth(agentConf["SSDB"]["Passcode"])

    names = confSSDB.hlist("", "", 100)

    for name in names:
        logging.info(name.decode("utf-8"))

    logging.info("------------------------------")

    statusSize = confSSDB.hsize("DNS-Agent-Sync")
    statusHashes = confSSDB.hkeys("DNS-Agent-Sync", "", "", statusSize)

    for agent in statusHashes:
        status = confSSDB.hget("DNS-Agent-Sync", agent)
        if status == b"Sync":
            logging.info("%s is good", agent.decode("utf-8"))
        else:
            logging.info("%s is in trouble!!", agent.decode("utf-8"))

    confSSDB.disconnect()
