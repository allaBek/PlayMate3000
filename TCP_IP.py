from multiprocessing import process
import  MiddlleMan
import TCP_manager

def start(sharedData, lock, com_param):
    com_manager = TCP_manager.TcpManagerClass(com_param)
    midMan = MiddlleMan.MiddleMan(sharedData, lock)
    while True:
        #print("tcp_ip process is running")
        ###################################### Listening ####################################################################
        command = com_manager.TCP_listener()
        while True:
            result = str(midMan.getCommand(command))
            print(result)
            if result:
                break
        
        ##################################### End listerning ################################################################


        ##################################### Send requested data to master #################################################
        #### But, Just demo (response) to remove ###################
        #array = np.round(np.random.rand(2, 2))
        #arr_str = np.array2string(array)  # Generating some random numpy array and sending it as string as demo
        #print(arr_str)
        ################# Demo end ####################

        ###################################### Emitter ####################################################################
        com_manager.TCP_send(str(result))  # send response
        ####################################### End of emitter ###########################################################