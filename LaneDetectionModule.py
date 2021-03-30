'''
The idea of this module is to use the video captured by the webcam to get the path
First we identify the path with treshold (pixels)
We then transform the view to look at it from the top
With the transformed image we count to pixels to look for the curve
'''

import cv2 as cv
import numpy as np
import Lane_functions_list

curveList = []
avgVal = 10 #Average 10 values

def getLaneCurve(video, display = 2): #1 displays results and 2 displays the complete pipeline, any other number doesn't display anything.
    videoCopy = video.copy() #Copy of the video, so we do not work on the original
    vidResult = video.copy()

    # STEP 1
    videoTresh = Lane_functions_list.tresholding(video) #Obtains the treshold video from utilities
    
    # STEP 2
    h, w, c = video.shape #Height, width and chanel
    points = Lane_functions_list.valTrackbars() #Points needed for the matrix to warp the video
    videoWarp = Lane_functions_list.warping(videoTresh, points, w, h) #Obtains the warped video
    videoCircles = Lane_functions_list.drawPoints(videoCopy, points) #Draws circles of the points chosen in the copy of the video
    
    # STEP 3
    midPoints, vidHist = Lane_functions_list.histogram(videoWarp, display = True, minPer = 0.5, region = 4)
    curveAvgPoints, vidHist = Lane_functions_list.histogram(videoWarp, display = True, minPer = 0.9)
    #middle point if for the middle point of the path taking only 1/4 of the video, so we can use the real center
    #curveAvPoints takes all the image and gets the average, we use both to determine the curve
    curve_raw = curveAvgPoints - midPoints
    
    # STEP 4
    #Averaging to get a smooth transition, it reduces the noise.
    curveList.append(curve_raw) #Creates a list with the raw values of the curve obtained
    if len(curveList) > avgVal:
        curveList.pop(0) #Takes out the first value, to always keep the list of a certain size
    
    curve = int(sum(curveList)/len(curveList)) #We get the average and define the curve value
    
    # STEP 5
    #Display
    if display != 0: #We get al the videos needed to be displayed
       vidInvWarp = Lane_functions_list.warping(videoWarp, points, w, h, inv = True) #Gets the warped video
       vidInvWarp = cv.cvtColor(vidInvWarp, cv.COLOR_GRAY2BGR)
       vidInvWarp[0:h//3, 0:w] = 0,0,0
       vidLaneColor = np.zeros_like(video) #Blank image of the same size as the original video
       vidLaneColor[:] = 0,255,0 #Define the color of the pixels
       vidLaneColor = cv.bitwise_and(vidInvWarp, vidLaneColor) #AND operation to draw the pixels of the path
       vidResult = cv.addWeighted(vidResult, 1, vidLaneColor, 1, 0) #Both videos have the same wigth (1) and no additional sum (0)
       midY = 450 #???
       cv.putText(vidResult, str(curve), (w//2-80, 85), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), thickness = 3) #Write the value of the curve in the video
       cv.line(vidResult, (w//2, midY), (w//2 + (curve*3), midY), (0,255,0), thickness = 5) #Line drawn in the path of the result video
       cv.line(vidResult, ((w//2 + (curve*3)), midY - 25), (w//2 + (curve*3), midY + 25), (0,255,0), thickness = 3)
       for x in range(-30, 30):
           wT = w//20
           cv.line(vidResult, (wT*x + int(curve//50), midY - 10),
                    (wT*x + int(curve//50), midY + 10), (0,0,255), 2)
       #fps = cv.getTickFrequency() / (cv.getTickCount() - timer)
       #cv.putText(vidResult, 'FPS '+ str(int(fps)), (20, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3)
    if display == 2:
        vidStacked = Lane_functions_list.stackImages(0.7, ([video, videoCircles, videoWarp], [vidHist, vidLaneColor, vidResult]))
        #Stack functions just stacks all the images together in one, 0.7 is the scale
        cv.imshow('Video Stacked', vidStacked)
    elif display == 1:
        cv.imshow('Results', vidResult)

    curve = curve/100 #Normalization, 100 is a random number but useful
    if curve > 1:
        curve == 1
    elif curve < -1:
        curve == -1
    
    return curve #We get the curve values from -1 to 1, for the MotorModule


if __name__ == '__main__':
    capture = cv.VideoCapture('Vid_lane_test_1.mp4') #Search for test video
    initialTrackbarsVal = [102, 80, 20, 214] #Values obtained empirically
    Lane_functions_list.initializeTrackbars(initialTrackbarsVal) #Give the values to the trackbars
    frameCounter = 0
    curveList = []
    while True:
        frameCounter +=1 #This is for the video to stay in loop
        if capture.get(cv.CAP_PROP_FRAME_COUNT) == frameCounter:
            capture.set(cv.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0 #restart video

        isTrue, frame = capture.read() #Reads video frame by frame
        frame = cv.resize(frame, (480, 240)) #Resize the video
        curve = getLaneCurve(frame, display = 2) #Gets the curve value

        if cv.waitKey(20) & 0xFF==ord('d'): #Stops the video from playing indefinetly if key d is pressed
            break
        
    capture.release()
    cv.destroyAllWindows()
