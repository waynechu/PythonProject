from random import randrange
from time import sleep

import csv
import threadpool
import dns.resolver
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query

class DNSQueryTask(threadpool.Task):

    def do(self):

        for arg in self.kargs:
            if arg == "qtype":
                qtype = self.kargs[arg]
            if arg == "qname":
                qname = self.kargs[arg]

        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ['8.8.8.8']

        for i in range(10):
            try:
                answer = resolver.query(qname, qtype)
                for rr in answer:
                    print(qname, qtype, rr)
            except Exception as ex:
                print(ex)
    
        return True

if __name__ == '__main__':
 
    csvfile = open('pythonproject\querylist.csv')
    reader = csv.reader(csvfile)

    thdpool = threadpool.ThreadPool(10, 20)
    thdpool.start_pool()

    try:
        for row in reader:
            task = DNSQueryTask(qtype=row[0], qname=row[1])
            thdpool.add_task(task)
    except csv.Error as ex:
        print(ex.args)

    print("Waiting for all tasks to complete...")
    thdpool.wait_completion()

    print("Task complete, stop thread pool")
    thdpool.stop_pool()
    print("Thread pool stopped successfully")
