# Playmate 3000 vision system

Playmate 3000 is a chess player. This repo represents only the vision section of the entire project.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
The project was tested on a Raspberry Pi 3 model B.

### Prerequisites
If you need desire to run the project on another pi or on you local machine, you would need to make sure that you have:
- Python >= 2.6.x and python >= 3.5.x
- Libraries: numpy >= 1.8.x, netifaces 0.10.x,
- OpenCV 4.0.x compiled with OPENCV_ENABLE_NONFREE=ON flag in order to have access to SIFT/SURF and other patented algorithms.
```
https://www.pyimagesearch.com/2018/08/15/how-to-install-opencv-4-on-ubuntu/
```
- picamera module if you want to run it on a raspberry pi with pi's camera module.
- scipy >= 1.1.0
- matplotlib >= 1.4.2


## Running the tests

1) Start by running Cut_images_pi.py by issuing the following command:

```
python3 Cut_images_pi.py
```

You will need to select pieces on the board that the main code will try to detect later on.
Once you run this program, the instructions on how to proceed will be printed on terminal window. Please follow these instructions.
--- Screen shot 1 will be added soon



2) Next, you will need to select reliable threshold values. We will use these values to detect the pieces later on. To do this, run Acquire_threshold.py:

```
python3 Acquire_threshold.py
```
  -Two windows will pop up. The first one has trackbars & the second shows the pieces you cropped using Cut_images_pi.py
	- Change the trackbars' position in order to get only the piece displayed WHITE & all the non-relevant parts would be black
	- Press 'q' once you select good threshold value to move to the next image
  - At the end of the program, a text file will be generated. It is named: threshold.txt. It will contain the threshold
  values to be used by the main code to detect the pieces.

3) At this point, everything is ready to run the main program. Run the main program by issuing the following command (note the use of python 2)

	```
	python2 mainCode_pi.py
	```

	- Follow the instructions printed on terminal.
		- master's ip: 127.0.0.1 (if you desire to use the localhost server)
		- master to slave port: 5005
		- slave to master port: 4005
		- buffer size: 1024
      
      
    - On another terminal:
    	  - run master_receiver.py by issuing the following command:
        ```
        python2 master_receiver.py
        ```

		This will keep listening. Whenever a message from the main program is sent, it will be displayed here !

		- On another terminal:
			- run master_emitter.py by issuing the following command:
			
        ```
        python2 master_emitter.py
        ```
		This will send a request to the main code to get arm position, board frame, pieces' position ..

## General notes:

- If you desire to use TCP/IP over a local or public network, you might need to consider the following:
	- Once you get the main code running, you need to run the provided (or modified) versions of master_emitter & master_receiver. Use a text editor to change the IP addresses hardcoded into these files.
	- You can change the ports too.
	- You might need to allow receiving the data from these ports on the master computer. Please make sure your firewall would not block the inbound packets on these ports (In this case 5005 & 4005 ports). Of Ubuntu, you can use the following command:
``` 
sudo iptables -A INPUT -i <interface> -j ACCEPT -p <port>
``` 
ex:
``` 
sudo iptables -A INPUT -i wlan0 -j ACCEPT -p 5005
```

## Screenshots will be added soon :) !

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

