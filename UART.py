import serial
from time import sleep
import MiddlleMan

def start(sharedData, lock, testingCommand = ''):
    print("started UART process")
    mm = MiddlleMan.MiddleMan(sharedData, lock)
    if testingCommand == '':
        ser = serial.Serial("/dev/ttyUSB0",
                            115200)  # Open port Serial (not mini serial) with baud rate set to max, I chose this just to test, we can reduce it later
        while True:
            ReceivedCommand = ser.readline()  # read Serial port
            DecodedCommand = ReceivedCommand.decode('utf-8') #decode the command into utf-8 format
            commandStarted = False
            command = ''
            for i in DecodedCommand:
                if commandStarted and i != '*':
                    command = command + i
                elif commandStarted and i == '*':
                    break
                if i == '*':
                    commandStarted = True
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
    else:
        for c in mm.checkList:
            if c == testingCommand:
                verify = True
                break
        if not verify:
            return 'wrong command'
        while verify:
            res = mm.getCommand(testingCommand)  # use MiddleMan to get the data from the main process of CV
            if res is not None:
                return res






