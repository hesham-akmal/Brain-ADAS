# Yolo imports
from __future__ import division
import torch 
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import cv2 
import time
import argparse
import os 
import os.path as osp
import pickle as pkl
import pandas as pd
import random
from skimage import io
#from matplotlib import pyplot as plt
from ConfidenceThresholdingAndNonMaximumSuppression import *
from NeuralNetwork import *
from Utilities import *

#########################################################################################################################

# Lane detection and distance estimation imports
import glob
from skimage import io, data
import matplotlib.image as mpimg
import camera_calibration
import lane_detection
import vanishing_point
#import utilities
import perspective_transform

import warnings
warnings.filterwarnings("ignore") #Not recommended

# YOLO code to be run only once ########################################################################################

#Driver values

images = 'imgs/'
batch_size = 1
confidence = 0.5
nms_thesh = 0.4
start = 0
weights_file = 'yolov3.weights'
cfg_file = 'cfg/yolov3.cfg'

#Change cfg file and save
def SetYoloReso(reso):
    with open(cfg_file, "r+") as f:
        lines = f.readlines()
        del lines[3]
        del lines[3]
        lines.insert(3, 'height = ' + str(reso) + '\n') 
        lines.insert(3, 'width = ' + str(reso) + '\n') 
        f.seek(0)
        f.truncate()
        f.writelines(lines)
        
reso = 32*7
SetYoloReso(reso)
det = 'det/'
CUDA = torch.cuda.is_available()

num_classes = 80    #For COCO
classes = load_classes("data/coco.names")

######

#Set up the neural network
print("Loading network.....")
model = Darknet(cfg_file)
model.load_weights(weights_file)
print("Yolo Network successfully loaded")
print("DriverBADAS loading")

model.net_info["height"] = reso
inp_dim = int(model.net_info["height"])
assert inp_dim % 32 == 0 
assert inp_dim > 32

#If there's a GPU availible, put the model on GPU
if CUDA:
    model.cuda()

#Set the model in evaluation mode
model.eval()

#########################################################################################################################

# Lane detection and distance estimation code to be run only once

ret, mtx, dist, rvecs, tvecs = camera_calibration.calibrate(False)

#########################################################################################################################

# YOLO prediction function
# Takes BGR image and returns: 1) image annotated with bounding boxes, 2) list of top left and bottom right
# coordinates of bounding boxes, 3) list of class numbers which correspond to class labels

def get_pred(img):
    read_dir = time.time()
    #Detection phase
    imlist = ['img']

    if not os.path.exists(det):
        os.makedirs(det)

    load_batch = time.time()
    loaded_ims = [np.array(img)]
#     loaded_ims = [cv2.undistort(np.array(img), mtx, dist, None, mtx)]
    
    #PyTorch Variables for images
    im_batches = list(map(prep_image, loaded_ims, [inp_dim for x in range(len(imlist))]))

    #List containing dimensions of original images
    im_dim_list = [(x.shape[1], x.shape[0]) for x in loaded_ims]
    im_dim_list = torch.FloatTensor(im_dim_list).repeat(1,2)

    if CUDA:
        im_dim_list = im_dim_list.cuda()

    leftover = 0
    if (len(im_dim_list) % batch_size):
        leftover = 1

    if batch_size != 1:
        num_batches = len(imlist) // batch_size + leftover            
        im_batches = [torch.cat((im_batches[i*batch_size : min((i +  1)*batch_size, len(im_batches))]))  for i in range(num_batches)]  

    write = 0
    start_det_loop = time.time()
    
    for i, batch in enumerate(im_batches):
        #load the image 
        start = time.time()
        t = time.time()  
        if CUDA:
            batch = batch.cuda()
        with torch.no_grad():
            prediction = model(Variable(batch), CUDA)
#         print("prediction: " , time.time()-t)    
        t = time.time()    
        prediction = write_results(prediction, confidence, num_classes, nms_conf = nms_thesh)
        end = time.time()

        if type(prediction) == int:

            for im_num, image in enumerate(imlist[i*batch_size: min((i +  1)*batch_size, len(imlist))]):
                im_id = i*batch_size + im_num
#                 print("{0:20s} predicted in {1:6.3f} seconds".format(image.split("/")[-1], (end - start)/batch_size))
#                 print("{0:20s} {1:s}".format("Objects Detected:", ""))
#                 print("----------------------------------------------------------")
            continue

        prediction[:,0] += i*batch_size    #transform the atribute from index in batch to index in imlist 
    
    try:
        if not write:                      #If we have't initialised output
            output = prediction  
            write = 1
        else:
            output = torch.cat((output,prediction))

        for im_num, image in enumerate(imlist[i*batch_size: min((i +  1)*batch_size, len(imlist))]):
            im_id = i*batch_size + im_num
            objs = [classes[int(x[-1])] for x in output if int(x[0]) == im_id]
