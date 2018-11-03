class MiddleMan:
    data = []
    lock = None
    sharedData = None
    
    def __init__(self, sharedData, lock):
        self.sharedData = sharedData
        self.lock = lock

    def getCommand(self, command):
        if self.sharedData.empty() == True:
            for i in self.data:
                if i[0] == command:
                    return i[1]
        else:
            self.lock.acquire()
            data = []
            while self.sharedData.empty() is False:
                data.append(self.sharedData.get())
            self.lock.release()
            if len(data) > 0:
                self.data = data
            for i in self.data:
                if i[0] == command:
                    return i[1]
