# It should be changed to the actual image processing
# results from the raspberry
import sys
import socket


class TcpManagerClass(object):
    __master_ip = None
    __self_ip = None
    __master2slave = None
    __slave2master = None
    __buffer_size = 1024
    __data = None

    ############################### Constructor to set communication parameters #############################
    def __init__(self, com_param):
        self.__master_ip = com_param[0]  # IP address of Master device
        self.__self_ip = com_param[1]
        self.__master2slave = com_param[2]   # Com port
        self.__slave2master = com_param[3]  # Com port
        self.__buffer_size = com_param[4]   # Buffer size

    ####################################### End constructor ###################################################

    ###################################### TCP IP communication handler ######################################

    ###################################### Slave is waiting for demands through this listener function TCP ######################
    def TCP_listener(self):

        print("Waiting for data ...")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening socket
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("IP local : "+self.__self_ip)
	s.bind((self.__self_ip, self.__master2slave))  # Setting IP and port settings of the socket
        s.listen(1)  # Start listening

        conn, addr = s.accept()
        print('Connection address:', addr)
        while 1:
            data = conn.recv(self.__buffer_size)
            self.__data = data
            print("received data:", self.__data)
            if data != None: break
            #print("received data:", data)
            conn.send(data)  # echo
        conn.close()
        return self.__data

    ################################# End Of demand receiver TCP #################################################################

    ################################  TCP Emitter ####################################################################################
    def TCP_send(self, MESSAGE):
        print("Message : " + MESSAGE)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((self.__master_ip, self.__slave2master))

        s.send(MESSAGE)
        data = s.recv(self.__buffer_size)

        print("received sent :", data)
        s.close()
    ############################## End of TCP emitter ###################################################################################
