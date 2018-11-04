import serial
from time import sleep
import MiddlleMan

def start(sharedData, lock):
    print("started UART process")
    ser = serial.Serial("COM4",
                        115200)  # Open port Serial (not mini serial) with baud rate set to max, I chose this just to test, we can reduce it later
    mm = MiddlleMan.MiddleMan(sharedData, lock)
    while True:
        ReceivedCommand = ser.readline()  # read Serial port till a star is recieved indicating end of command
        DecodedCommand = ReceivedCommand.decode('utf-8')
        commandStarted = False
        command = ''
        for i in DecodedCommand:
            if commandStarted and i != '*':
                command = command + i
            elif commandStarted and i == '*':
                break
            if i == '*':
                commandStarted = True
        print(command)
        verify =False
        for c  in mm.checkList:
            if c == command:
                verify = True
                break
        if not verify:
            ser.write(b"wrong command")
            print("wrong command")
        #sleep(0.03)  # stop the process for 30ms
        while verify:
            res = mm.getCommand(command) #use MiddleMan to get the data from the main process of CV
            if res is not None:
                ser.write(res)
                print("result is:" + str(res))
                break






