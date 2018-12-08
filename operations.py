

class operations():

    def reArrange(matrix, r, c):
        ### initialize the matrix where the sorted values will be
        # r for rows, and c for columns of matrix,
        sorted_matrix = [[[0, 0]] * c for i in range(r)]
        # looping through the columns, i ,
        for i in range(c):
            # sorting according to x coordinate
            matrix.sort(key=lambda tup: tup[0])
            # we take each column apart and re arrange its y coordinate
            a = matrix[i * r:(i + 1) * r]
            a.sort(key=lambda tup: tup[1])
            # storing the sorted values in the i column,
            for j in range(r):
                if a[j] != [0, 0]:
                    sorted_matrix[j][i] = a[j]
                else:
                    pass
        # the resulted sorted matrix is sorted_matrix
        return sorted_matrix

    def getCorners(mapped):
        #This function aims to get the baord corners out of the 
        #matrix of mapped internal line intersections in the squares
        
        #we get 4 corners pairs, each pair is x and y
        corners=[[0,0] for i in range(4)]
        # number of rows r, and number of columns c in input matrix.
        r=len(mapped)
        c=len(mapped[0])
        # each corner is calculated by 3 neighbour points
        #Top left corner coordinates:
        corners[0][0] = 2 * mapped[0][0][0] - mapped[1][1][0]
        corners[0][1] = 2 * mapped[0][0][1] - mapped[1][1][1]
        # Top right corner coordinates:
        corners[1][0] = 2 * mapped[0][c-1][0] - mapped[1][c-2][0]
        corners[1][1] = 2 * mapped[0][c-1][1] - mapped[1][c-1][1]
        # buttom left corner coordinates:
        corners[2][0] = 2 * mapped[r-1][0][0] - mapped[r-2][1][0]
        corners[2][1] = 2 * mapped[r-1][0][1] - mapped[r-2][1][1]
        # buttom right corner coordinates:
        corners[3][0] = 2 * mapped[r-1][c - 1][0] - mapped[r-2][c - 2][0]
        corners[3][1] = 2 * mapped[r-1][c - 1][1] - mapped[r-2][c-2][1]
        return corners
    
    def getCorners2(mapped):
        a=mapped
        x=[]
        y=[]
        r=len(mapped)
        c=len(mapped[0])
        for i in range(r):
            for j in range(c):
                x.append([a[i][j][0]])
                y.append([a[i][j][1]])

        min_x=x.index(min(x))
        a1=int((min_x-min_x%r)/r)
        b1=min_x%r
        x1y1=a[a1][b1]

        max_y=y.index(max(y))
        a2=int((max_y-max_y%r)/r)
        b2=max_y%r
        x2y2=a[a2][b2]

        min_y=y.index(min(y))
        a3=int((min_y-min_y%r)/r)
        b3=min_y%r
        x3y3=a[a3][b3]

        max_x=x.index(max(x))
        a4=int((max_x-max_x%r)/r)
        b4=max_x%r
        x4y4=a[a4][b4]

        temp=x2y2
        x2y2=x3y3
        x3y3=temp
    if abs(x1y1[1]-x3y3[1])<5 or abs(x2y2[1]-x4y4[1])<5 or abs(x2y2[0]-x3y3[0])<30 or abs(x1y1[1]-x2y2[1])<50:
            x1y1=mapped[0][0]
            x2y2=mapped[0][c-1]
            x3y3=mapped[r-1][0]
            x4y4=mapped[r-1][c-1]
        else:
            pass
        # print(x1y1,x2y2,x3y3,x4y4)
        
        corners=[[0,0] for i in range(4)]

        corners[0][0]=x1y1[0]-(x4y4[0]-x1y1[0])/r
        corners[0][1]=x1y1[1]-(x4y4[1]-x1y1[1])/r
        
        corners[1][0]=x2y2[0]-(x3y3[0]-x2y2[0])/r
        corners[1][1]=x2y2[1]-(x3y3[1]-x2y2[1])/r
        
        corners[2][0]=x3y3[0]-(x2y2[0]-x3y3[0])/r
        corners[2][1]=x3y3[1]-(x2y2[1]-x3y3[1])/r

        corners[3][0]=x4y4[0]-(x1y1[0]-x4y4[0])/r
        corners[3][1]=x4y4[1]-(x1y1[1]-x4y4[1])/r
        return corners

    
    def imageSlices(image,mapped_matrix,corners):
        #This function cuts down the image in small images according to
        # a matrix of intersection points and corners.
        #intially x and y are in top left
        x=int(corners[0][0])
        y=int(corners[0][1])

        # w is the width which by we cut each small picture
        w=int(mapped_matrix[0][1][0]-mapped_matrix[0][0][0])
        # h is the height which by we cut each small picture
        h=int(mapped_matrix[1][0][1]-mapped_matrix[0][0][1])
        # number of rows r, and number of columns c in input matrix.
        r = len(mapped_matrix)+1
        c = len(mapped_matrix[0])+1
        # we shall store all the output small images into the matrix
        #  small_images:
        stored_images=[]
        # looping and cutting:
        for i in range(r):
                if i==0:
                    for j in range(c):
                        cropped_image=image[y:y+h,x:x+w]
                        stored_images.append(cropped_image)
                        x=x+w
                else:
                    x = int(corners[0][0])
                    # y = int(mapped_matrix[0][i - 1][1])
                    y=y+h
                    for j in range(c):
                        cropped_image = image[y:y + h, x:x + w]
                        stored_images.append(cropped_image)
                        # x = int(mapped_matrix[i-1][j-1][0])
                        x=x+w
        return stored_images
    
    def imageSlices2(image, height=400, width=400,r=8,c=8):
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
 
