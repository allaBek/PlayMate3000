import cv2
import numpy as np
def nothing(x):
    pass
def automatedLevels(capture):
    _, frame = capture.read()  # Getting frame from the cameras
    imageSize = frame.size
    #Set the maximum area of a square to the size of image over 64, maximum case is when all board is detected
    maximumArea = int(imageSize / 64)
    threshStep = 15
    areaStep = int (maximumArea / 10)
    bestValue = [0, 0, 0, 0] #NumOfSquares, thresh, area, block
    for loopThreshold in range(1, 10, 1):
        print("loopThresh: " + str(loopThreshold))
        for blockSize in range(3, 49, 2):
            print("blockSize: " + str(blockSize))
            for loopArea in range(maximumArea,25, -25):
                numOfSquares = captureFrames(frame, loopArea, loopThreshold, blockSize)
                if bestValue[0] <= numOfSquares and numOfSquares < 66:
                    bestValue = [numOfSquares, loopThreshold, loopArea, blockSize]
                    print("new maximum  " + str(bestValue))
    return bestValue
def captureFrames(frame, maxArea, threshold, blockSize):

        #################################### Preprocessing ! ##############################################################
        # RGB to Gray
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Kernel used to apply the morphological filter
        kernel = np.ones((5, 5), np.uint8)
        # Thresholding (We got the value f the threshold from the trackbar)
        thresholded = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,blockSize,threshold)
        blur = cv2.GaussianBlur(thresholded, (5, 5), 0)
        ret, thresholded = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Laplacian operator for edge detection
        lap = cv2.Laplacian(thresholded, cv2.CV_64F)  # Applying Laplacian transform
        # Applying gradient morephological filter
        lap = cv2.morphologyEx(lap, cv2.MORPH_GRADIENT, kernel)
        #################################### Preprocessing ended ###########################################################

        #################################### Contours manipulation ########################################################
        # Calculating the contour from the edge detected matrix (Output of the Laplacian operator)
        _, contours, hierarchy = cv2.findContours(lap.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Initializing the nbr of detected squares
        nbrofsquares = 0  # Will be needed to detect the board type and thus the game !
        # Getting min required area of the square to be accepted !
        # Looping through the contours detected previously
        for c in contours:
            # Compute the area of the contour
            area = cv2.contourArea(c)
            if area > maxArea:  # Accept only large enough squares
                peri = cv2.arcLength(c, True)  # Calculate the perimeter of the contour
                # (0.15 was deduced experimentaly) Using Ramer-Douglas-Peucker algorithm for shape detection
                approx = cv2.approxPolyDP(c, 0.15 * peri, True)
                if len(approx) == 4:  # The shape has vertices => either square or rectangle, both are fine
                    # Square detected
                    nbrofsquares += 1  # Increment the nbr of sqaures seen
                    M = cv2.moments(c)  # Getting the moments of the contour
                    cX = int(M["m10"] / M["m00"])  # Getting the x coordinate of the center of the square
                    cY = int(M["m01"] / M["m00"])  # Getting the y coordinate of the center of the square
                else:
                    # if not square, pass !
                    pass
        # If 'q' key was pressed, the loop will break, consequently, the program will exit !
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return 0
        return nbrofsquares
def main():
    capture = cv2.VideoCapture(r"C:\Users\moham\Desktop\20181008_221213.mp4")  # Opening the webcam
    print(automatedLevels(capture))
    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()