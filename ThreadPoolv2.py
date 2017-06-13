from queue import Queue
from threading import Thread, Event

class Task:
    """Task to obtain function for thread pool to run"""
    def __init__(self, **kargs):
        self.kargs = kargs
        self.event = Event()

    def do(self):
        pass

    def task_complete(self):
        self.event.set()

    def wait_for_task_done(self, timout = None):
        return self.event.wait(timout)

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.doing = True
    
    def run(self):
        while self.doing:
            try:
                task = self.tasks.get(True, 3)

                try:
                    task.do()
                    task.task_complete()
                except Exception as taskex:
                    print("__exception: ", str(taskex), taskex.args)

                self.tasks.task_done()
            except: # no item to get
                pass

    def stop(self):
        self.doing = False

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads, max_queue_size):
        self.tasks = Queue(max_queue_size)
        self.threads = []
        for i in range(num_threads):
            self.threads.append(Worker(self.tasks))

    def start_pool(self):
        for idx in range(len(self.threads)):
            self.threads[idx].start()

    def stop_pool(self):
        for idx in range(len(self.threads)):
            self.threads[idx].stop()
        for idx in range(len(self.threads)):
            self.threads[idx].join()
            print(self.threads[idx].name, "stopped")

    def add_task(self, task):
        self.tasks.put(task)

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()

class SleepTask(Task):

    def do(self):
        delay = 0
        for arg in self.kargs:
            if arg == "delay":
                delay = self.kargs[arg]
        if delay > 0:
            print("Sleep for", delay, "second(s)")
            sleep(delay)
        return True

if __name__ == '__main__':
 
    from random import randrange
    delays = [randrange(1, 4) for i in range(100)]
    
    from time import sleep

    # 1) Init a Thread pool with the desired number of threads
    pool = ThreadPool(20, 50)
    pool.start_pool()
    
    for i, d in enumerate(delays):
        # print the percentage of tasks placed in the queue
        print("Adding a new task: wait_delay(delay=", d, ")")
        
        # 2) Add the task to the queue
        task = SleepTask(delay = d)
        pool.add_task(task)
        task.wait_for_task_done(0.001)
    
    # 3) Wait for completion
    print("Waiting for all tasks to complete...")
    pool.wait_completion()

    print("Task complete, stop thread pool")
    pool.stop_pool()
    print("Thread pool stopped successfully")
