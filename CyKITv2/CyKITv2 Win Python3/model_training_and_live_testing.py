
# coding: utf-8

# In[9]:

#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import gc
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.metrics import classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis 
from sklearn import preprocessing
from sklearn import metrics


# In[2]:

def upload_file(fname):
    data = pd.read_csv("Our Dataset/" + fname + ".csv",  index_col=False)
    return data


# In[11]:

def make_all_columns(electrodes):
    newCols = []
    for col in electrodes:
        for i in range(192):
            newCols.append(col + '.' + str(i))
    newCols.append('y')
    return newCols


# In[5]:

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


# In[6]:

def check_if_driver_brake(start_stim, data):
    for i in range(start_stim,start_stim+192):
        if(data["Brake Pedal"][i] == 1):
            return True
    return False


# In[7]:

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


# In[22]:

def convert_to_row(start, label, electrodes, data):
    row = []
    for col in electrodes:
        row += data[col][start:start+192].tolist()
    row += [label]
    return row


# In[24]:

def upload_and_save_pos_neg(folder):
    data = upload_file(folder + "/Subject")
    data = data.drop("COUNTER", axis = 1)
    for f in fnames:
        d = upload_file(folder + "/" + f)
        d = d.drop("COUNTER", axis = 1)
        data = data.append(d, ignore_index=True)
    electrodes = data.columns.drop(["Brake Pedal", "y"])
    newCols = make_all_columns(electrodes)
    y = data["y"]
    posDfs, indices = positive_events(newCols, y, data, electrodes)
    posDfs.to_csv("Our Dataset/csv/"+folder+"pos.csv", index = False)
    negDfs = negative_events(indices, newCols, y, data, electrodes)
    negDfs.to_csv("Our Dataset/csv/"+folder+"neg.csv", index = False)


# In[3]:

def upload_pos_neg(fname):
    pos = pd.read_csv("Our Dataset/csv/" + fname + "pos" + ".csv", index_col=False)
    neg = pd.read_csv("Our Dataset/csv/" + fname + "neg" + ".csv", index_col=False)
    return pos, neg


# In[10]:

def get_drop_cols(i1):
    dropCols = []
    nums = np.arange(i1, 192)
    for i in range(14):
        name = newCols[i*192].split('.')[0]
        dropCols.append([name + '.' + str(num) for num in nums])
    return np.array(dropCols).flatten()


# In[29]:

def make_columns(numOfCols):
    nCols = []
    for i in range(14):
        name = newCols[i*192].split('.')[0]
        nCols.append(newCols[i*192:i*192+numOfCols])
    return np.array(nCols).flatten()


# In[33]:

#mean of ten discriminating time intervals

def time_intervals_features(pos, neg, interval, numOfCols):
    #cols = list(pos)
    newCols = make_columns(numOfCols)
    mean_features_pos = pd.DataFrame(columns = newCols)
    mean_features_neg = pd.DataFrame(columns = newCols)
    cols = list(pos)
    step = int((len(cols)-1)/len(newCols))
    for i in range(0, 14):
        for j in range(0, numOfCols):
            mean_features_pos[newCols[i*numOfCols + j]] = np.mean(pos[cols[i*interval+step*j:i*interval+numOfCols*j + step]], axis = 1).values
            #print( mean_features_pos[newCols[i*numOfCols + j]])
            mean_features_neg[newCols[i*numOfCols + j]] = np.mean(neg[cols[i*interval+step*j:i*interval+numOfCols*j + step]], axis = 1).values
            #print(mean_features_neg[newCols[i*numOfCols + j]])
    return mean_features_pos, mean_features_neg
    


# In[27]:

def train_for_live_test(f):
    LDAClassifier = LinearDiscriminantAnalysis()
    pos, neg = upload_pos_neg(f)
    dropCols = get_drop_cols(12*6)
    pos = pos.drop(dropCols, axis = 1)
    neg = neg.drop(dropCols, axis = 1)
    mean_features_pos, mean_features_neg = time_intervals_features(pos, neg, 12*6, 36)
    mean_features_pos['y'] = 1
    mean_features_neg['y'] = 0
    all_data = mean_features_pos.append(mean_features_neg)
    y = all_data['y']
    X = all_data.drop(['y'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1000)
    X_train = np.nan_to_num(X_train)
    X_test = np.nan_to_num(X_test)
    LDAClassifier.fit(X_train, y_train)
    y_predict = LDAClassifier.predict(X_test)
    print(str(500) + "ms")
    print(classification_report(y_test, y_predict))
    fpr, tpr, thresholds = metrics.roc_curve(y_test, y_predict)
    acc_auc = metrics.auc(fpr, tpr)
    print("AUC: " + str(acc_auc))
    print("-----------------------")
    return LDAClassifier


# In[35]:

#mean of columns
def time_intervals_features_test(packets, interval, numOfCols):
    #cols = list(pos)
    newCols = make_columns(numOfCols)
    mean_features_packets = pd.DataFrame(columns = newCols)
    cols = list(packets)
    step = int((len(cols)-1)/len(newCols))
    for i in range(0, 14):
        for j in range(0, numOfCols):
            mean_features_packets[newCols[i*numOfCols + j]] = np.mean(pos[cols[i*interval+step*j:i*interval+numOfCols*j + step]], axis = 1).values
    return mean_features_packets
    
def live_test(packets):
    dropCols = get_drop_cols(12*6)
    packets = packets.drop(dropCols, axis = 1)
    mean_features_packets = time_intervals_features_test(packets, interval=72, numOfCols=36)
    mean_features_packets = np.nan_to_num(mean_features_packets)
    y_predict = model.predict(mean_features_packets)
    return y_predict

# In[16]:

electrodes = ['F3', ' FC5', ' AF3', ' F7', ' T7', ' P7', ' O1', ' O2', ' P8', ' T8',
       ' F8', ' AF4', ' FC6', ' F4']


# In[17]:

newCols = make_all_columns(electrodes)


# In[18]:

#fnames = ["Subject_1"]
#befor calling upload_and_save_pos_neg, you should put all the file names in fnames except Subject file
#you should put the files the files in a folder called "Our Dataset" in EEG work directory


# In[25]:

#upload_and_save_pos_neg("Wagih2")





