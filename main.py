import threadpool

class SleepTask(threadpool.Task):

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
    delays = [randrange(1, 4) for i in range(20)]
    
    from time import sleep

    # 1) Init a Thread pool with the desired number of threads
    pool = threadpool.ThreadPool(20, 50)
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
