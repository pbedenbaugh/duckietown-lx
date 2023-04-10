import cv2
import numpy as np

#lower_hsv = np.array([171, 140, 100])
#upper_hsv = np.array([179, 200, 255])
#lower_hsv = np.array([2, 0, 80])
#upper_hsv = np.array([60, 255, 255])

lower_hsv = np.array([0, 60, 0])
upper_hsv = np.array([120, 255, 255])

def preprocess(image_rgb: np.ndarray) -> np.ndarray:
    """Returns a 2D array"""
    hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    return mask
