import json
import os
import logging
import sys
from pyssdb import pyssdb

def parameter_check(argv):

    Parameters = {"ConfigFile": ""}
    idx, argc = 0, len(argv)

    while idx < argc:
        if (sys.argv[idx] == "-f") and (idx < argc - 1):
            idx = idx + 1
            Parameters["ConfigFile"] = sys.argv[idx]
        idx = idx + 1

    if (Parameters["ConfigFile"] == ""):
        print("-f <config_file_name>")
        exit(0)
    else:
        return Parameters

if __name__ == '__main__':

    Parameters = parameter_check(sys.argv)

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(thread)06d-%(levelname)s: %(message)s", datefmt="%Y%m%d-%H%M%S")

    ConfFD = open(Parameters["ConfigFile"])
    ConfData = ConfFD.read()
    ConfFD.close()
    print(ConfData)

    AgentConf = json.loads(ConfData)
    SSDBHost = AgentConf["SSDB"]["Host"]
    SSDBPort = AgentConf["SSDB"]["Port"]
    SSDBPasscode = AgentConf["SSDB"]["Passcode"]

    ConfSSDB = pyssdb.Client(host = SSDBHost, port = SSDBPort)

    ConfSSDB.auth(SSDBPasscode)

    #print(ConfSSDB.hgetall("DNS-Agent-Sync"), end = "\n\n")
    #print(ConfSSDB.hkeys("DNS-Agent-Sync", "", "", 100), end = "\n\n")
    #print(ConfSSDB.hgetall("DNS-Agent-Status"), end = "\n\n")
    #print(ConfSSDB.hkeys("DNS-Agent-Status", "", "", 100), end = "\n\n")

    Names = ConfSSDB.hlist("", "", 100)

    for Name in Names:
        print(Name)

    print("------------------------------")

    #LogSize = ConfSSDB.hsize("DNS-Agent-Log-HKSGDNSDF01")
    #hksgdnsdf01 = ConfSSDB.hgetall("DNS-Agent-Log-HKSGDNSDF01", "", "", LogSize)
    #for log in hksgdnsdf01:
    #    print(log)

    print("------------------------------")

    StatusSize = ConfSSDB.hsize("DNS-Agent-Sync")
    StatusHashes = ConfSSDB.hkeys("DNS-Agent-Sync", "", "", StatusSize)

    for Agent in StatusHashes:
        Status = ConfSSDB.hget("DNS-Agent-Sync", Agent)
        if Status == b"Sync":
            print(Agent, "is good!")
        else:
            print(Agent, "in trouble!")

    ConfSSDB.disconnect()