## Description
Piece detection consists of 3 modules, the first is **cut_images.py** which obtains pieces 
images from the board by manually cropping the frame, the second is **Acquire_threshold.py** 
which processes the cut images and save threshold values to be used in the HSV filter, and
 lastly **Classification.py** which is the module were HSV filter is applied on a list 
 of images obtained from the board, it then classifies them into player1, player2 and 
 empty square.
In this documentation the three modules are presented in more details and how to 
integrate them into the project.

### cut_images:
This module consists of two functions, which are used to take samples of the pieces in the game. It displays the camera frame and that will be used to manually crop small squares of the pieces. The algorithm requires 8 images, divided as a tree into player1, player2; background1, background2; flash, no flash; these are used to obtain threshold values later in HSV. The images are cropped by first pressing the button s, then selecting two points in the frame which will be the two opposite edges of a rectangle. If the selection was good, press q to save it into a folder in the same directory, otherwise press r to repeat the selection. After 8 iterations the loop will end and the program will terminate. 

### Acquire_threshold:
This module consists of call back functions and a main script. This module is used to obtain the correct HSV filter parameters to distinguish between pieces of the game. The module uses mages obtained from cut_images, hence 8 images will be processed. The user would change the values of the Hue, Saturation and Value to obtain an image where only the piece is in black and background is white. Once the process is over, the values of the threshold are saved to a txt file for both player 1 and player 2. The values are then used to classify images in the future, however if pieces colors are to be changed, the processed need to be repeated to have accurate results.

### Classification:
The module consists of 6 functions. Pieces_to_matrix function is the main part of the code, which takes as input a linear list of images (1 * 64) of the pieces and outputs an 8 * 8 matrix containing either 1,-1, 0 as player1, player2, empty. The function starts by converting the linear list to an 8*8 matrix. Then it applies the filter to each image one by one and fill in the value of the pieces. The used method for classification is the percentage of the white area in the resulting filtered image, if it is above a certain threshold then it will be detected as a piece, otherwise it is empty. 



#### example
An application example is shown on the next video, where cut_images and acquire_threshold are used.  
