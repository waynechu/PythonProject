import sys
import csv
import time
import logging

import threadpool

import dns.resolver
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import dns.exception

class DNSQueryTask(threadpool.Task):

    def do(self):

        qcount = 100

        for arg in self.kargs:
            if arg == "qtype":
                qtype = self.kargs[arg]
            elif arg == "qname":
                qname = self.kargs[arg]
            elif arg == "qcount":
                qcount = int(self.kargs[arg])
            elif arg == "bdnsip":
                bdnsip = self.kargs[arg]

        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [bdnsip]

        for i in range(qcount):
            try:
                time_start = time.perf_counter()
                answer = resolver.query(qname, qtype)
                time_stop = time.perf_counter()
                for rr in answer:
                    logging.info("%02d %s %s %15s - performace = %3.3f sec", i, qname, qtype, rr, time_stop - time_start)

            except dns.exception.DNSException as dnsex:
                time_stop = time.perf_counter()
                logging.warning("%s - performance = %3.3f sec", dnsex.msg, time_stop - time_start)

            except Exception as ex:
                print(ex)
    
        return True

def printusage():
    print("python dnsquery.py -f <query_list.csv> -s <backend_dns_ip>")

if __name__ == '__main__':

    idx = 1
    argc = len(sys.argv)
    qlistfile = ""
    bdnsip = ""

    while idx < argc:
        if (sys.argv[idx] == "-f") and (idx < argc - 1):
            idx = idx + 1
            qlistfile = sys.argv[idx]
        elif (sys.argv[idx] == "-s") and (idx < argc - 1):
            idx = idx + 1
            bdnsip = sys.argv[idx]
        idx = idx + 1

    if (qlistfile == "") or (bdnsip == ""):
        printusage()
    else:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(threadName)10s-%(levelname)s: %(message)s", datefmt="%Y%m%d-%H%M%S")

        logging.info("dnsquery started...")

        csvfile = open(qlistfile)
        reader = csv.reader(csvfile)
 
        thdpool = threadpool.ThreadPool(10, 10)
        thdpool.start_pool()

        try:
            for row in reader:
                qtask = DNSQueryTask(qtype = row[0], qname = row[1], qcount = 5, bdnsip = bdnsip)
                thdpool.add_task(qtask)

        except csv.Error as ex:
            print(ex.args)

        thdpool.wait_completion()
        thdpool.stop_pool()

        logging.info("dnsquery complete...")
