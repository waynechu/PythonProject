import time
from datetime import datetime
import sched


def perform_task():
    scheduler.enter(10, 0, perform_task)
    print('hello world')


if __name__ == '__main__':
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enterabs(datetime.now().timestamp() + 10, 0, perform_task)  # datetime.timestamp()是python3.3后才有
    print('crontab run')
    scheduler.run()
