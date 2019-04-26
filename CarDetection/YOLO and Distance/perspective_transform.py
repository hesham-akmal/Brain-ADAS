import numpy as np
import cv2
import glob
import os
from skimage import io, data
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import Utilities
import lane_detection


def find_x(p1, p2, y):
    y1, y2, x1, x2 = p1[1], p2[1], p1[0], p2[0]
    return (y-y1) * ((x2-x1) / (y2-y1)) + x1

	
def display_trapezoid(img_orig, p1, p2, p3, p4, vp):
    img = np.array(img_orig)
    
    cv2.line(img,(p1[0],p1[1]),(p3[0],p3[1]),(255,0,0), 5)
    cv2.line(img,(p2[0],p2[1]),(p4[0],p4[1]),(255,0,0), 5)
    cv2.line(img,(p2[0],p2[1]),(p1[0],p1[1]),(255,0,0), 5)
    cv2.line(img,(p3[0],p3[1]),(p4[0],p4[1]),(255,0,0), 5)
    cv2.line(img,(vp[0,0],vp[1,0]),(vp[0,0],vp[1,0]),(255,0,0),20)
    
    Utilities.show_images([cv2.cvtColor(img, cv2.COLOR_BGR2RGB)])
	

def perspective_transform(vp, img, debug):
    #vp = calculate_vanishing_point(img)
    width, height = img.shape[1], img.shape[0]
    rem_width, rem_height = min(vp[0, 0], width-vp[0, 0]), height - vp[1, 0]
    x_off, y_off =  int(0.5*rem_width), int(0.15*rem_height)
    y_base = vp[1, 0] + int(0.6*rem_height)
	#y_base = img.shape[0]-100
    #x_off, y_off =  200, 30
    p1, p2 = [vp[0,0]-x_off, vp[1, 0]+y_off], [vp[0,0]+x_off, vp[1, 0]+y_off]
    p3, p4 = [find_x(p1, [vp[0, 0], vp[1, 0]], y_base), y_base], [find_x(p2, [vp[0, 0], vp[1, 0]], y_base), y_base]
		
    if(debug):        
        ps = [p1, p2, p3, p4]
        for p in ps:
            p[0], p[1] = int(p[0]), int(p[1])
        display_trapezoid(img, p1, p2, p3, p4, vp)
            
    map_size = (300, 600)
    src = np.float32([p1, p2, p3, p4])
    dst = np.float32([[0,0], [map_size[0]-1, 0], [0, map_size[1]-1], [map_size[0]-1, map_size[1]-1]])
    H, H_inv = cv2.getPerspectiveTransform(src, dst), cv2.getPerspectiveTransform(dst, src)
    warped = cv2.warpPerspective(img, H, map_size)
    
    if(debug):
    	# warped image
        Utilities.show_images([cv2.cvtColor(warped, cv2.COLOR_BGR2RGB)])
    
    return H, H_inv, warped
	
	
def get_mapped_pxl(pxl, H):
    return cv2.perspectiveTransform(np.float32([[pxl]]), H)[0][0]
	
	
def get_ratio(H, H_inv, orig_warped, mtx, debug):
    meter_to_feet = 1/3.28084
    low_thresh = 50
    high_thresh = 100
	
    if(debug):
        warped = np.array(orig_warped)
    
    #gray = cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)
    #gray = cv2.GaussianBlur(gray,(9, 9),0)
    #edges = cv2.Canny(gray,low_thresh,high_thresh,apertureSize = 3)
    #Utilities.show_images([edges])
    #lines = cv2.HoughLines(edges,1,np.pi/180,100)
    detector = lane_detection.LaneDetector()
    lines = detector.process(cv2.cvtColor(orig_warped,cv2.COLOR_BGR2RGB), False, 0.02, debug)
    '''lines = cv2.HoughLinesP(
        edges,
        rho=2,
        theta=np.pi / 180,
        threshold=50,
        lines=np.array([]),
        minLineLength=40,
        maxLineGap=120
    )'''
    
    x_min = 1000000
    x_max = 0
	
    tot_xlft, cnt_xlft = 0, 0
    tot_xrit, cnt_xrit = 0, 0 
    
    for line in lines:
        x1, y1, x2, y2 = Utilities.get2pts(line[0], True)

        '''if(x1 < x_min):
            x_min = x1
        if(x1 > x_max):
            x_max = x1'''

        if(min(x1, x2) < 0.5*orig_warped.shape[1]):
            tot_xlft += float(x1+x2) / 2
            cnt_xlft += 1
        else:
            tot_xrit += float(x1+x2) / 2
            cnt_xrit += 1
			
        if(debug):
            cv2.line(warped,(x1,y1),(x2,y2),(0,0,255),2)
    
    warped_height = orig_warped.shape[0]
    '''left_low, left_high, right_low, right_high = get_mapped_pxl([x_min, warped_height-1], H_inv),\
    get_mapped_pxl([x_min, 0], H_inv), get_mapped_pxl([x_max, warped_height-1], H_inv),\
    get_mapped_pxl([x_max, 0], H_inv)'''
    
    avg_xlft, avg_xrit = int(float(tot_xlft) / cnt_xlft), int(float(tot_xrit) / cnt_xrit)
	
    left_low, left_high, right_low, right_high = get_mapped_pxl([avg_xlft, warped_height-1], H_inv),\
    get_mapped_pxl([avg_xlft, 0], H_inv), get_mapped_pxl([avg_xrit, warped_height-1], H_inv),\
    get_mapped_pxl([avg_xrit, 0], H_inv)
	
    if(debug):
    	# lanes on warped
        Utilities.show_images([cv2.cvtColor(warped, cv2.COLOR_BGR2RGB)])
    
    approx_dist = avg_xrit - avg_xlft
    x_pixels_per_meter = approx_dist / (12 * meter_to_feet)
    
    inv_H_x_mtx = np.linalg.inv(np.matmul(H , mtx))
    x_norm = np.linalg.norm(inv_H_x_mtx[:,0])
    y_norm = np.linalg.norm(inv_H_x_mtx[:,1])
    scale = x_norm / y_norm
    y_pixels_per_meter = x_pixels_per_meter * scale
    
    if(debug):
        print("pxls/mtr: "+str(x_pixels_per_meter)+","+str(y_pixels_per_meter))
	
    return x_pixels_per_meter , y_pixels_per_meter, left_low, left_high, right_low, right_high
	
	
def get_distance(pxl1, pxl2, H, x_ratio, y_ratio):
    mapped_pxl1 = cv2.perspectiveTransform(np.float32([[pxl1]]), H)[0][0]
    mapped_pxl2 = cv2.perspectiveTransform(np.float32([[pxl2]]), H)[0][0]
    x_pxl_dis, y_pxl_dis = mapped_pxl1[0]-mapped_pxl2[0], mapped_pxl1[1]-mapped_pxl2[1]
    #print('pxl: '+str(y_pxl_dis))
    x_mtr_dis, y_mtr_dis = x_pxl_dis/x_ratio, y_pxl_dis/y_ratio
    #return np.sqrt(x_mtr_dis**2 + y_mtr_dis**2)
    return np.abs(y_mtr_dis)