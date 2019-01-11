#This module is used to obtain threshold values for the HSV filter used to classify the image, it reads images saved on folders player1 and player2
#And process them individually.


from __future__ import print_function
import cv2 as cv
import argparse
import os
#Player1:0,64,0,165,49,184
#Player2:134,180,74,255,101,255

#Initialize values
max_value = 255
max_value_H = 360 // 2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
#check if an element on a directory is a file or not, return iterative containing these files
def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file
#Call back function
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = max(min(high_H - 1, low_H), 0)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)

#Call back function
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H + 1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)

#Call back function
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = max(min(high_S - 1, low_S),0)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)

#Call back function
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S + 1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)

#Call back function
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = max(min(high_V - 1, low_V),0)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)

#Call back function
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V + 1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)
#Define the paths used to get the images, for MAC users change \\ into /
path1 = "{}\\{}".format(os.getcwd(), "Player_1")
path2 = "{}\\{}".format(os.getcwd(), "Player_2")
#initiatate lists to contain the images
list_of_images_1 = []
list_of_images_2 = []
for file in files(path1):
    if("jpg" in file or "png" in file):
        list_of_images_1.append(file)
for file in files(path2):
    if("jpg" in file or "png" in file):
        list_of_images_2.append(file)
#initialiaze parameters
past_low_H = 180
past_high_H =0
past_low_S= 180
past_high_S = 0
past_low_V = 180
past_high_V = 0
#create windows
cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)
cv.createTrackbar(low_H_name, window_detection_name, low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name, high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name, low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name, high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name, low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name, high_V, max_value, on_high_V_thresh_trackbar)
#iterate over images of player1
for i in list_of_images_1:
    while True:
        img = cv.imread(r"{}\{}".format(path1, i))
        #resize images to have a readable image if the size was too small
        frame = cv.resize(img, (250, 250), interpolation=cv.INTER_AREA)
        #check if the imafe was read successfully
        if frame is None:
            break
        #convert RGB to HSV
        frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        #Apply the threshold on the image
        frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
        #show images
        cv.imshow(window_capture_name, frame)
        cv.imshow(window_detection_name, frame_threshold)
        key = cv.waitKey(30)
        if key == ord('q') or key == 27:
            break
    #update threshold parameters
    past_high_H = max(high_H, past_high_H)
    past_high_S = max(high_S, past_high_S)
    past_high_V = max(high_V, past_high_V)
    past_low_H = max(min(past_low_H, low_H),0)
    past_low_S = max(min(past_low_S, low_S),0)
    past_low_V = max(min(past_low_V, low_V),0)
    high_H = past_high_H
    high_S = past_high_S
    high_V = past_high_V
    low_H = past_low_H
    low_S = past_low_S
#write to text file
txt = open("threshold.txt", "wt")
txt.write("Player1:{},{},{},{},{},{}\n".format(low_H, high_H, low_S, high_S, low_V, high_V))
#initiate parameters
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
past_low_H = 0
past_high_H =0
past_low_S= 0
past_high_S = 0
past_low_V = 0
past_high_V = 0
#iterate over player2 images
for i in list_of_images_2:
    while True:
        #read image
        img = cv.imread(r"{}\{}".format(path2, i))
        #resize image to obtain readable image
        frame = cv.resize(img, (250, 250), interpolation=cv.INTER_AREA)
        #check if frame is read successfully
        if frame is None:
            break
        #convert RGB to HSV
        frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        #Apply threshold
        frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
        #show images
        cv.imshow(window_capture_name, frame)
        cv.imshow(window_detection_name, frame_threshold)
        key = cv.waitKey(30)
        if key == ord('q') or key == 27:
            break
        past_high_H = max(high_H, past_high_H)
        past_high_S = max(high_S, past_high_S)
        past_high_V = max(high_V, past_high_V)
        past_low_H = min(past_low_H, low_H)
        past_low_S = min(past_low_S, low_S)
        past_low_V = min(past_low_V, low_V)
        high_H = past_high_H
        high_S = past_high_S
        high_V = past_high_V
        low_H = past_low_H
        low_S = past_low_S
        low_V = past_low_V
#update text file with player2 thresholds
txt.write("Player2:{},{},{},{},{},{}\n".format(low_H, high_H, low_S, high_S, low_V, high_V))
txt.close()