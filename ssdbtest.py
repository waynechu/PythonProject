import json
import os
import logging
import sys
from pyssdb import pyssdb

def parameter_check(argv):

    parameters = {"ConfigFile": ""}
    idx, argc = 0, len(argv)

    while idx < argc:
        if (sys.argv[idx] == "-f") and (idx < argc - 1):
            idx = idx + 1
            parameters["ConfigFile"] = sys.argv[idx]
        idx = idx + 1

    if (parameters["ConfigFile"] == ""):
        print("python ssdbtest.py -f <config_file_name>")
        exit(0)
    else:
        return parameters

def load_config(filename):

    fd = open(filename)
    data = fd.read()
    fd.close()

    return data

if __name__ == '__main__':

    parameters = parameter_check(sys.argv)

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(thread)06d-%(levelname)s: %(message)s", datefmt="%Y%m%d-%H%M%S")

    confData = load_config(parameters["ConfigFile"])
    agentConf = json.loads(confData)
    ssdbHost = agentConf["SSDB"]["Host"]
    ssdbPort = agentConf["SSDB"]["Port"]
    ssdbPasscode = agentConf["SSDB"]["Passcode"]

    confSSDB = pyssdb.Client(host = ssdbHost, port = ssdbPort)

    confSSDB.auth(ssdbPasscode)

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