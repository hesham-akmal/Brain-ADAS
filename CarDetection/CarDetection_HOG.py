#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import pandas as pd
import numpy as np
from skimage import data , io , filters #Data for images , io for imshow , filters for prewitt
import matplotlib.pyplot as plt
import colorsys
get_ipython().run_line_magic('matplotlib', 'inline')
cell_size = 8
n_angles = 18
angle_step = 20
hist_grid = None
block_grid = None
win_size = 64
#from CarDetection_SVM.py import p


# In[2]:


def display(img, isgray):
    plt.figure(dpi=150)
    if(isgray):
        plt.imshow(img, cmap='gray')
    else:
        plt.imshow(img)
    plt.show()


# In[3]:


def get_mags_and_dirs(img):
    r, c = img.shape[0], img.shape[1]
    mags = np.zeros((r, c, 3), dtype=float)
    dirs = np.zeros((r, c, 3), dtype=float)
    for i in range(3):
        comp = img[:,:,i]
        mags[:,:,i] = filters.sobel(comp)
        dirs[:,:,i] = np.arctan2(filters.sobel_h(comp), filters.sobel_v(comp))*180.0/np.pi
    return mags, dirs


# In[4]:


def get_hist_grid(sub_img):
    ri, ci = sub_img.shape[0], sub_img.shape[1] 
    #r, c = (ri-1)//cell_size+1, (ci-1)//cell_size+1
    r, c = ri-cell_size+1, ci-cell_size+1
    global hist_grid
    hist_grid = np.zeros((r, c, n_angles), dtype=float)
    for i in range(0, r, cell_size):
        for j in range(0, c, cell_size):
            cur_cell = np.zeros((cell_size, cell_size, 3), sub_img.dtype)
            #ilo, iup, jlo, jup = i*cell_size, min((i+1)*cell_size, ri), j*cell_size, min((j+1)*cell_size, ci)
            #cur_cell[:min(cell_size, iup-ilo),:min(cell_size, jup-jlo),:] = sub_img[ilo:iup,jlo:jup,:]
            ilo, iup, jlo, jup = i, i+cell_size, j, j+cell_size
            cur_cell[:cell_size,:cell_size,:] = sub_img[ilo:iup,jlo:jup,:]
            mags, dirs = get_mags_and_dirs(cur_cell)
            for k in range(cell_size):
                for l in range(cell_size):
                    max_mag, its_dir = 0, 0
                    for m in range(3):
                        if(mags[k, l, m] > max_mag):
                            max_mag, its_dir = mags[k, l, m], dirs[k, l, m]
                    if(its_dir < 0):
                        its_dir = 360 + its_dir
                    flr = int(np.floor(its_dir/angle_step))
                    lo, up = flr*angle_step, (flr+1)*angle_step
                    dl, du = its_dir-lo, up-its_dir
                    hist_grid[i, j, (lo//angle_step)%n_angles] += (1-dl/float(angle_step))*max_mag
                    hist_grid[i, j, (up//angle_step)%n_angles] += (1-du/float(angle_step))*max_mag
    #return hist_grid


# In[5]:

def Block_Normalization_Preprocess():
    hist_grid_r, hist_grid_c = hist_grid.shape[0], hist_grid.shape[1]
    R, C = hist_grid_r-cell_size, hist_grid_c-cell_size
    global block_grid
    block_grid = np.zeros((R, C, n_angles*4), dtype=float)
    for i in range(0, R, cell_size):
        for j in range(0, C, cell_size):
            #Row-major concatenation
            big_hist = list(hist_grid[i,j]) + list(hist_grid[i,j+cell_size]) + list(hist_grid[i+cell_size,j]) + list(hist_grid[i+cell_size,j+cell_size])
            
            #Squaring the values
            big_hist_sq = [h ** 2 for h in big_hist]
            
            #Adding the values
            big_hist_sum = sum(big_hist_sq)
            
            #Getting the histogram magnitude
            big_hist_mag = math.sqrt(big_hist_sum)
            
            #Normalizing the historgram
            big_hist_norm = [0.0 if big_hist_mag == 0 else m / big_hist_mag for m in big_hist]
            
            block_grid[i,j] = big_hist_norm

def Block_Normalization(si,sj):
    R,C = win_size, win_size
    giant_hist = []
    
    for i in range(si, si+R-2*cell_size+1, cell_size):
        for j in range(sj, sj+C-2*cell_size+1, cell_size):
            
            #Concatinating all the histograms
            giant_hist += list(block_grid[i,j])
            
    return giant_hist


# In[6]:


'''
img = io.imread('image0974.png')
display(img, True)
print(img.shape)
hist_grid = get_hist_grid(img, 8)
#print("element ", 11, ", ", 16, " in histogram grid: ", hist_grid[11, 16, :])
giant_hist = Block_Normalization(hist_grid)
print("length of giant histogram: ", len(giant_hist))
'''
