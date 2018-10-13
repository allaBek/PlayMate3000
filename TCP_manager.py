# It should be changed to the actual image processing
# results from the raspberry
import sys
import socket


class TcpManagerClass(object):
    __master_ip = None
    __master2slave = None
    __slave2master = None
    __buffer_size = 1024

    ############################### Constructor to set communication parameters #############################
    def __init__(self):
        print("Welcome to the PLAYMATE 3000 computer vision interface")
        print("You have chosen TCP/IP protocol as the main communication interface !")
        print("Please enter Master's IP address:")
        self.__master_ip = "127.0.0.1"#sys.stdin.readline().rstrip("\n")  # IP address of Master device
        self.__master2slave = 5005 #int(input("Please enter Master-to-Slave port: \n"))  # Com port
        self.__slave2master = 6005 #int(input("Please enter Slave-to-Master port: \n")) # Com port
        self.__buffer_size = 1024 #int(input("Please specify buffer size (Default = 1024)\n"))  # Buffer size

    ####################################### End constructor ###################################################

    ###################################### TCP IP communication handler ######################################

    ###################################### Slave is waiting for demands through this listener function TCP ######################
    def TCP_listener(self):
        print("Waiting for data ...")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening socket
        s.bind((self.__master_ip, self.__master2slave))  # Setting IP and port settings of the socket
        s.listen(1)  # Start listening

        conn, addr = s.accept()
        print('Connection address:', addr)
        while 1:
            data = conn.recv(self.__buffer_size)
            if not data: break
            print("received data:", data)
            conn.send(data)  # echo
        conn.close()
        return data

    ################################# End Of demand receiver TCP #################################################################

    ################################  TCP Emitter ####################################################################################
    def TCP_send(self, MESSAGE):
        MESSAGE = "haha"
        print(MESSAGE)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.__master_ip, self.__slave2master))

        s.send(MESSAGE)
        data = s.recv(self.__buffer_size)

        print("received sent :", data)
        s.close()
    ############################## End of TCP emitter ###################################################################################
