import cv2
import numpy as np
import os


################# MAPPING Squares Coordinates in a Matrix ####################

def mapping(tomap):
    sorted_matrix=[[[0,0]]*8 for i in range(8)]
    for i in range(8):
        tomap.sort(key=lambda tup: tup[0])
        a = tomap[i*8:(i+1)*8]
        a.sort(key=lambda tup: tup[1])
        for j in range(8):
                sorted_matrix[j][i] = a[j]
    return sorted_matrix



################# Final Output Matrix as Zeros and Ones  ####################
def Pieces_to_Matrix(circles, sortedMatrix):
    m = 0
    output = np.zeros((8,8))
    for x in range(len(sortedMatrix)):
        for y in range(len(sortedMatrix[0])):
            for c in circles:
                if abs(c[0] - sortedMatrix[x][y][0]) < 3 and abs(c[1] - sortedMatrix[x][y][1]) < 3:
                    sortedMatrix[x][y]
                    output[x][y] = 1

    return output
def findBoard(contours, img, coloured):
    #What this function does is that it takes the contours of the images taken by camera, and the image in gray scale and the coloured image, it returns the board
    #colored image.
    #get the dimensions of the grayscale image
    h, w = img.shape
    #measure the surface of the frame or the number of pixels in all the image, this will be used to limit the size of the board
    frameArea = h*w
    #measure the minimum area that could be set for a board, which is one tenth of the whole image
    s = frameArea / 10
    #this variable will contain the coordinates of the corners
    boardPts = []
    #this variable will take the cropped colored image
    board = []
    # this variable will take the corners points
    pts = 0
    #loop in all the contours of the image, and check for the board by its surface
    for c in contours:
        # Compute the area of the contour
        area = cv2.contourArea(c)
        if area > s:  # Accept only large enough squares
            peri = cv2.arcLength(c, True)  # Calculate the perimeter of the contour
            # (0.10 was deduced experimentaly) Using Ramer-Douglas-Peucker algorithm for shape detection
            approx = cv2.approxPolyDP(c, 0.10 * peri, True)
            if len(approx) == 4:  # The shape has vertices => either square or rectangle, both are fine
                # Square detected
                #check if this square is the smallest square that is larger than image/10, this way we avoid having many squares like the page or the table which are bigger
                #than the board
                if area < frameArea:
                    frameArea = area
                    boardPts = approx
            else:
                # if not square, pass !
                pass
    #check if the array was filled and it is not a null
    if len(boardPts) > 1:
        #set the points of teh border
        pts = setPoints(boardPts)
        #transform the board corners into the cropped image of the board
        board = transformToBoard(coloured, pts)
    #return the board image and the corner points, these will be used later to avoid redoing computations if the board was fully detected
    return [board, pts]
def transformToBoard(img, pts):
    #######this function takes the img, and the corner point and crops the part selected by pts
    #take the top left, top right, bottom right, bottom left corners from the given points
    (tl, tr, br, bl) = pts
    #measure the width from the points, that is simple geometry application of two points distance
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    #choose the largest to width, since the two measurements would not be equal
    maxWidth = max(int(widthA), int(widthB))
    #measure the height from the points, that is simple geometry application of two points distance
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    # choose the largest to height, since the two measurements would not be equal
    maxHeight = max(int(heightA), int(heightB))
    #create a numpy array with the  dimensions of the baord
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], np.float32)
    #find the transformation matrix from image to board
    M = cv2.getPerspectiveTransform(pts, dst)
    #crop the board from the image
    board = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
    #create a border for the image
    bordersize = 10
    bordererImage = cv2.copyMakeBorder(board, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,
                                       borderType=cv2.BORDER_CONSTANT, value=[255, 255, 255])

    return bordererImage


def setPoints(approx):
    #this function sets the points of the corners, meaning it detects which is the top-left, bottom-right ...ect
    #create and empty array of 4*2, 4 coordinates and each is x,y
    rect = np.zeros((4, 2),np.float32)
    #find the sum of the x,y for each point, this way we can deduce the top left ane the bottom right
    s = approx.sum(axis= 2)
    #bottom right has the maximum sum
    rect[2] = approx[np.argmax(s)]
    # Top left has the minimum sum
    rect[0] = approx[np.argmin(s)]
    #find the difference of the coordinates, the lowest should be the bottom left, and the left is the top right
    diff = np.diff(approx, axis= 2)
    rect[1] = approx[np.argmax(diff)]
    rect[3] = approx[np.argmin(diff)]
    return rect
def getBoard(frameColoured, threshold = 0):
    #convert to gray image
    frame = cv2.cvtColor(frameColoured, cv2.COLOR_BGR2GRAY)
    #apply adaptive threshold
    thresholded = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 15, threshold)
    #find countours of the image
    _, contours, _ = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #get the board and the corner points
    [board, pts] = findBoard(contours, frame, frameColoured)
    return [board, pts]