#             print("{0:20s} predicted in {1:6.3f} seconds".format(image.split("/")[-1], (end - start)/batch_size))
#             print("{0:20s} {1:s}".format("Objects Detected:", " ".join(objs)))
#             print("----------------------------------------------------------")

        if CUDA:
            torch.cuda.synchronize()
#         output
    except:
        #print("exception")
        return loaded_ims[0]

    im_dim_list = torch.index_select(im_dim_list, 0, output[:,0].long())

    scaling_factor = torch.min(inp_dim/im_dim_list,1)[0].view(-1,1)

    output[:,[1,3]] -= (inp_dim - scaling_factor*im_dim_list[:,0].view(-1,1))/2
    output[:,[2,4]] -= (inp_dim - scaling_factor*im_dim_list[:,1].view(-1,1))/2

    output[:,1:5] /= scaling_factor

    for i in range(output.shape[0]):
        output[i, [1,3]] = torch.clamp(output[i, [1,3]], 0.0, im_dim_list[i,0])
        output[i, [2,4]] = torch.clamp(output[i, [2,4]], 0.0, im_dim_list[i,1])

    class_load = time.time()
    colors = pkl.load(open("pallete", "rb"))

    draw = time.time()

    list(map(lambda x: write_img(x, loaded_ims, color = random.choice(colors), classes = classes), output))

    t = time.time()
    det_names = pd.Series(imlist).apply(lambda x: "{}/det_{}".format(det,x.split("/")[-1]))
    
    end = time.time()
    
#     print("SUMMARY")
###     print("----------------------------------------------------------")
###     print("{:25s}: {}".format("Task", "Time Taken (in seconds)"))
###     print()
###     print("{:25s}: {:2.3f}".format("Reading addresses", load_batch - read_dir))
###     print("{:25s}: {:2.3f}".format("Loading batch", start_det_loop - load_batch))
###     print("{:25s}: {:2.3f}".format("Drawing Boxes", end - draw))
#     print("{:25s}: {:2.3f}".format("Average time_per_img", (end - load_batch)/len(imlist)))
#     print("----------------------------------------------------------")

#     t = time.time()
#     torch.cuda.empty_cache()
#     print('= Time to torch.cuda.empty_cache : ', time.time() - t)
   
    return loaded_ims[0], output[:, 1:3], output[:, 3:5], output[:, -1]

#########################################################################################################################

# Perspective transform function.
# Takes as input: 1) BGR image, 2) debug mode, 3) YOLO annotated image
# Returns: 1) Homography matrix, 2) x pixels per meter, 3) y pixels per meter
# To be called only one time one time on a base image, its outputs are then used for any image

def driver_perspective_transform(img_BGR, debug=False):
#     ud_img_BGR = cv2.undistort(img_BGR, mtx, dist, None, mtx)
    ud_img_BGR = img_BGR
    ud_img_RGB = cv2.cvtColor(ud_img_BGR, cv2.COLOR_BGR2RGB)
    if(debug):
        show_images([ud_img_RGB])
    detector = lane_detection.LaneDetector()
    lines = detector.process(ud_img_RGB, True, 0.5, 0.16, debug)
    
    vp = vanishing_point.calculate_vanishing_point(lines, ud_img_BGR, debug)
    
    H, H_inv, warped = perspective_transform.perspective_transform(vp, ud_img_BGR, debug)
    
    x_pixels_per_meter , y_pixels_per_meter, left_low, left_high, right_low, right_high = \
                    perspective_transform.get_ratio(H, H_inv, warped, mtx, debug)

    return H, x_pixels_per_meter, y_pixels_per_meter

#########################################################################################################################

# Distance estimation function
# Takes as input: 1) Query pixel, 2) Bottom center coordinates of screen, 3) homography matrix,
# 4) x pixels per meter, 5) y pixels per meter
# Returns distance to the query pixel
def get_distance(query_pnt, center, H, x_pixels_per_meter, y_pixels_per_meter):
    return perspective_transform.get_distance(query_pnt, center, H, x_pixels_per_meter, y_pixels_per_meter)

#######################################################################################################################

# Annotates image with lanes or prints on image that lane departure is detected
# Inputs: 1) image, 2) resolution of image / 1200x500 resolution
# Outputs: 2) Annotated image

