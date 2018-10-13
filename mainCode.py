import multiprocessing as mp
import UART
import numpy as np
import time
import cv2 as cv
import TCP_IP
com = [UART, TCP_IP]
communication = 0
# A queue that will have the data shared between processes
sharedData = mp.Queue()
# A lock to block the access of critical section when either main code is writing or communication process is reading
lock = mp.Lock()
#start the UART process or the TCP/IP
proc = mp.Process(target=com[1].start, name='Communication', args=(sharedData, lock))
if __name__ == '__main__':
    proc.start()
    image = cv.imread(r"F:\sw\0.jpg")
    board = np.zeros((8, 8))
    pieces = np.zeros((8, 8, 3))
    piece = [1, 2, 3]
    arm = [7, 1, 10]
    i = 0
    while True:
        lock.acquire()
        while sharedData.empty() is False:
            sharedData.get()
        sharedData.put(["image" + str(i), image])
        sharedData.put(["pieces" + str(i), pieces])
        sharedData.put(["board" + str(i), board])
        sharedData.put(["piece" + str(i), piece])
        sharedData.put(["arm" + str(i), arm])
        lock.release()
        i += 1
        time.sleep(0.1)