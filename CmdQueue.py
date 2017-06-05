# Cmd Queue is a queue to store Cmd

from queue import Queue

class Cmd:
    """ Cmd class that represents a Cmd """
    def __init__(self, id):
        self.id = id

try:
    CmdQueue = Queue(5)
    CmdQueue.put(Cmd(0x00000010), block = False)
    CmdQueue.put(Cmd(0x00000020), block = False)
    CmdQueue.put(Cmd(0x00000001), block = False)
    CmdQueue.put(Cmd(0x00000010), block = False)
    CmdQueue.put(Cmd(0x00000020), block = False)
    CmdQueue.put(Cmd(0x00000010), block = False)
    CmdQueue.put(Cmd(0x00000020), block = False)
    CmdQueue.put(Cmd(0x00000001), block = False)
    CmdQueue.put(Cmd(0x00000010), block = False)
    CmdQueue.put(Cmd(0x00000020), block = False)
except:
    print("Excpetion!!")
else:
    print("No problem!")
    
cnt = CmdQueue.qsize()
print(cnt)
for idx in range(cnt):
    cmd = CmdQueue.get()
    if cmd is not None:
        print("Get queue success. Cmd = ", cmd.id)
    else:
        print("Unable to get Cmd from queue")