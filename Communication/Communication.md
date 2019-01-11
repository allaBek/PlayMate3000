## Description
Communication part consists of three parts, a UART communication class, TCP/IP communication
and a broker between the main code and the communication modules named MiddleMan. 
### MiddleMan.py:
This class contains methods to retrieve data from the main code, in other words it is used by 
the UART or TCP/IP classes to communicate with the main processes, such as getting the frame or
the position of the arm.
### UART:
This is one way to communicate between the computer vision host device and other devices.
The simple format is to enclose the sent command with stars, for example * image *, then it will be 
received by the UART process. The latter uses MiddleMan class to retrieve data from the main process 
and send it again to the requesting device.

### TCP/IP:

 
