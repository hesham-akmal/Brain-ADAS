#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import pandas as pd
import numpy as np
from skimage import data , io , filters #Data for images , io for imshow , filters for prewitt
import matplotlib as mpl
import matplotlib.pyplot as plt
import colorsys
import cv2
get_ipython().run_line_magic('matplotlib', 'inline')
cell_size = 8
n_block = 1
win_size = 64
hists_per_dim =(win_size-cell_size*n_block)//cell_size+1
n_angles = 18
angle_step = 20
hist_grid = None
block_grid = None
grad_mag_grid = None
grad_dir_grid = None
max_angle = 360
n_block_vals = n_block*n_block*n_angles
n_win_blocks = hists_per_dim*hists_per_dim
n_win_vals = n_win_blocks * n_block_vals

#from CarDetection_SVM.py import p


# In[2]:


def display(img, isgray):
    plt.figure(dpi=150)
    if(isgray):
        plt.imshow(img, cmap='gray')
    else:
        plt.imshow(img)
    plt.show()

def readimg(name):
    img = io.imread(name)
    return cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
    

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

def preprocess_grad_grids(img):
    r, c = img.shape[0], img.shape[1]
    global grad_mag_grid, grad_dir_grid
    grad_mag_grid, grad_dir_grid = get_mags_and_dirs(img)

def get_hist_grid(sub_img):
    ri, ci = sub_img.shape[0], sub_img.shape[1] 
    #r, c = (ri-1)//cell_size+1, (ci-1)//cell_size+1
    r, c = ri//cell_size, ci//cell_size
    global hist_grid
    hist_grid = np.zeros((r, c, 3, n_angles), dtype=float)
    preprocess_grad_grids(sub_img)
    for i in range(0, ri-cell_size+1, cell_size):
        for j in range(0, ci-cell_size+1, cell_size):
            for k in range(cell_size):
                for l in range(cell_size):
                    for m in range(3):
                        max_mag, its_dir = grad_mag_grid[i+k,j+l, m], grad_dir_grid[i+k,j+l, m]
                        flr = int(np.floor(its_dir/angle_step))
                        lo, up = flr*angle_step, (flr+1)*angle_step
                        dl, du = its_dir-lo, up-its_dir
                        hist_grid[i//cell_size, j//cell_size, m, (lo//angle_step)%n_angles] += (1-dl/float(angle_step))*max_mag
                        hist_grid[i//cell_size, j//cell_size, m, (up//angle_step)%n_angles] += (1-du/float(angle_step))*max_mag


# In[5]:

def Block_Normalization_Preprocess():
    hist_grid_r, hist_grid_c = hist_grid.shape[0], hist_grid.shape[1]
    R, C = hist_grid_r-n_block+1, hist_grid_c-n_block+1
    global block_grid
    block_grid = np.zeros((R, C, 3, n_angles*n_block*n_block), dtype=float)
    for i in range(0, R, 1):
        for j in range(0, C, 1):
            for k in range(3):
                #Row-major concatenation
                #big_hist = list(hist_grid[i:i+n_block,j:j+n_block].reshape((n_block_vals)))
                big_hist = hist_grid[i:i+n_block,j:j+n_block,k].reshape((n_block_vals))

                #Squaring the values
                big_hist_sq = [h ** 2 for h in big_hist]

                #Adding the values
                big_hist_sum = sum(big_hist_sq)

                #Getting the histogram magnitude
                big_hist_mag = math.sqrt(big_hist_sum)

                #Normalizing the historgram
                big_hist_norm = [0.0 if big_hist_mag == 0 else m / big_hist_mag for m in big_hist]

                block_grid[i,j,k] = big_hist_norm

def Block_Normalization(si,sj):
    R,C = win_size, win_size
    giant_hist = []
    
    si = si//cell_size
    sj = sj//cell_size
    
    #Concatinating all the histograms
    #giant_hist = list(block_grid[si:si+hists_per_dim,sj:sj+hists_per_dim].reshape(n_win_vals))
    giant_hist = block_grid[si:si+hists_per_dim,sj:sj+hists_per_dim,:].reshape(n_win_vals*3)
            
            
            
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
