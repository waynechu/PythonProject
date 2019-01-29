# Command Queue is a queue to store command

from collections import deque

class Command:
    """ Command class that represents a command """
    def __init__(self, id):
        self.id = id


class CommandQueue:

    def __init__(self, MaxSize):
        self.CmdQueue = deque([])
        self.MaxSize = MaxSize

    def add(self, cmd):
        if (len(self.CmdQueue) < self.MaxSize):
            self.CmdQueue.append(cmd)
            return True
        else:
            return False

    def get(self):
        if (len(self.CmdQueue) > 0):
            cmd = self.CmdQueue.popleft()
            return cmd
        else:
            return None

    def count(self):
        return len(self.CmdQueue)

cq = CommandQueue(5)
cq.add(Command(0x00000001))
cq.add(Command(0x00000010))
cq.add(Command(0x00000020))
cq.add(Command(0x00000001))
cq.add(Command(0x00000010))
cq.add(Command(0x00000020))

cnt = cq.count()
print(cnt)
for idx in range(cnt):
    cmd = cq.get()
    if cmd is not None:
        print("Get queue success. Cmd = ", cmd.id)
    else:
        print("Unable to get command from queue")