def get_lane_image(img, ratio, debug=False):
    base_left_m, base_left_c, base_right_m, base_right_c = -0.32785089597153977, 446.0614062879984*ratio,\
                                                            0.2911316010810115, 79.62376483613377*ratio
    max_m_diff, max_c_diff = 0.13, 50

    test_img = np.array(img)
    width, height = test_img.shape[1], test_img.shape[0]

    detector = lane_detection.LaneDetector()
    lines = detector.process(cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB), True, 0.4, 0.5, debug)

    left_lane_lines, right_lane_lines = lane_detection.get_lane_lines(lines, base_left_m, base_left_c, base_right_m,
                                                                      base_right_c, max_m_diff, max_c_diff)
    if(len(left_lane_lines)==0 or len(right_lane_lines)==0):
        outOfLane = True
        cv2.putText(test_img,
            "Not inside lane",
            (int(width/2-150), 50), 
            font, 
            fontScale,
            fontColor,
            lineType)
    else:
        outOfLane = False
        left_lane_line, right_lane_line = get_lines_mean(left_lane_lines), get_lines_mean(right_lane_lines)
        low_y, high_y = height-1, int(height * 0.6)
        left_low, left_high = (int((low_y-left_lane_line[1])/left_lane_line[0]), low_y),\
                              (int((high_y-left_lane_line[1])/left_lane_line[0]), high_y)
        right_low, right_high = (int((low_y-right_lane_line[1])/right_lane_line[0]), low_y),\
                              (int((high_y-right_lane_line[1])/right_lane_line[0]), high_y)
        cv2.line(test_img, tuple(left_low), tuple(left_high),(0,0,255),5)
        cv2.line(test_img, tuple(right_low), tuple(right_high),(0,0,255),5)
    
    return test_img, outOfLane

#########################################################################################################################

##Emergency braking fns
import math
import threading
import time    
# To play sounds
import winsound

#pip install pyserial
import serial
import array

last_t = time.time()
last_dist = 0
last_RV = 0
last_VDi = 0

avgd_dist = 0

def scale(val, src, dst):
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

outOfLane = False
WarningSnRunning = False
def WarningSn():
    print('WarningSn' , flush = True)
    global outOfLane
    global WarningSnRunning
    global veh_speed
    while(outOfLane):
        if(veh_speed > 5 and BADAS_fns.Braking == False):
            winsound.Beep(300, 800)
        time.sleep(0.5)
    WarningSnRunning = False

def LaneWarningControllerUpdate():
    global outOfLane
    global WarningSnRunning
    if(outOfLane and WarningSnRunning == False):
        WarningSnRunning = True
        threading.Thread(target=WarningSn).start()

History_Dists = []
def AvgLastDists(new_dist):
    global History_Dists
    History_Dists.append(new_dist)
    if(len(History_Dists) == 4 ):
        History_Dists.pop(0)
    return sum(History_Dists)/len(History_Dists)

#recent_dist
def BrakeDecide(new_dist):
    global tiva_send
    global last_RV
    global last_dist
    global last_VDi
    global last_t
    global avgd_dist
    
    avgd_dist = AvgLastDists(new_dist)
    
    time_from_last_frame = time.time() - last_t
    RV =  ( last_dist - avgd_dist ) / time_from_last_frame
    RA = -( last_RV - RV) / time_from_last_frame
    
    VDi = veh_speed
    VOi = VDi - RV

    #Only once "time_from_last_frame" occured to be zero for an unknown reason, handling it below
    if(time_from_last_frame == 0):
        return 0 #VISIONprob is zero (ignored)

    AD = (VDi - last_VDi) / time_from_last_frame
    AO = AD - RA
    
    ###Set last frame vals
    last_t = time.time()
    last_dist = avgd_dist
    last_RV = RV
    last_VDi = VDi
    
    max_decel = 20
    ds = ( VDi*VDi ) / (2*max_decel)
    ts = VDi / max_decel
    VOf = VOi + AO*ts
    if(VOf >= 0):
        do = ( VOi*ts ) + (0.5 * AO * (ts*ts))
    else:
        if(AO == 0):
            do = 1000
        else:
            do = -(VOi * VOi) / (2 * AO)

#     print('\nnew_dist = ' , new_dist )
#     print('\navgd_dist = ' , avgd_dist )
#     print('time_from_last_frame = ' , time_from_last_frame )
#     print('RV = ' , RV )
#     print('RA = ' , RA )
#     print('VDi = ' , VDi )
#     print('VOi = ' , VOi )
#     print('AD = ' , AD )
#     print('AO = ' , AO )
#     print('ds = ' , ds )
#     print('ts = ' , ts )
#     print('do = ' , do )
#     print('(avgd_dist + do) - ds = ' , (avgd_dist + do) - ds )
    
    min_safe_dist = 8
    X = (avgd_dist + do) - ds
    
    if( X <= 0 ):
        VISIONprob = 1
    elif( X >= min_safe_dist ):
        VISIONprob = 0
    else:
        VISIONprob = scale(X , [0,min_safe_dist] , [1,0])

    return VISIONprob
    
