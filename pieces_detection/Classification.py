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

#function to read the values of HSV saved in txt file
def read_txt():
    txt = open("{}\\{}".format(os.getcwd(), "threshold.txt"))
    _, player1 = (txt.readline()).split(':')
    _, player2 = (txt.readline()).split(':')
    txt.close()
    values1 = player1.split(',')
    values2 = player2.split(',')
    for i in range(0, len(values1)):
        values1[i] = int(values1[i])
        values2[i] = int(values2[i])
    return [values1, values2]

#Function to Compute the percentage of white part on the processed image, indicating precesne of a piece
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
def classifier(frame_hsv):
    [values1, values2] = read_txt()
    [low_H1, high_H1, low_S1, high_S1, low_V1, high_V1] = values1
    [low_H2, high_H2, low_S2, high_S2, low_V2, high_V2] = values2
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
            output[i,j] = classifier(frame_HSV)
    return output
#To be constructed, parallel processing pool for the classificaton algorithm
def pieces_matrix_paralell(list):
    return 0
#This function is used to convert a linear list of 1*64 into an 8*8 matrix
def line_to_square(list):
    matrix = []
    row = []
    for i in range(0,64):
        row.append(list[i])
        if (i+1)%8 == 0:
            matrix.append(row)
            row = []
    return matrix

if __name__ == '__main__':
    list = []
    for i in range(1,65):
        img = cv2.imread(r"C:\Users\moham\Desktop\myData\pics\({}).jpg".format(i))
        list.append(img)
    print(pieces_matrix(list))
