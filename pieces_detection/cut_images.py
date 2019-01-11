import cv2
import numpy as np
import time
import os
#initiate variables
drawing = False
point1 = ()
point2 = ()
#This fucnton is used to take the button clicks coodinates to be used late n cropping images
def mouse_drawing(event, x, y, flags, params):
    global point1, point2, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing is False:
            drawing = True
            point1 = (x, y)
        else:
            drawing = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            point2 = (x, y)
#This function crops pieces of the images
def cut_images():
    cropped_ready = False
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", mouse_drawing)
    player = ["Player_1", "Player_2"]
    background = ["Background_1", "Backrgound_2"]
    light = ["Flash", "No Flash"]
    for p in player:
        try:
            os.mkdir("{}\\{}".format(os.getcwd(), p))
        except FileExistsError:
            pass
        image = 1
        for b in background:
            for i in light:
                print('Crop an image of {} {} with {}'.format(p, b,i))
                while True:
                    _, frame = cap.read()
                    cv2.imshow("Frame", frame)
                    if point1 and point2:
                        cv2.rectangle(frame, point1, point2, (0, 255, 0))
                    c = cv2.waitKey(1) & 0xFF
                    if c == ord('s'):
                        cropped_ready = True
                        if point1[0] <= point2[0]:
                            if point1[1] <= point2[1]:
                                cropped = frame[point1[1]:point2[1], point1[0]:point2[0]]
                            else:
                                cropped = frame[point2[1]:point1[1], point1[0]:point2[0]]
                        else:
                            if point1[1] <= point2[1]:
                                cropped = frame[point1[1]:point2[1], point2[0]:point1[0]]
                            else:
                                cropped = frame[point2[1]:point1[1], point2[0]:point1[0]]

                    elif c == ord('r'):
                        cropped_ready = False
                        cv2.destroyWindow('Cropped')

                    if cropped_ready:
                        #Show corpped image
                        cv2.imshow('Cropped', cropped)
                        #Save images to directories, MAC or Linux users need tpo be changed to \\ to /
                        if c == ord('q'):
                            cv2.imwrite("{}\\{}\\{}.jpg".format(os.getcwd(), p, image), cropped)
                            break
                image += 1
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    cut_images()