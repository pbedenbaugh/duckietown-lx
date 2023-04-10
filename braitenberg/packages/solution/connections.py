from typing import Tuple

import cv2
import numpy as np

# 3.21673


turnlow = 0.75
turnmed = 1.25#1.5#1.0 # 2.0#
turnhigh = 3.0#2.0#1.5#2.5#3.0
urgent   = 3.0#2.5#2.0

urgentratio = 0.3

brakes = 5.0
brakeratio = 0.4 #*#  0.35 # 0.45 # 0.3


#evaluation script
#for ii in `find . -name results.yaml -print`; do grep distance-from-start_max $ii; done | sort -n | unique oooo; cat oooo
# for ii in `find . -name results.yaml -print`; do grep distance-from-start_max $ii; done | sort -n | unique oooo; cat oooo; awk 'BEGIN {total = 0; count = 0} { total += $2; count +=1;} END {avg = total/count; print avg}' oooo
zlut = np.array([[315,0],[315,64],[480,128],[480,0]]) # zone for urgent turn, left side
zrut = np.array([[315,640],[315,640-64],[480,640-128],[480,640]]) # zone for urgent turn, right side

zllt = np.array([[150,0],[150,308],[408,90],[315,64],[315,0]]) #zone for low turn, left side
zrlt = np.array([[150,680],[150,640-308],[408,640-90],[315,640-64],[315,640]]) #zone for low turn, right side

zlmt = np.array([[150,308],[150,312],[480,128],[408,90]]) #zone for medium turn, left side
zrmt = np.array([[150,640-308],[150,640-312],[480,640-128],[408,640-90]]) #zone for medium turn, right side

zlht = np.array([[150,312],[150,320],[397,320],[397,318],[480,192],[480,128]]) #zone for medium turn, left side
zrht = np.array([[150,640-312],[150,640-320],[397,640-320],[397,640-318],[480,640-192],[480,640-128]]) #zone for medium turn, right side

zrev = np.array([[397,318],[397,322],[480,448],[480,192]])
zrevleft  = np.array([[397,318],[397,319],[480,319],[480,192]])
zrevright = np.array([[397,320],[397,322],[480,448],[480,319]])

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
                res[ypos,xpos] = -urgent*urgentratio
            elif(rtest>=0):
                res[ypos,xpos] = -urgent
    # gentle turn zone
    # 
    for xpos in range(shape[1]):
        for ypos in range(shape[0]):
            ltest = cv2.pointPolygonTest(zllt,(ypos,xpos),False)
            rtest = cv2.pointPolygonTest(zrlt,(ypos,xpos),False)
            if(ltest>=0):
                res[ypos,xpos] = turnlow
            elif(rtest>=0):
                res[ypos,xpos] = -turnlow    

    # medium turn zone
    for xpos in range(shape[1]):
        for ypos in range(shape[0]):
            ltest = cv2.pointPolygonTest(zlmt,(ypos,xpos),False)
            rtest = cv2.pointPolygonTest(zrmt,(ypos,xpos),False)
            if(ltest>=0):
                res[ypos,xpos] = turnmed
            elif(rtest>=0):
                res[ypos,xpos] = -turnmed   

            
    # hard turn zone
    for xpos in range(shape[1]):
        for ypos in range(shape[0]):
            ltest = cv2.pointPolygonTest(zlht,(ypos,xpos),False)
            rtest = cv2.pointPolygonTest(zrht,(ypos,xpos),False)
            if(ltest>=0):
                res[ypos,xpos] = turnhigh
            elif(rtest>=0):
                res[ypos,xpos] = -turnhigh

    # reverse zone
    for xpos in range(shape[1]):
        for ypos in range(shape[0]):
            lrevtest = cv2.pointPolygonTest(zrevleft, (ypos,xpos),False)
            rrevtest = cv2.pointPolygonTest(zrevright,(ypos,xpos),False)

            if(lrevtest>=0):
                res[ypos,xpos] = -brakes*brakeratio
            elif(rrevtest>=0):
                res[ypos,xpos] = -brakes    
                        



    print(res.shape)
    #print(len(yascend))
  
    # ---
    return res


def get_motor_right_matrix(shape: Tuple[int, int]) -> np.ndarray:
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
                res[ypos,xpos] = -urgent
            elif(rtest>=0):
                res[ypos,xpos] = -urgent*urgentratio
    # gentle turn zone
    # 
    for xpos in range(shape[1]):
        for ypos in range(shape[0]):
            ltest = cv2.pointPolygonTest(zllt,(ypos,xpos),False)
            rtest = cv2.pointPolygonTest(zrlt,(ypos,xpos),False)
            if(ltest>=0):
                res[ypos,xpos] = -turnlow
            elif(rtest>=0):
                res[ypos,xpos] = turnlow    

    # medium turn zone
    for xpos in range(shape[1]):
        for ypos in range(shape[0]):
            ltest = cv2.pointPolygonTest(zlmt,(ypos,xpos),False)
            rtest = cv2.pointPolygonTest(zrmt,(ypos,xpos),False)
            if(ltest>=0):
                res[ypos,xpos] = -turnmed
            elif(rtest>=0):
                res[ypos,xpos] = turnmed   

            
    # hard turn zone
    for xpos in range(shape[1]):
        for ypos in range(shape[0]):
            ltest = cv2.pointPolygonTest(zlht,(ypos,xpos),False)
            rtest = cv2.pointPolygonTest(zrht,(ypos,xpos),False)
            if(ltest>=0):
                res[ypos,xpos] = -turnhigh
            elif(rtest>=0):
                res[ypos,xpos] = turnhigh

    # reverse zone
    for xpos in range(shape[1]):
        for ypos in range(shape[0]):
            lrevtest = cv2.pointPolygonTest(zrevleft, (ypos,xpos),False)
            rrevtest = cv2.pointPolygonTest(zrevright,(ypos,xpos),False)

            if(lrevtest>=0):
                res[ypos,xpos] = -brakes 
            elif(rrevtest>=0):
                res[ypos,xpos] = -brakes  *brakeratio

                
                        

    print(res.shape)
    #print(len(yascend))
  
    # ---
    return res
