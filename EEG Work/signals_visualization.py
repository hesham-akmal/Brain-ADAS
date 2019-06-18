

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import gc
from sklearn import preprocessing
import plotly 
from plotly.offline import *

def upload_file(fname):
    data = pd.read_csv("Our Dataset/" + fname,  index_col=False)
    return data

def make_columns_drawing(electrodes):
    newCols = []
    for col in electrodes:
        for i in range(192):
            newCols.append(col + '.' + str(i))
    newCols.append('y')
    return newCols

def convert_to_row(start, label, electrodes, data):
    row = []
    for col in electrodes:
        row += data[col][start:start+192].tolist()
    row += [label]
    return row

def positive_events(newCols, y, data, electrodes):
    posDfs = pd.DataFrame(columns = newCols)
    indices = []
    j = 0
    while j < (len(y)):
        #assume positive events are: pedestrian, dog, collision, and leadning car brake
        if (y[j] != 0):
            if (j+192 < len(y) and check_if_driver_brake(j, data)):
                posDfs.loc[len(posDfs)] = convert_to_row(j, 1, electrodes, data)
                indices.append(j)
                j += 384 #192*2
            else:
                j+=1
        else:
            j += 1
    return posDfs, indices  

def check_if_driver_brake(start_stim, data):
    for i in range(start_stim,start_stim+192):
        if(data[data.columns[0]][i] == 1):
            return True
    return False

def negative_events(indices, newCols, y, data, electrodes):
    negDfs = pd.DataFrame(columns = newCols)
    j = 0
    while j < (len(y)):
        if(len(indices) > 0 and j <= indices[0] and j+192 > indices[0]):
            j = indices[0] + 384
            indices.pop(0)
        elif(j+192 < len(y)):
            negDfs.loc[len(negDfs)] = convert_to_row(j, 0, electrodes, data)
            j += 192
        else:
            break
    return negDfs

def upload_and_draw(folder, preprocess, apply_filter, fc):
    fnames = os.listdir("Our Dataset/"+folder)
    data = upload_file(folder + '/'+fnames[0])
    data = data.drop("COUNTER", axis = 1)
    for i in range(1,len(fnames)):
        d = upload_file(folder + "/" + fnames[i])
        d = d.drop("COUNTER", axis = 1)
        data = data.append(d, ignore_index=True)
        print(fnames[i])
    brake_col = data.columns[0]
    electrodes = data.columns.drop([data.columns[0], "y"])
    newCols = make_columns_drawing(electrodes)
    y = data["y"]
    posDfs, indices = positive_events(newCols, y, data, electrodes)
    posDfs.to_csv("Our Dataset/csv/"+folder+"pos.csv", index = False)
    negDfs = negative_events(indices, newCols, y, data, electrodes)
    negDfs.to_csv("Our Dataset/csv/"+folder+"neg.csv", index = False)
    #return posDfs, negDfs
    if(apply_filter):
        draw_signals_low_pass(folder, posDfs, negDfs, fc, preprocess)
    else:
        draw_signals(folder, posDfs, negDfs, preprocess)



def draw_signals(subject, posDfs, negDfs, preprocess):
    if(preprocess):
        meanPos = preprocessing.scale(np.mean(posDfs.drop("y", axis = 1)))
        meanNeg = preprocessing.scale(np.mean(negDfs.drop("y", axis = 1)))
    else:
        meanPos = np.mean(posDfs.drop("y", axis = 1)).values
        meanNeg = np.mean(negDfs.drop("y", axis = 1)).values
    cols = list(posDfs)
    for i in range(14):
        name = cols[i*192].split('.')[0]
        plt.ylim(np.amin(meanPos[i*192:i*192+192])-10, np.max(meanPos[i*192:i*192+192])+10)
        plt.title(subject + ": " + name, fontsize=16, fontweight='bold')
        plt.plot(meanPos[i*192:i*192+192], label="Braking Event")
        plt.plot(meanNeg[i*192:i*192+192], label="Normal Driving")
        plt.legend()
        plt.show()
        
def mean_zero(array):
    for i in range(14):
        mean = np.mean(array[i*192:i*192+192])
        for j in range(192):
            array[i*192+j] -= mean
        
def apply_filter(pos_interval, neg_interval, fc):
    b = 0.08
    N = int(np.ceil((4 / b)))
    if not N % 2: N += 1
    n = np.arange(N)

    sinc_func = np.sinc(2 * fc * (n - (N - 1) / 2.))
    window = 0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
    sinc_func = sinc_func * window
    sinc_func = sinc_func / np.sum(sinc_func)

    s = list(pos_interval)
    new_signal_pos = np.convolve(s, sinc_func)
    s = list(neg_interval)
    new_signal_neg = np.convolve(s, sinc_func)
    return new_signal_pos, new_signal_neg
        

def draw_signals_low_pass(subject, posDfs, negDfs, fc, preprocess):
    #plotly.tools.set_credentials_file(username='fatema4', api_key='cKM0lg5CtfIveNnvRSfH')
    #plotly.tools.set_config_file(world_readable=True, sharing='public')
    if(preprocess):
        meanPos = preprocessing.scale(np.mean(posDfs.drop("y", axis = 1)))
        meanNeg = preprocessing.scale(np.mean(negDfs.drop("y", axis = 1)))
    else:
        meanPos = np.mean(posDfs.drop("y", axis = 1)).values
        meanNeg = np.mean(negDfs.drop("y", axis = 1)).values
        print(posDfs.columns)
    mean_zero(meanPos)
    mean_zero(meanNeg)
    cols = list(posDfs)
    for i in range(14):
        name = cols[i*192].split('.')[0]
        title = subject + ": " + name
        new_signal_pos, new_signal_neg = apply_filter(meanPos[i*192:i*192+192], meanNeg[i*192:i*192+192], fc)
        plt.title(subject + ": " + name, fontsize=16, fontweight='bold')
        out_bound = int((new_signal_pos.shape[0] - 192)/2)
        plt.plot(new_signal_pos[out_bound:new_signal_pos.shape[0]-out_bound], label="Braking Event")
        plt.plot(new_signal_neg[out_bound:new_signal_pos.shape[0]-out_bound], label="Normal Driving")
        plt.axis('tight')
        plt.legend()
        plt.show()
        #print("should be drawn")