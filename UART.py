# TX/Rx : GPIO14/GPIO15
import serial
from time import sleep
import MiddlleMan

def start(sharedData, lock):
    ser = serial.Serial("/dev/ttyAMA0 ",
                        115200)  # Open port Serial (not mini serial) with baud rate set to max, I chose this just to test, we can reduce it later
    mm = MiddlleMan.MiddleMan(sharedData, lock)
    while True:
        command = ser.read_until('*')  # read Serial port till a star is recieved indicating end of command
        sleep(0.03)  # stop the process for 30ms
        while True:
            res = mm.getCommand(command) #use MiddleMan to get the data from the main process of CV
            if res is not None:
                ser.write(res + "*")
                break






