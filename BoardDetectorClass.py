
import cv2
import numpy as np
import logging

class BoardDetector:

    def imageSlices2(self,image, height=400, width=400, r=8,c=8):
        # This function cuts down the image in small images
        # starting from x,y=0,0
        x = 0
        y = 0
        # w is the width which by we cut each small picture
        w=int(height/8)
        # h is the height which by we cut each small picture
        h=int(width/8)
        # we shall store all the output small images into the matrix
        #  small_images:
        stored_images = []
        # looping and cutting:
        for i in range(r):
            for j in range(c):
                cropped_image = image[y:y + h, x:x + w]
                stored_images.append(cropped_image)
                x = x + w 
            x = 0
            y = y + h 
        return stored_images

    def reArrange(self, matrix, r, c):
        ### initialize the matrix where the sorted values will be
        # r for rows, and c for columns of matrix,
        sorted_matrix = [[[0, 0]] * c for i in range(r)]
        # looping through the columns, i ,
        for i in range(c):
            # sorting according to x coordinate
            matrix.sort(key=lambda tup: tup[0])
            # we take each column apart and re arrange its y
            a = matrix[i * r:(i + 1) * r]
            a.sort(key=lambda tup: tup[1])
            # storing the sorted values in the i column,
            for j in range(r):
                if a[j] != [0, 0]:
                    sorted_matrix[j][i] = a[j]
        # the resulted sorted matrix is sorted_matrix
        return sorted_matrix

    def getCorners(self, mapped):
        corners = [[0, 0] for i in range(4)]
        r = len(mapped)
        c = len(mapped[0])
        corners[0][0] = 2 * mapped[0][0][0] - mapped[0][1][0]
        corners[0][1] = 2 * mapped[0][0][1] - mapped[1][0][1]

        corners[1][0] = 2 * mapped[0][c - 1][0] - mapped[0][c - 2][0]
        corners[1][1] = 2 * mapped[0][c - 1][1] - mapped[1][c - 2][1]

        corners[2][0] = 2 * mapped[r - 1][0][0] - mapped[r - 1][1][0]
        corners[2][1] = 2 * mapped[r - 1][0][1] - mapped[r - 2][1][1]

        corners[3][0] = 2 * mapped[r - 1][c - 1][0] - mapped[r - 1][c - 2][0]
        corners[3][1] = 2 * mapped[r - 1][c - 1][1] - mapped[r - 2][c - 1][1]
        return corners


    def board_detector(self, frame):

        colored_frame = frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        patternfound,corners = cv2.findChessboardCorners(frame, (7, 7),
                                   flags=cv2.CALIB_CB_NORMALIZE_IMAGE |cv2.CALIB_CB_ADAPTIVE_THRESH |cv2.CALIB_CB_FAST_CHECK)

        map_matrix = [[0, 0] for i in range(49)]

        if (patternfound):
            points = corners.tolist()
            map_matrix = [[0, 0] for i in range(49)]

            for k in range(49):
                map_matrix[k] = points[k][0]

            cv2.cornerSubPix(frame, corners, (11, 11), (-1, -1),
                             (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.1))

            #cv2.drawChessboardCorners(colored_frame, (7, 7), corners, patternfound)
            
            sorted = self.reArrange(map_matrix, 7, 7)
            
            cornersbound = self.getCorners(sorted)
            
            pts2 = np.float32([[0, 0], [400, 0], [0, 400], [400, 400]])
            
            pts1 = np.float32([[cornersbound[0][0], cornersbound[0][1]], [cornersbound[1][0], cornersbound[1][1]],
                              [cornersbound[2][0], cornersbound[2][1]], [cornersbound[3][0], cornersbound[3][1]]])

            matrix = cv2.getPerspectiveTransform(pts1, pts2)



            board = cv2.warpPerspective(colored_frame, matrix, (400, 400))
            #cv2.imshow('only the board', board)

            #cv2.imshow('frame', frame)
            # Remember to return also the coordonates of the final augmented board!!!!
            return patternfound, board
        
        else: # If the board was not found, return false
            return patternfound, []
