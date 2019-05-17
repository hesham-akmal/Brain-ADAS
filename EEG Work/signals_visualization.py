

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import gc
from sklearn import preprocessing


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
        if(data["Brake Pedal "][i] == 1):
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

def upload_and_draw(folder, preprocess):
    fnames = os.listdir("Our Dataset/"+folder)
    data = upload_file(folder + '/'+fnames[0])
    data = data.drop("COUNTER", axis = 1)
    for i in range(1,len(fnames)):
        d = upload_file(folder + "/" + fnames[i])
        d = d.drop("COUNTER", axis = 1)
        data = data.append(d, ignore_index=True)
        print(fnames[i])
    electrodes = data.columns.drop(["Brake Pedal ", "y"])
    newCols = make_columns_drawing(electrodes)
    y = data["y"]
    posDfs, indices = positive_events(newCols, y, data, electrodes)
    posDfs.to_csv("Our Dataset/csv/"+folder+"pos.csv", index = False)
    negDfs = negative_events(indices, newCols, y, data, electrodes)
    negDfs.to_csv("Our Dataset/csv/"+folder+"neg.csv", index = False)
    draw_signals(folder, posDfs, negDfs, preprocess)

#run this block if you want to draw without preprocessing


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