def getPieces(frame, thresholdPieces):
    nbrofsquares = 0
    nbrofcircles = 0
    w, h = frame.shape
    s = w * h
    # Kernel used to apply the morphological filter
    kernel = np.ones((5, 5), np.uint8)
    # Thresholding (We got the value f the threshold from the trackbar)
    _, thresholded = cv2.threshold(frame, thresholdPieces, 255, cv2.THRESH_BINARY)  # Applying threshold
    # Laplacian operator for edge detection
    lap = cv2.Laplacian(thresholded, cv2.CV_64F)  # Applying Laplacian transform
    # Applying gradient morephological filter
    lap = cv2.morphologyEx(lap, cv2.MORPH_GRADIENT, kernel)
    #
    cv2.imshow("lap", lap)
    #################################### Preprocessing ended ###########################################################
    piecesMatrix = []
    #################################### Contours manipulation ########################################################
    # Calculating the contour from the edge detected matrix (Output of the Laplacian operator)
    _, contours, _ = cv2.findContours(lap.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Getting min required area of the square to be accepted !
    # Looping through the contours detected previously


    map_matrix= [[0, 0] for i in range(64)] # map matrix stores the coordinates of every single square within the board
    i, k = 0, 0
    # ends here
    circlesFrame = frame.copy()
    for c in contours:
        # Compute the area of the contour
        area = cv2.contourArea(c)
        if area > (s/220) and area < (s / 10):  # Accept only large enough squares in this range
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
                #Added
                map_matrix[i][k] = cX          # the x coordinates for the c contour stored in map
                map_matrix[i][k + 1] = cY      # the y coordinates for the c contour stored in map
                i += 1

            else:
                # if not square, pass !
                pass
    #################################### Contours manipulation ended ! ########################################################
    cv2.imshow("squares", frame)
    #find circles in the board
    piecesMatrix, frame = getCircles(circlesFrame)
    cv2.imshow("circles", frame)
    map_matrix = map_matrix + piecesMatrix
    map_matrix = filterPositionsMatrix(map_matrix)
    #if we have 64 squares detected, display the results
    if len(map_matrix) == 64:
        # pass message that the board is fully detected
        #detect the pieces in the board using circle detection
        mapped = mapping(map_matrix)  ### using the mapping function we rearrange the stored values in map matrix ###
        Out_matrix = Pieces_to_Matrix(piecesMatrix, mapped)
        print(Out_matrix)
    elif nbrofsquares < 64 and nbrofsquares > 10:
        #pass message that chess board is partially detected message
        pass
    else:
        #pass message that the board cannot be seen in the picture
        pass
    return [nbrofsquares, piecesMatrix,frame]

def filterPositionsMatrix(map):
    map = list(filter(lambda b: b != [0, 0], map))
    for i in range(len(map)):
        map[i].append(map[i][0] + map[i][1])
    map.sort(key=lambda x: x[2])
    repeatedCenters = []
    for i in range(0, len(map)):
        for j in range(i +1, len(map)):
            if abs(map[i][2]  - map[j][2]) < 40 and abs(map[i][1]  - map[j][1]) < 25 and abs(map[i][0]  - map[j][0]) < 25:
                repeatedCenters.append(j)
    for i in range(len(map)):
        del map[i][2]
    for i in repeatedCenters:
        del map[i]
    return map
def getCircles(frame):
    nbrofcircles = 0
    # Getting circles from gray image using hough circle
    circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 1, 24, param1=50, param2=28, minRadius=10,
                               maxRadius=20)
    piecesMatrix = []
    # Casting the content of circles
    if circles is not None:
        circles = np.round(circles[0, :]).astype('int')

        # If board detected, let's detect the pieces !
        for (Cx, Cy, r) in circles:
            nbrofcircles += 1
            cv2.circle(frame, (Cx, Cy), r, (255, 255, 255), 3)
            cv2.rectangle(frame, (Cx - 5, Cy - 5), (Cx + 5, Cy + 5), (0, 128, 255), -1)
            piecesMatrix.append([Cx, Cy])
    return [piecesMatrix, frame]

def nothing(x):
    pass
def main():
    capture = cv2.VideoCapture(r"H:\v2.mp4")  # Opening the webcam
    cv2.namedWindow('frame')  # Giving a name to the window I'll open, needed for the Trackbars
    cv2.createTrackbar('threshold', 'frame', 0, 255,
                       nothing)  # Trackbar to manage threshold values (Threshold filtering)
    cv2.setTrackbarPos('threshold', 'frame', 120)  # Setting Initial threshold value
    nbrofsquares = 0  # Will be needed to detect the board type and thus the game !
    nbrofcircles = 0
    pts = 0
    thresholdBoard = 0

    while True:
        thresholdPieces = cv2.getTrackbarPos("threshold", 'frame')
        # Initializing the nbr of detected squares
        _, frame = capture.read()
        cv2.imshow("original", frame)
        try:
            if nbrofsquares == 64:
                ret = transformToBoard(frame, pts)
                frame = cv2.cvtColor(ret, cv2.COLOR_BGR2GRAY)
            else:
                ret = getBoard(frame, thresholdBoard)
                frame = cv2.cvtColor(ret[0], cv2.COLOR_BGR2GRAY)
                pts = ret[1]
            nbrofsquares, nbrofcircles, img = getPieces(frame, thresholdPieces)
            print("number of circles: " + str(len(nbrofcircles)))
            cv2.imshow("frame", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except (AttributeError):
            print("I am in an error")
    capture.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()