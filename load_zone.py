import dns.zone
import sys
import os
import logging

ZONE_FILENAME = 1
ZONE_EXTENSION = ".zone"

ARGUMENT_LIST = [
    [ZONE_FILENAME, "-z", "<zone_file_name>", True]
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


if __name__ == "__main__":

    args = GetArguments(sys.argv)

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(thread)06d-%(levelname)s: %(message)s", datefmt="%Y%m%d-%H%M%S")

    zoneFilename = args[ZONE_FILENAME]
    originName = os.path.basename(zoneFilename)
    if len(originName) - len(ZONE_EXTENSION) == originName.rfind(ZONE_EXTENSION):
        originName = originName.rpartition(ZONE_EXTENSION)[0]

    zone = dns.zone.from_file(zoneFilename, origin = originName)

    for (name, ttl, rdata) in zone.iterate_rdatas():
        logging.info("%10s %8d %3d %s", name.to_text(), ttl, rdata.extended_rdatatype(), rdata.to_text())

