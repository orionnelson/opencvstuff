import numpy as np
import cv2
import imutils
import random as rd
from operator import itemgetter

#find all the squares in  image.jpg and order them by size


def sortsize(image):
    img = cv2.imread(image)
    #Empty Squares Array
    squares=[]

    #Edge and dialate to get thicker shapes
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(img, 91, 255, cv2.THRESH_BINARY)[1]
    #cv2.imshow('thresh',thresh)
    edged = cv2.Canny(thresh, 5, 700,8)
    kernel = np.ones((12, 12), 'uint8')
    edged = cv2.dilate(edged, kernel, iterations=1)
    #cv2.imshow('edged',edged)

    #Invert because findcontours looks for white objects.
    edged = np.invert(edged)
    # Use cv2 to find all of the squares in the image by using contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    #limit 10 squares.
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
    screenCnt = None
    biggest = 0
    bigcontour = None
    img2 = img.copy()
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.0225 * peri, True)
        rect = cv2.minAreaRect(approx)
        #rect = (rect[0],(rect[1][0]+12,rect[1][1]),rect[2]) # (center(x, y), (width, height), angle of rotation)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        #cv2.drawContours(img2, [box], -1, (rd.randint(0,255), rd.randint(0,255), rd.randint(0,255)), 1)
        #area = cv2.contourArea(c)
        area=int(rect[1][0]*rect[1][1])
        rectboxarea =(rect,box,area)
        squares.append(rectboxarea)
        if (area > biggest and len(approx)==4):
            biggest = area
            bigcontour = box
            screenCnt= (approx)
            #print("Set New Card")
        if(bigcontour is not None):
           pass
           #cv2.drawContours(img2, [box], -1, (rd.randint(0,255), rd.randint(0,255), rd.randint(0,255)), 2)
           #cv2.imshow("Card Found", img2)
           #cv2.waitKey(0)
           #print(rect)
    squares = sorted(squares,key=lambda x: int(x[2]),reverse=True)
    #cv2.imshow('Recolored',img2)
    for x in range(0,len(squares)):
        area = squares[x][2]
        center = squares[x][0][0]
        center = np.int0(center)
        print(str(area) + " " + str( center))
        img = cv2.putText(img,str(x+1),center,cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 0),2,cv2.LINE_AA)
    cv2.imshow(str(image),img)    
    return


sortsize("test.jpg")
sortsize("test2.jpg")
sortsize("test3.jpg")
sortsize("test4.jpg")
sortsize("test5.jpg")
cv2.waitKey(0)
