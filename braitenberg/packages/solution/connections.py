from typing import Tuple

import numpy as np


def get_motor_left_matrix(shape: Tuple[int, int]) -> np.ndarray:
    # TODO: write your function instead of this one
    res = np.zeros(shape=shape, dtype="float32")
    # these are random values
    ###res[100:150, 100:150] = 1
    ###res[300:, 200:] = 1
    # if in center lower, back up
    res[220:480,220:420] = -2
    #if on left lower, go forward
    res[220:479,0:219]=1
    #if on left upper, go forward

    res[0:219,0:219]=1
    res[0:219,220:319]=0.25
    # if far left, go forward fast
    res[0:480,0:100]=2
    # if far right, reverse
    res[0:480,540:639]=-2
    #if blank, creep forward
    res[:,:]=res[:,:]=res[:,:]+0.1
    # ---
    return res


def get_motor_right_matrix(shape: Tuple[int, int]) -> np.ndarray:
    # TODO: write your function instead of this one
    res = np.zeros(shape=shape, dtype="float32")
    # these are random values
    #res[100:150, 100:300] = -1
     # if in center lower, back up
    res[220:480,220:420] = -2
    #if on right lower, go forward
    res[220:479,421:639]=1
    #if on right upper, go forward
    res[0:219,421:639]=1
    res[0:219,320:420]=0.25
    # if far right, go forward fast
    res[0:480,540:639]=2

    # if far left, go reverse
    res[0:480,0:100]=-2
    #if blank, creep forward
    res[:,:]=res[:,:]=res[:,:]+0.1

    # ---
    return res
