from random import randrange
from time import sleep

import csv
import time
import threadpool
import dns.resolver
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query

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
        resolver.nameservers = ['27.126.245.88']
        #resolver.nameservers = ['1.1.1.1']
        #resolver.nameservers = ['8.8.8.8']

        for i in range(qcount):
            try:
                t1_start = time.perf_counter()
                answer = resolver.query(qname, qtype)
                t1_stop = time.perf_counter()
                print("performance = {0:.6f} sec".format(t1_stop - t1_start))
                for rr in answer:
                    print(i, qname, qtype, rr)
            except Exception as ex:
                t1_stop = time.perf_counter()
                t2_stop = time.process_time()
                print(ex, "performance = {0:.6f} sec".format(t1_stop - t1_start))
    
        return True

if __name__ == '__main__':
 
    csvfile = open('pythonproject\querylist.csv')
    reader = csv.reader(csvfile)

    thdpool = threadpool.ThreadPool(3, 10)
    thdpool.start_pool()

    try:
        for row in reader:
            task = DNSQueryTask(qtype = row[0], qname = row[1], qcount = 100)
            thdpool.add_task(task)
            #thdpool.add_task(task)
            #thdpool.add_task(task)
    except csv.Error as ex:
        print(ex.args)

    thdpool.wait_completion()
    thdpool.stop_pool()
