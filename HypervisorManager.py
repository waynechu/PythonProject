

class HypervisorManager:

    def __init__(self):
        self.hypervisors = []
        # get database data and load corresponding hypervisor controllers

    def AddVM(self):
        pass

    def RemoveVM(self):
        pass

    def CovertVMToTemplate(self):
        pass

if __name__ == "__main__":
    print("Hello!!")
    hm = HypervisorManager()
    hm.hypervisors.append("abc")
    hm.hypervisors.append("cde")
    print(hm.hypervisors)



