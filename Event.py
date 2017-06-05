import threading
import time
import logging

logging.basicConfig(level=print,
                    format='(%(threadName)-9s) %(message)s',)
                    
def wait_for_event(e):
    print('wait_for_event starting')
    event_is_set = e.wait()
    print('event set: ', event_is_set)

def wait_for_event_timeout(e, t):
    while not e.isSet():
        print('wait_for_event_timeout starting')
        event_is_set = e.wait(t)
        print('event set: ', event_is_set)
        if event_is_set:
            print('processing event')
        else:
            print('doing other things')

if __name__ == '__main__':
    e = threading.Event()
    t1 = threading.Thread(name='blocking', 
                      target=wait_for_event,
                      args=(e,))
    t1.start()

    t2 = threading.Thread(name='non-blocking', 
                      target=wait_for_event_timeout, 
                      args=(e, 2))
    t2.start()

    print('Waiting before calling Event.set()')
    time.sleep(3)
    e.set()
    print('Event is set')