##################################################################################################################################################################

def crop_center(img,cropx,cropy):
    y,x,z = img.shape
    startx = x//2-(cropx//2)
    starty = y//2-(cropy//2)    
    return img[starty:starty+cropy,startx:startx+cropx]

# Preparing text style that will be used in writing distances
font                   = cv2.FONT_HERSHEY_SIMPLEX
pos = (0,0)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

img = cv2.imread('imgs/noshade1200x500.JPG')
H, x_pixels_per_meter, y_pixels_per_meter = driver_perspective_transform(img, False)

print("DriverBADAS successfully loaded")

drawDebug = True
printDebug = False

def EstimateDistance():
    global outOfLane

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        return 999

    prob = 0
    t3 = time.time()
    t1 = t3
    
    global veh_speed
    veh_speed = BADAS_fns.GetSuvVel()
    
    try:
        img = BADAS_fns.GetSimImg()
        if(drawDebug):
            cv2.imshow("", img)
            #show_images([cv2.cvtColor(img, cv2.COLOR_BGR2RGB)])
        if(printDebug):
            print('T Sim image extract: ' , time.time() - t1)
    except Exception as e:
        print('GetSimImg Exception ' , str(e))
        return prob
    
    # Image bottom center coordinates
    center = [img.shape[1]//2, img.shape[0]-1]
    
    try:
        t1 = time.time()
        img, outOfLane = get_lane_image(img, float(img.shape[0])/500)
        if(printDebug):
            print('T get_lane_image: ' , time.time() - t1)
            
        LaneWarningControllerUpdate()

        imgYOLO = crop_center(img,208,208)
        #imgYOLO = img

        if(drawDebug):
            cv2.imshow("", img)
            #show_images([cv2.cvtColor(img, cv2.COLOR_BGR2RGB)])
        # Getting predictions from yolo
        t1 = time.time()
        pred, top_left, bottom_right, labels = get_pred(imgYOLO)
        if(printDebug):
            print('T Yolo: ' , time.time() - t1)
        #if(drawDebug):
        #    show_images([cv2.cvtColor(pred, cv2.COLOR_BGR2RGB)])
    except Exception as e:
        return prob
    
    t1 = time.time()
    # Looping on every detected object
    for i in range(len(labels)):
        # Object label
        label = classes[int(labels[i])]

        if(label != "car"):
            continue

        # Top left x,y
        tlx, tly = int(top_left[i,0]), int(top_left[i,1])

        # Bottom right x,y
        brx, bry = int(bottom_right[i,0]), int(bottom_right[i,1])

        # Bottom center coordinates of bounding box
        cx, cy = (tlx + brx)//2, bry

        # Distance to car
        float_dist = get_distance(scale_pixel([cx, cy], img.shape), scale_pixel(center, img.shape), H, x_pixels_per_meter, y_pixels_per_meter)

        prob = BrakeDecide(float_dist)
        
        if(drawDebug):
            dtime = time.time()
            #paste yolo img on lane img
            img[0:pred.shape[0] , 146:146 + pred.shape[1]] = pred
            #img = pred
    
            distance = str(round_float(float_dist))+"m"
            if(prob>=0.5):
                cv2.putText(img, "EMERGENCY",(cx-60+146, cy-60), font, fontScale,fontColor, lineType)
           # Annotate yolo image with distance to car
            cv2.putText(img, distance, (cx-60+146, cy+30), font, fontScale, fontColor, lineType)
            if(printDebug):
                print('T Get distance: ' , time.time() - t1)
            cv2.imshow("", img)
            #show_images([cv2.cvtColor(pred, cv2.COLOR_BGR2RGB)])
            if(printDebug):
                print('T Debug Draw: ' , time.time() - dtime)
    if(printDebug):
        print('T Total: ' , time.time() - t3 , '\n')
        print('FrameEnd\n')
        
    return prob

class VisionThread(threading.Thread):

    def __init__(self, BADAS_fns_param):
        super().__init__()
        self.prob = 0
        global BADAS_fns
        BADAS_fns = BADAS_fns_param
        return

    def run(self):
        while(True):
            self.prob = EstimateDistance()
        return
    
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()