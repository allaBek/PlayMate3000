import cv2
import numpy as np
import time
import os


drawing = False
point1 = ()
point2 = ()

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
def cut_images():

    cropped_ready = False
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", mouse_drawing)

    player = ["Player_1", "Player_2"]
    background = ["Background_1", "Backrgound_2"]
    light = ["Flash", "No Flash"]

    ### Few notes for users ###
    print('Please consider the following use manual')
    print('Please use the left mouse key to enclose the desired piece by the green square')
    print('Then, please press "s" to mark the square as "desired"')
    print('Then, press "r" to start new cropping session')
    print('If the desired square is well selected, please press "q" to save it')
    print('Please follow the instructions')
    print('If you want to exit the entire program, please press "escape"')

    for p in player:
        try:
            os.mkdir("{}/{}".format(os.getcwd(), p))
        except FileExistsError:
            pass
        image = 1
        for b in background:
            for i in light:
                print('Crop an image of {} {} with {}'.format(p, b,i))
                while True:
                    _, frame = cap.read()
                    frame_draw = frame.copy()

                    if point1 and point2:
                        cv2.rectangle(frame_draw, point1, point2, (0, 255, 0))
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
                    elif c == 27:
                        print('Closing the entire program ...')
                        break

                    if cropped_ready:
                        #Show corpped image
                        cv2.imshow('Cropped', cropped)
                        #Save images to directories
                        if c == ord('q'):
                            cv2.imwrite("{}/{}/{}.jpg".format(os.getcwd(), p, image), cropped)
                            break


                    cv2.imshow("Frame", frame_draw)

                image += 1

                # Escape key to exit
                if c == 27:
                    break
            # Escape key to exit
            if c == 27:
                break
        # Escape key to exit
        if c == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    cut_images()