import numpy as np
import cv2
import glob
import os
from skimage import io, data
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import utilities
	
	
def getnormal(line, isp):
    if(isp):
        x1, y1, x2, y2=line
        dx, dy = x2-x1, y2-y1
        norm = np.sqrt(dx**2+dy**2)
        return -dy/norm, dx/norm

    rho, theta = line
    return np.cos(theta), np.sin(theta)


def calculate_vanishing_point(lines, ud_img_BGR):

    ud_img = np.array(ud_img_BGR)
    
    t1 = np.zeros((2,2) , dtype=np.float)
    t2 = np.zeros((2,1) , dtype= np.float)
        
    for line in lines:
        
        a,b = getnormal(line[0], True)
        x1, y1, x2, y2 = utilities.get2pts(line[0], True)

        n = np.array([[a],[b]] , dtype=np.float)
        n_x_nt = np.matmul(n , np.transpose(n))
        p = np.array([[x1],[y1]] , dtype= np.float)
        t1 += n_x_nt
        t2 += np.matmul(n_x_nt , p)

        cv2.line(ud_img,(x1,y1),(x2,y2),(0,0,255),2)
            
            
    vp = np.matmul(np.linalg.pinv(t1),t2)
    vp = np.array(vp , dtype = np.int)
    print(vp)
    
    cv2.line(ud_img,(vp[0,0],vp[1,0]),(vp[0,0],vp[1,0]),(255,0,0),20)
            
    utilities.show_images([cv2.cvtColor(ud_img, cv2.COLOR_BGR2RGB)])
	
    return vp