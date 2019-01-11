import multiprocessing as mp
import numpy as np
########### Own Classes ################
from Communication import UART


def test_UART():
    # A queue that will have the data shared between processes
    sharedData = mp.Queue()
    testData  = mp.Queue()
    #create a lock between the two processes
    lock = mp.Lock()
    #pass arguments for the process
    proc = mp.Process(target=UART.start, name='Communication', args=(sharedData, lock, testData))
    #start the process
    proc.start()
    # testing data
    board = np.random.random((8, 8))
    pieces = np.random.random((8, 8, 3))
    piece = [1, 2, 3]
    arm_position = np.random.random((1, 2))
    #acquire the lock to write data into the critical section
    lock.acquire()
    #check if the common stack is empty
    while sharedData.empty() is False:
        sharedData.get()
    sharedData.get()
    sharedData.put(["pieces", pieces])
    sharedData.put(["board", board])
    sharedData.put(["piece", piece])
    sharedData.put(["arm", arm_position])
    lock.release()


    # capture.release()
