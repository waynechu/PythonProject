import threading

class Counter(object):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start
    def increment(self):
        print(threading.current_thread(), 'Waiting for lock')
        self.lock.acquire()
        try:
            print(threading.current_thread(), 'Acquired lock')
            self.value = self.value + 1
        finally:
            print(threading.current_thread(), 'Release')
            self.lock.release()

def worker(c):
    for i in range(200):
        c.increment()
    print('Done')

counter = Counter()
thd = []

for i in range(4):
    t = threading.Thread(target=worker, args=(counter,))
    thd.append(t)

for t in thd:
    t.start()

print('Waiting for worker threads')

for t in thd:
    t.join()

print('Counter: ', counter.value)

