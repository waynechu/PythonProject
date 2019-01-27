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
            if arg == "qname":
                qname = self.kargs[arg]
            if arg == "qcount":
                qcount = int(self.kargs[arg])

        resolver = dns.resolver.Resolver(configure=False)
        #resolver.nameservers = ['27.126.245.88']
        #resolver.nameservers = ['1.1.1.1']
        resolver.nameservers = ['8.8.8.8']

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

if __name__ == '__main__':

    print(sys.argv)

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(threadName)10s-%(levelname)s: %(message)s", datefmt="%Y%m%d-%H%M%S")

    logging.info("dnsquery started...")

    csvfile = open("pythonproject\\querylist.csv")
    reader = csv.reader(csvfile)
 
    thdpool = threadpool.ThreadPool(10, 10)
    thdpool.start_pool()

    try:
        for row in reader:
            qtask = DNSQueryTask(qtype = row[0], qname = row[1], qcount = 5)
            thdpool.add_task(qtask)

    except csv.Error as ex:
        print(ex.args)

    thdpool.wait_completion()
    thdpool.stop_pool()

    logging.info("dnsquery complete...")
