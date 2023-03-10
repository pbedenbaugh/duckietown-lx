from typing import Tuple

import cv2
import numpy as np


turnlow = 1
turnmed = 2
turnhigh = 3
urgent   = 4.0

zlut = np.array([[315,0],[315,64],[480,128],[480,0]]) # zone for urgent turn, left side
zrut = np.array([[315,640],[315,640-64],[480,640-128],[480,640]]) # zone for urgent turn, right side

zllt1 = np.array([[150,0],[150,308],[315,154],[315,0]]) #zone for low turn, left side
zllt2 = np.array([[315,154],[408,90],[315,64]])
zrlt1 = np.array([[150,680],[150,680-308],[315,680-154],[315,680]]) #zone for low turn, right side
zrlt2 = np.array([[315,680-154],[408,680-90],[315,680-64]])



def get_motor_left_matrix(shape: Tuple[int, int]) -> np.ndarray:
    # TODO: write your function instead of this one
    res = np.zeros(shape=shape, dtype="float32")
    # these are random values
    ###res[100:150, 100:150] = 1y
    ###res[300:, 200:] = 1
    #hard turn away from object at edge
    for xpos in range(shape[1]):
        for ypos in range(shape[0]):
            ltest = cv2.pointPolygonTest(zlut,(ypos,xpos),False)
            rtest = cv2.pointPolygonTest(zrut,(ypos,xpos),False)
            if(ltest>=0):
                res[ypos,xpos] = urgent
            elif(rtest>=0):
                res[ypos,xpos] = urgent
    # gentle turn zone
    for xpos in range(shape[1]):
        for ypos in range(shape[0]):
            ltest = ((cv2.pointPolygonTest(zllt2,(ypos,xpos),False) >=0)or (cv2.pointPolygonTest(zllt1,(ypos,xpos),False)>=0))
            rtest = (cv2.pointPolygonTest(zrlt2,(ypos,xpos),False)>=0) or (cv2.pointPolygonTest(zrlt1,(ypos,xpos),False)>=0)
            if(ltest):
                res[ypos,xpos] = turnlow
            elif(rtest):
                res[ypos,xpos] = turnlow

            

    print(res.shape)
    #print(len(yascend))
  
    # ---
    return res


def get_motor_right_matrix(shape: Tuple[int, int]) -> np.ndarray:
    # TODO: write your function instead of this one
    res = np.zeros(shape=shape, dtype="float32")
    ymax = shape[0]-1
    xmax = shape[1]-1
    horizon = ymax//4
    xmid = xmax//2
    
    xascend = [(ll - xmid)/ (xmax/2) for ll in range(xmax)]
    xdescend = [-ll for ll in xascend]

    yascend = [ll/(ymax-horizon) for ll in range(ymax - horizon)]
    yascend = [yascend[ll]*yascend[ll] for ll in range(len(yascend))]

    deltascale = -0.25
    rampscale = 1.0
    midwidth = xmax//5
    deltazone = [ll + xmid - 50 for ll in range(midwidth)]
    leftzone  = [ll + xmid - (midwidth//2) - midwidth for ll in range(midwidth)]
    rightzone = [ll + xmid + (midwidth//2) for ll in range(midwidth)]

    # main difference of linear rampa connection
    for xpos in range(xmax):
        for ypos in [ll + horizon +1 for ll in range(len(yascend))]:
            res[ypos,xpos] = rampscale*(yascend[ypos-horizon-1] *yascend[ypos-horizon-1] * xascend[xpos])
    # difference for close up objects in center
    for xpos in deltazone:
        for ypos in range(ymax -  3*horizon//2, ymax):
            res[ypos,xpos] =res[ypos,xpos] - deltascale * np.sign(xpos-xmid)      
    for xpos in leftzone:
        for ypos in range(ymax - 2*horizon, ymax):
            res[ypos,xpos] = res[ypos,xpos] + deltascale/4
    for xpos in rightzone:
        for ypos in range(ymax - 2*horizon, ymax):
            res[ypos,xpos] = res[ypos,xpos] - deltascale/4
    #go ahead for clear path in center
    for xpos in deltazone:
        for ypos in range(horizon,(ymax - horizon)):
            res[ypos,xpos] = res[ypos,xpos] - np.abs(deltascale)/6             
    #back up fast - you are about to crash
    #backscale = -1
    backscale = -3
    for ypos in range(ymax-ymax//10,ymax):
        for xpos in range(xmax):
            res[ypos,xpos] = res[ypos,xpos]+backscale

    # ---
    return res
