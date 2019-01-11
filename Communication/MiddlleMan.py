class MiddleMan:
    data = []
    lock = None
    sharedData = None
    checkList = ["pieces","board","arm", "image"]
    logger = None

    def __init__(self, sharedData, lock, logger):
        self.sharedData = sharedData
        self.lock = lock
        self.logger = logger

    def getCommand(self, command):
        self.logger.info('Get command reached')

        if self.sharedData.empty() == True:
            for i in self.data:
                if i[0] == command:
                    return i[1]
        else:
            self.lock.acquire()
            data = []
            self.logger.info('Lock state : '+ self.sharedData.empty())
            while self.sharedData.empty() is False:
                data.append(self.sharedData.get())
            self.lock.release()
            if len(data) > 0:
                self.data = data
            for i in self.data:
                if i[0] == command:
                    return i[1]
