import cv2
import numpy as np


def nothing(x):
    pass


def main():
    capture = cv2.VideoCapture(r"C:\Users\moham\Desktop\v4.mp4")  # Opening the webcam
    cv2.namedWindow('frame')  # Giving a name to the window I'll open, needed for the Trackbars
    cv2.createTrackbar('threshold', 'frame', 0, 255,
                       nothing)  # Trackbar to manage threshold values (Threshold filtering)
    cv2.setTrackbarPos('threshold', 'frame', 127)  # Setting Initial threshold value
    cv2.createTrackbar('Area', 'frame', 0, 3000,
                       nothing)  # Trackbar to set threshold area of the accepted squares (used with shape recognition)
    cv2.setTrackbarPos('Area', 'frame', 300)  # Setting the initial accepted square area to 300 px
    while True:
        _, frame = capture.read()  # Getting frame from the cameras
        #################################### Preprocessing ! ##############################################################
        # RGB to Gray
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Kernel used to apply the morphological filter
        kernel = np.ones((5, 5), np.uint8)
        # Thresholding (We got the value f the threshold from the trackbar)
        threshold = cv2.getTrackbarPos('threshold', 'frame')
        _, thresholded = cv2.threshold(frame, threshold, 255, cv2.THRESH_BINARY)  # Applying threshold
        # Laplacian operator for edge detection
        lap = cv2.Laplacian(thresholded, cv2.CV_64F)  # Applying Laplacian transform
        # Applying gradient morephological filter
        lap = cv2.morphologyEx(lap, cv2.MORPH_GRADIENT, kernel)
        #################################### Preprocessing ended ###########################################################

        #################################### Contours manipulation ########################################################
        # Calculating the contour from the edge detected matrix (Output of the Laplacian operator)
        _, contours, _ = cv2.findContours(lap.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Initializing the nbr of detected squares
        nbrofsquares = 0  # Will be needed to detect the board type and thus the game !
        nbrofcircles = 0
        # Getting min required area of the square to be accepted !
        maxArea = cv2.getTrackbarPos('Area', 'frame')
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
                    nbrofsquares += 1  # Increment the nbr of squres seen
                    M = cv2.moments(c)  # Getting the moments of the contour
                    cX = int(M["m10"] / M["m00"])  # Getting the x coordinate of the center of the square
                    cY = int(M["m01"] / M["m00"])  # Getting the y coordinate of the center of the square
                    cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)  # Drawing the contour
                    # cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)	# Drawing the center of the contour
                    cv2.putText(frame, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                                2)  # Printing "center" above the center point of the contour
                else:
                    # if not square, pass !
                    pass
        #################################### Contours manipulation ended ! ########################################################

        print('I detected %d square !' % (nbrofsquares))  # Printing out the nbr of squares detected !

        if nbrofsquares > 50 and nbrofsquares < 67:
            cv2.putText(frame, "Chess board detected !", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            # Getting circles from gray image using hough circle
            circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 1, 8, param1=50, param2=24, minRadius=8,
                                       maxRadius=20)
            # Casting the content of circles
            if circles is not None:
                circles = np.round(circles[0, :]).astype('int')

                # If board detected, let's detect the pieces !
                for (Cx, Cy, r) in circles:
                    nbrofcircles += 1
                    cv2.circle(frame, (Cx, Cy), r, (255, 255, 255), 3)
                    cv2.rectangle(frame, (Cx - 5, Cy - 5), (Cx + 5, Cy + 5), (0, 128, 255), -1)
        elif nbrofsquares < 64 and nbrofsquares > 10:
            cv2.putText(frame, "Chess board partially detected !", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (255, 255, 255), 2)
        else:
            cv2.putText(frame, "I Can't see the board !", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        print('I detected %d piece !' % nbrofcircles)

        cv2.imshow("frame", frame)  # Showing the frame !

        # If 'q' key was pressed, the loop will break, consequently, the program will exit !
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()