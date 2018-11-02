#FindChessBoard opencv
import cv2
import numpy as np

#image = cv2.imread('chess3.jpg', 0)
#image = cv2.resize(image, (300, 400))

#print(corners[1][1][0][0])

capture = cv2.VideoCapture(0)
while True:
	_, image = capture.read()

	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	corners = cv2.findChessboardCorners(image, (3, 3), flags=cv2.CALIB_CB_ADAPTIVE_THRESH)
	
	if corners[0]:
		for point in corners[1]:
			x = point[0][0]
			y = point[0][1]
			cv2.circle(image, (x, y), 10, [100, 100, 0], -1)


	cv2.imshow('image', image)
 	k = cv2.waitKey(1) & 0xFF

	if k == ord('q'): #press escape to exit
	    break

capture.release()
cv2.destroyAllWindows()