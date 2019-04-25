import matplotlib.pyplot as plt
import cv2
import os, glob
import numpy as np
from moviepy.editor import VideoFileClip
from collections import deque
import utilities

#%matplotlib inline


# convert image to hls color space
def convert_hls(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
	
# convert image to hls color space
def convert_hsv(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

# choose the lowest lightness value of the lightest pixels that form lightest_percent% of the image
def get_white_threshold(image, lightest_percent):
    hist = cv2.calcHist([image], [1], None, [256], [0, 256])
    total = np.float64(image.shape[0])*image.shape[1]
    current = 0
    for i in range(255, -1, -1):
        current += hist[i,0]
        if(current / total >= lightest_percent):
            return i
	
# select only white and yellow parts of image, discarding yello color for now
def select_white_yellow(image, lightest_percent, debug):
    converted = convert_hls(image)
    #converted = convert_hsv(image)
    #show_images([converted])
    # white color mask
    lower = np.uint8([  0, get_white_threshold(converted, lightest_percent),   0])
    upper = np.uint8([255, 255, 255])
    #sensitivity = 164
    #lower = np.array([0,0,255-sensitivity])
    #upper = np.array([255,sensitivity,255])
    white_mask = cv2.inRange(converted, lower, upper)
    # yellow color mask
    #lower = np.uint8([ 10,   0, 100])
    #upper = np.uint8([ 40, 255, 255])
    #yellow_mask = cv2.inRange(converted, lower, upper)
    # combine the mask
    #mask = cv2.bitwise_or(white_mask, yellow_mask)
    mask = white_mask
    ret = cv2.bitwise_and(image, image, mask = mask)

    if(debug):
        print('after white color selection')
        utilities.show_images([ret])
    
    return ret
	
	
# convert image to grayscale
def convert_gray_scale(image, debug):
    ret = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    if(debug):
        print('after converting to grayscale')
        utilities.show_images([ret])
    
    return ret
	

# apply gaussian blurring over the image
def apply_smoothing(image, debug, kernel_size=15):
    """
    kernel_size must be postivie and odd
    """
    ret = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    if(debug):
        print('after smoothing')
        utilities.show_images([ret])
    
    return ret
	

# produce edges image
def detect_edges(image, debug, low_threshold=50, high_threshold=80):
    ret = cv2.Canny(image, low_threshold, high_threshold)
    
    if(debug):
        print('after edge detection')
        utilities.show_images([ret])
	
    return ret
	

def filter_region(image, vertices):
    """
    Create the mask using the vertices and apply it to the input image
    """
    mask = np.zeros_like(image)
    if len(mask.shape)==2:
        cv2.fillPoly(mask, vertices, 255)
    else:
        cv2.fillPoly(mask, vertices, (255,)*mask.shape[2]) # in case, the input image has a channel dimension        
    return cv2.bitwise_and(image, mask)
	
	
# select region of interest based on predetermined ratios of the image dimensions
def select_region(image, debug):
    """
    It keeps the region surrounded by the `vertices` (i.e. polygon).  Other area is set to 0 (black).
    """
    # first, define the polygon by vertices
    # cols, rows where: 0.1, 0.4, 0.9, 0.6 | 0.95, 0.6, 0.95, 0.6
    rows, cols = image.shape[:2]
    bottom_left  = [cols*0.0, rows*0.9]
    top_left     = [cols*0.0, rows*0.55]
    bottom_right = [cols*1.0, rows*0.9]
    top_right    = [cols*1.0, rows*0.55] 
    # the vertices are an array of polygons (i.e array of arrays) and the data type must be integer
    vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    ret = filter_region(image, vertices)
    
    if(debug):
        print('after ROI')
        utilities.show_images([ret])
    
    return ret

	
# apply hough transform over the image
def hough_lines(image):
    """
    `image` should be the output of a Canny transform.
    
    Returns hough lines (not the image with lines)
    """
    return cv2.HoughLinesP(image, rho=1, theta=np.pi/180, threshold=20, minLineLength=10, maxLineGap=5)
	
	

QUEUE_LENGTH=50

class LaneDetector:
    def __init__(self):
        self.left_lines  = deque(maxlen=QUEUE_LENGTH)
        self.right_lines = deque(maxlen=QUEUE_LENGTH)

    def process(self, image, ROI, lightest_percent, debug):
        white_yellow = select_white_yellow(image, lightest_percent, debug)
        gray         = convert_gray_scale(white_yellow, debug)
        smooth_gray  = apply_smoothing(gray, debug)
        edges        = detect_edges(smooth_gray, debug)
        #edges        = detect_edges(gray)
        if(ROI):
            regions  = select_region(edges, debug)
        else:
            regions  = edges
        lines 		 = hough_lines(regions)
        return lines
