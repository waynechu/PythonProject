import sys
import csv
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from common import threadpool
import dns.resolver
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import dns.exception

class DNSQueryTask(threadpool.Task):

    def do(self):

        qname, qtype, qcount, bdnsip = "", "", 0, ""

        for arg in self.kargs:
            if arg == "qtype":
                qtype = self.kargs[arg]
            elif arg == "qname":
                qname = self.kargs[arg]
            elif arg == "qcount":
                qcount = int(self.kargs[arg])
            elif arg == "bdnsip":
                bdnsip = self.kargs[arg]

        if (qname == "") or (qtype == "") or (qcount == 0) or (bdnsip == ""):
            logger.error("Incorrect task!")
            return False

        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [bdnsip]

        for i in range(qcount):
            try:
                time_start = time.perf_counter()
                answer = resolver.query(qname, qtype)
                time_performance = time.perf_counter() - time_start
                for rr in answer:
                    if time_performance > 0:
                        logger.info("%03d %s %s %15s - performace = %3.3f sec", i, qname, qtype, rr, time_performance)
                        time_performance = 0
                    else:
                        logger.info("    %s %s %15s", qname, qtype, rr)

            except dns.exception.DNSException:
                time_performance = time.perf_counter() - time_start
                logger.exception("Exception - performance = %3.3f sec", time_performance)

            except Exception as ex:
                logger.exception("Exception...")
    
        return True

QUERY_FILE = 1
DNS_IP = 2
TEST = 3

ARGUMENT_LIST = [
    [QUERY_FILE, "-f", "<query_list_file>", True],
    [DNS_IP, "-s", "<DNS server IP>", True],
    [TEST, "-t", "<test>", False]
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

if __name__ == '__main__':

    arguments = GetArguments(sys.argv)

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(thread)06d-%(levelname)s: %(message)s", datefmt="%Y%m%d-%H%M%S")

    logger = logging.getLogger("agent")
    fileHandler = TimedRotatingFileHandler("query.log", when='D', interval=1, backupCount=5)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(logging.Formatter("%(asctime)s-%(thread)s-%(levelname)s: %(message)s", datefmt="%y/%m/%d-%H:%M:%S"), )
    logger.addHandler(fileHandler)

    csvfile = open(arguments[QUERY_FILE])
    reader = csv.reader(csvfile)
 
    thdpool = threadpool.ThreadPool(20, 40)
    thdpool.start_pool()

    try:
        for row in reader:
            qtask = DNSQueryTask(qtype = row[0], qname = row[1], qcount = int(row[2]), bdnsip = arguments[DNS_IP])
            thdpool.add_task(qtask)

    except csv.Error as ex:
        print(ex.args)

    thdpool.wait_completion()
    thdpool.stop_pool()

    logger.info("dnsquery complete...")
