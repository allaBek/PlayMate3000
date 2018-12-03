import multiprocessing as mp
import numpy as np
import time, sys, netifaces
import cv2
import os
import logging
## Pi modules
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

########### Own Classes ################
import TCP_IP, UART     # Com services resides here
from BoardDetectorClass import BoardDetector
from ArmDetectorClass import ArmDetector


def getCommunicationType():
    print("Welcome to the PLAYMATE 3000 computer vision interface")
    print("Please select one of the following communication protocols")
    print("1)TCP/IP\t\t2)UART")
    choice = sys.stdin.readline().rstrip("\n")
    return choice
def com_init():
    count = 1
    print("You have chosen TCP/IP protocol as the main communication interface !")
    print("Please select the interface you're going to use :")
    for x in netifaces.interfaces():
        print(str(count) + " : " + x)
        count += 1
    tmp = netifaces.interfaces()[input() - 1]
    self_ip = netifaces.ifaddresses(tmp)[netifaces.AF_INET][0]['addr']
    print(self_ip)
    print("Please enter Master's IP address:")
    master_ip = sys.stdin.readline().rstrip("\n")  # IP address of Master device
    master2slave = int(input("Please enter Master-to-Slave port: \n"))  # Com port
    slave2master = int(input("Please enter Slave-to-Master port: \n"))  # Com port
    buffer_size = int(input("Please specify buffer size (Default = 1024)\n"))  # Buffer size
    com_param = [master_ip, self_ip, master2slave, slave2master, buffer_size]
    return com_param

if __name__ == '__main__':
    
    choice = '0'
    com = [UART, TCP_IP]
    communication = 0

    ### logging
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename='logs.log', level=logging.DEBUG, format=LOG_FORMAT, filemode='w')
    logger = logging.getLogger()
    ###
    ####### Board detection variables
    board = np.random.random((8, 8))
    pieces = np.random.random((8, 8, 3))
    piece = [1, 2, 3]
    arm_position = np.random.random((1,2))
    ###### Board detection variables end ####################

    # A queue that will have the data shared between processes
    sharedData = mp.Queue()
    # A lock to block the access of critical section when either main code is writing or communication process is reading
    lock = mp.Lock()

    # Let's start the chosen communication method
    while choice != '1' and choice !='2':
        choice = getCommunicationType()
    if choice == '1':
        # Initialization of communication parameters
        com_param = com_init()
        logger.info('Process started !')
        proc = mp.Process(target=com[1].start, name='Communication', args=(sharedData, lock, com_param))
    elif choice == '2':
        print("You have chosen I2C protocol as the main communication interface!")
        proc = mp.Process(target=com[0].start, name='Communication', args=(sharedData, lock))
    proc.start()
    
#################################################### Board detection ############################################
    
    ## Pi specific
    # Initialize the camera
    camera = PiCamera()
    camera.resolution = (640,480)
    camera.framerate = 30
    camera.sensor_mode = 1      # 5 might be also interesting. # It controls the field of view FoV
    rawCapture = PiRGBArray(camera, size=(640,480))

    # Allow camera to warmup
    time.sleep(0.1)
    
    #this will have the number of squares on the image
    for image in camera.capture_continuous(rawCapture, format = "bgr", use_video_port=True):
        #read frame from camera
        frame = image.array
        #try catch block to avoid errors
        if bframe:  # bframe stands for boolean frame => frame status
            # Ceation of board detection object. The only used function is board_detector
            # It takes the frame as input and returns a boolean flag => if true => board detected and returns the cropped board. If False, board to detected and [] as empty board
            boardDetectorObj = BoardDetector()

            # Creating an Arm detection object. Only one function is valuable (arm_detector).
            # returns the position of the center of the 'arm' and a frame on which a square and center of the arm are drawn
            armDetectorObj = ArmDetector()
            

            # Initially, let's pass the frame to  see if the board is present or not
            status, board = boardDetectorObj.board_detector(frame=frame)

            #print(status)

            if not status: # If the board is not detected, let's check if the arm is interrupting the view ! -
                # Let's see the frame
                cv2.imshow('frame', frame)
                
                arm_position, arm_frame = armDetectorObj.arm_detector(frame=frame)
                
                #if arm_position:    # Yes. The arm is interrupting the view. Let's start the arm feedback mode
                    #print(arm_position)

                #else:               # Nop. Arm is not present in the board view. The board in not found !
                    #print('The board is not found')

            else:
                cv2.imshow('board', board)
                cv2.imshow('frame', frame)


            pieces = np.zeros((8, 8, 3))
            piece = [1, 2, 3]
            
            i=0

        
            lock.acquire()
            while sharedData.empty() is False:
                sharedData.get()
            sharedData.put(["image" , frame])
            sharedData.put(["pieces", pieces])
            sharedData.put(["board", board])
            sharedData.put(["piece", piece])
            sharedData.put(["arm", arm_position])
            lock.release()
            i+=1

            key = cv2.waitKey(1) & 0xFF
            
            rawCapture.truncate(0)

            if key == ord('q'):
                cv2.destroyAllWindows()
                break

################################################ Board detection ###########################################