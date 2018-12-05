# It should be changed to the actual image processing
# results from the raspberry
import sys
import socket


class TcpManagerClass(object):
    __master_ip = None
    __master2slave = None
    __slave2master = None
    __buffer_size = 1024
    logger = None

    ############################### Constructor to set communication parameters #############################
    def __init__(self, com_param, logger):
        #logger.info("Welcome to the PLAYMATE 3000 computer vision interface")
        #logger.info("You have chosen TCP/IP protocol as the main communication interface !")
        #logger.info("Please enter Master's IP address:")
        self.__master_ip = "127.0.0.1"#sys.stdin.readline().rstrip("\n")  # IP address of Master device
        self.__master2slave = com_param[2] #int(input("Please enter Master-to-Slave port: \n"))  # Com port
        self.__slave2master = com_param[3] #int(input("Please enter Slave-to-Master port: \n")) # Com port
        self.__buffer_size  = com_param[4] #int(input("Please specify buffer size (Default = 1024)\n"))  # Buffer size
        self.logger = logger
    ####################################### End constructor ###################################################

    ###################################### TCP IP communication handler ######################################

    ###################################### Slave is waiting for demands through this listener function TCP ######################
    def TCP_listener(self):
        self.logger.info("Waiting for data ...")
        #logger.info(self.__master_ip, self.__master2slave, self.__slave2master, self.__buffer_size)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening socket
        s.bind((self.__master_ip, self.__master2slave))  # Setting IP and port settings of the socket
        s.listen(1)  # Start listening

        conn, addr = s.accept()
        self.logger.info('Connection address:', addr)
        while 1:
            data = conn.recv(self.__buffer_size)
            if not data: break
            self.logger.info("received data:", data)
            conn.send(data)  # echo
        conn.close()
        return data

    ################################# End Of demand receiver TCP #################################################################

    ################################  TCP Emitter ####################################################################################
    def TCP_send(self, MESSAGE):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.__master_ip, self.__slave2master))

        s.send(MESSAGE)
        data = s.recv(self.__buffer_size)

        self.logger.info("received sent :", data)
        s.close()
    ############################## End of TCP emitter ###################################################################################
