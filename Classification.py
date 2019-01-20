#This module will be used to classify the squares into three categories, either Color1, Color2 or empty square.
#It takes as input 8*8 array of a lists, each list has an image which is the square that we need, and the value that it has.
#It takes edits accordingly a new matrix, which would have 8*8 elements and places either 1, -1, 0 for Color1, Color2, Empty respectively
import datetime
import cv2
import numpy as np
import os
import math
from scipy.cluster.vq import vq, kmeans, whiten
from matplotlib import pyplot as plt
import operations
from multiprocessing import Pool

#function to calculate the mean of the array
def read_txt():
    txt = open("{}/{}".format(os.getcwd(), "threshold.txt"))
    _, player1 = (txt.readline()).split(':')
    _, player2 = (txt.readline()).split(':')
    txt.close()
    values1 = player1.split(',')
    values2 = player2.split(',')
    for i in range(0, len(values1)):
        values1[i] = int(values1[i])
        values2[i] = int(values2[i])
    return [values1, values2]
def getWhitePercentage(thresholded_image):
    h, w = thresholded_image.shape
    s = h * w
    percentage = 0
    for i in range(0,h):
        for j in range(0,w):
            if thresholded_image[i,j] > 200:
                percentage +=1
    if percentage > (s/3):
        return True
    else:
        return False
#Player1:0,64,0,165,49,184
#Player2:0,180,97,255,68,225
def classifier(frame_hsv, threshold_values):
    [values1, values2] = read_txt()
    [low_H1, high_H1, low_S1, high_S1, low_V1, high_V1] = values1
    [low_H2, high_H2, low_S2, high_S2, low_V2, high_V2] = values2
    #print(values1)
    #print(values2)
    #apply first threshold range from txt file threshold.txt
    f1 = cv2.inRange(frame_hsv, (low_H1, low_S1, low_V1), (high_H1, high_S1, high_V1))
    check1 = getWhitePercentage(f1)
    if check1:
        return 1
    elif not check1:
        f2 = cv2.inRange(frame_hsv, (low_H2, low_S2, low_V2), (high_H2, high_S2, high_V2))
        check2 = getWhitePercentage(f2)
        if check2:
            return -1
        else:
            return 0
def pieces_matrix(list):
    matrix = line_to_square(list)
    output = np.zeros((8, 8))
    for i in range(0,8):
        for j in range(0,8):
            frame_HSV = cv2.cvtColor(matrix[i][j] , cv2.COLOR_BGR2HSV)
            output[i,j] = classifier(frame_HSV, 1)
    return output
def pieces_matrix_paralell(list):



    return 0
def line_to_square(list):
    matrix = []
    row = []
    for i in range(0,64):
        row.append(list[i])
        if (i+1)%8 == 0:
            matrix.append(row)
            row = []
    return matrix
def simpleCheck():
    correct_values = 0
    for i in range(1, 315):
        # read first image
        img = cv2.imread(r"C:\Users\moham\Desktop\myData\pics\({}).jpg".format(i))
        #resized = cv2.resize(img, (h, w), interpolation=cv2.INTER_AREA)
        frame_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        correct = 0
        if i < 31 or i > 122 and i < 185 or i > 214 and i < 281:
            correct = 0
        elif i > 30 and i < 49 or i > 64 and i <93 or i > 280:
            correct = 1
        elif i >48 and i < 65 or i >92 and i <122 or  i > 184 and i < 215:
            correct = -1
        guess = classifier(frame_HSV, 1)
        if guess == correct:
            print(str(i) +"     "+ str(guess) +"     True")
            correct_values +=1
        else:
            print(str(i) + "     " + str(guess) + "     False")
    print('Accuracy:    '+ str(correct_values) +"/314")
if __name__ == '__main__':
    list = []
    for i in range(1,65):
        img = cv2.imread(r"C:\Users\moham\Desktop\myData\pics\({}).jpg".format(i))
        list.append(img)
    print(pieces_matrix(list))
