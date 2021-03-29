'''
The module will get images from the Camera Module V1
using OpenCV.
This images can be displayed as video or not
The idea is to stream this images to another computer
'''

import cv2 as cv #Get OpenCV package

video = cv.VideoCapture(0) #This tells to get the video from the webcam

def getVid(display = False, size = [480, 240]):
    #Dispay can be turned on
    #Size can be changed
    isTrue, frame = capture.read() #Reads video frame by frame
    frame = cv.resize(frame, (size[0], size[1])) #Resize
    if display:
        cv.imshow('Video from the camera', frame)
    
    return frame

if __name__ == '__main__':
    while True:
        frame = getVid(display = True) #Get the video