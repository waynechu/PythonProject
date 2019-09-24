import json
import os
import logging
import sys

SETTING_FILE = 0

ARGUMENT_LIST = [
    [SETTING_FILE, "-f", "<config_file_name>", True],
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

def LoadSetting(filename):

    fd = open(filename)
    data = fd.read()
    fd.close()

    return data

if __name__ == '__main__':

    args = GetArguments(sys.argv)

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(thread)06d-%(levelname)s: %(message)s", datefmt="%Y%m%d-%H%M%S")

    with open(args[SETTING_FILE], encoding='utf-8') as zoneJson:
        gvtZones = json.load(zoneJson)

    try:

        zones = gvtZones["zones"]
        for zone in zones:
            zoneName = zone["name"]
            dnsInfos = zone["dns_info"]
            Idx = 0
            for dnsInfo in dnsInfos:
                Idx = Idx + 1
                dnsIP = dnsInfo["server"]
                logging.info(dnsInfo)

    except Exception as ex:
        print(ex)

    finally:
        logging.info("Finish -- OK")

