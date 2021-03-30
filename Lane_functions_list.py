'''
In here we have the functions needed to obtane the curve and lane of the video
We did it separately for a cleaner code
'''

import cv2 as cv
import numpy as np

'''Edson's personal note:
Retry with the treshold function in OpenCV, EOF syntax error
Check tresholding.py'''

def tresholding(video):
    videoHSV = cv.cvtColor(video, cv.COLOR_BGR2HSV) #We change the video to HSV color
    lowerWhite = np.array([80,0,0]) #Values need to be obtain empirically, this one marks the min value of the pixel
    upperWhite = np.array([255,160,255]) #Values obtain with ColorPicker.py, this one marks the max value of the pixel
    maskWhite = cv.inRange(videoHSV, lowerWhite, upperWhite) #We get a black and white video, on and off pixels showing only the path

    return maskWhite

def warping(video, points, width, height, inv = False): #Warping works using linear algebra to transform the image into a square(upper view)
    point1 = np.float32(points) #Points from the camera view (skew square)
    point2 = np.float32([[0,0], [width, 0], [0, height], [width, height]]) #Points if looking from above
    
    if inv:
        matrixTransform = cv.getPerspectiveTransform(point2, point1) #For the display
    else:
        matrixTransform = cv.getPerspectiveTransform(point1, point2) #Transform the original form to the desired perspective

    warpedVideo = cv.warpPerspective(video, matrixTransform, (width, height)) #Uses the matrix to transform the video

    return warpedVideo

def nothing(): #Function needed for the trackbars, no special function.
    pass

def initializeTrackbars(initialTrackbarsVal, widthTarget = 480, heightTarget = 240): #Function that creates trackbars
    cv.namedWindow("Trackbars") #Creates a window for the trackbars
    cv.resizeWindow("Trackbars", 360, 240) #Size of the window

    cv.createTrackbar("Width Top", "Trackbars", initialTrackbarsVal[0], widthTarget//2, nothing) #Create a trackbar
    cv.createTrackbar("Height Top", "Trackbars", initialTrackbarsVal[1], heightTarget, nothing) #heightTarget is the max value
    cv.createTrackbar("Width Bottom", "Trackbars", initialTrackbarsVal[2], widthTarget//2, nothing) #initial Value of the trackbar
    cv.createTrackbar("Height Bottom", "Trackbars", initialTrackbarsVal[3], heightTarget, nothing) #Calls a function when there's a change
    #in the trackbar, we are sending nothing so we create a function for that

def valTrackbars(widthTarget = 480, heightTarget = 240): #Returns the values of the trackbars in real time
    widthTop = cv.getTrackbarPos("Width Top", "Trackbars") #Inputs are the trackbar name and window name
    heightTop = cv.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv.getTrackbarPos("Height Bottom", "Trackbars")

    points = np.float32([(widthTop, heightTop), (widthTarget - widthTop, heightTop), 
                        (widthBottom , heightBottom ), (widthTarget - widthBottom, heightBottom)])
    #Then we create the points from the values of the trackbar
    return points

def drawPoints(video, points): #We draw the points of the trackbars as circles on the video
    for x in range(4): #4 because we have 4 trackbars
        cv.circle(video, (int(points[x][0]), int(points[x][1])), 15, (0,255,0), thickness = -1)
        #The center is each point in the 'points' list we did in the past function
    
    return video #Video with the drawn points

def histogram(video, minPer = 0.1, display = False, region = 1): #We sum up the value of the pixels in the warped video (255 for white and 0 for black)
    #We define a region to evaluate the firsts rows of pixels to get the correct center of the path, 1 is all the image, 4 is the first 1/4 of it.
    if region == 1:
        histValues = np.sum(video, axis = 0) #Sum all the columns, all the pixels in the height
    else:
        histValues = np.sum(video[video.shape[0]//region:,:], axis = 0) #Sum all the pixels in each column only for a define horizontal region
    
    maxVal = np.max(histValues) #We get the Max Value to use it as treshold (Column with the most amount of white pixels)
    #The idea is to later use about 50% of the max value as the lower treshold so that every value under it is considered noise and not path.
    minVal = minPer*maxVal #We get the lower treshold, any value under it is noise and not path

    indexArray = np.where(histValues >= minVal) #We specify everything that is path and get the index of the column and save it in a list
    basePoint = int(np.average(indexArray)) #We get the average of the list to use it as base point (We make it an integer to later plot it)

    #Create a blank image to plot the histogram and draw the base point. (Histogram will be only white pixels describing the path)
    if display:
        vidHist = np.zeros((video.shape[0], video.shape[1], 3), np.uint8) #Create a blank image
        for x,intensity in enumerate(histValues): #We want to plot the index and intensity
            cv.line(vidHist, (x, video.shape[0]), (x, video.shape[0] - intensity//255//region), (255,0,255), thickness = 1)
            #1st Point is the index (horizontal) and height of the video (vid.shape[0])
            #2nd point is again the index and the intensity, we divide by 255 because the number is too high(normalize it), this shows the number of pixels that are on and off
            #We need to susbtract from the height because our top is (0,0) and bottom the Max
            cv.circle(vidHist, (basePoint, video.shape[0]), 20, (0,255,255), thickness = -1)
            #Circle shows the base point
        return basePoint, vidHist

    return basePoint

def stackImages(scale, vidArray): #Code to stack images or videos in just one window
    rows = len(vidArray) 
    columns = len(vidArray[0])
    rowsAvailable = isinstance(vidArray[0], list) #Checks if VidArray[0] is a list (True), if it is, that means we have more than 1 img/vid in a single row
    width = vidArray[0][0].shape[1] #We set the width and height using the one from the first image/video
    height = vidArray[0][0].shape[0]
    if rowsAvailable:
        for x in range (0, rows): #We then move to another row (read second)
            for y in range(0, columns): #We first fill the columns of the first row (read first)
                if vidArray[x][y].shape[:2] == vidArray[0][0].shape [:2]: #If the size of the images/videos are the same
                    vidArray[x][y] = cv.resize(vidArray[x][y], (0, 0), None, scale, scale) #No resize
                else:
                    vidArray[x][y] = cv.resize(vidArray[x][y], (vidArray[0][0].shape[1], vidArray[0][0].shape[0]), None, scale, scale) #Resize it as the first img/video
                if len(vidArray[x][y].shape) == 2: #No channel of color
                    vidArray[x][y]= cv.cvtColor(vidArray[x][y], cv.COLOR_GRAY2BGR) #Change from gray to BGR (3 channels of color)

        imageBlank = np.zeros((height, width, 3), np.uint8) #Blank image
        hor = [imageBlank]*rows

        for x in range(0, rows):
            hor[x] = np.hstack(vidArray[x]) #Horizontal stack
        ver = np.vstack(hor) #Vertical stack
    else:
        for x in range(0, rows):
            if vidArray[x].shape[:2] == vidArray[0].shape[:2]: #If the size of the images/videos are the same
                vidArray[x] = cv.resize(vidArray[x], (0, 0), None, scale, scale) #No resize
            else:
                vidArray[x] = cv.resize(vidArray[x], (vidArray[0].shape[1], vidArray[0].shape[0]), None,scale, scale)  #Resize it as the first img/video
            if len(vidArray[x].shape) == 2: #No channel of color
                vidArray[x] = cv.cvtColor(vidArray[x], cv.COLOR_GRAY2BGR) #Change from gray to BGR (3 channels of color)

        hor = np.hstack(vidArray) #Horizontal stack, since there is just onw img/vid per row, we just stack them horizontally
        ver = hor #Just to stay with 1 variable

    return ver