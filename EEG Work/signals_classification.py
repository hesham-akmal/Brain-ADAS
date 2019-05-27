
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis 
from sklearn import preprocessing
from sklearn import metrics
from signals_visualization import make_columns_drawing
import numpy as np
import pandas as pd

def upload_pos_neg(fname):
    pos = pd.read_csv("Our Dataset/csv/" + fname + "pos" + ".csv", index_col=False)
    neg = pd.read_csv("Our Dataset/csv/" + fname + "neg" + ".csv", index_col=False)
    return pos, neg

def select_electrodes(electrodes, pos, neg):
    all_electrodes = pos.columns
    for i in range(0, 192*14, 192):
        electrode = all_electrodes[i].split('.')[0]
        if  electrode not in electrodes:
            pos = pos.drop([(electrode+'.'+str(j)) for j in range(192)], axis = 1)
            neg = neg.drop([(electrode+'.'+str(j)) for j in range(192)], axis = 1)
    return pos, neg

#put here your selected electrodes


all_electrodes = ['F3', ' FC5', ' AF3', ' F7', ' T7', ' P7', ' O1', ' O2', ' P8', ' T8',
       ' F8', ' AF4', ' FC6', ' F4']



def make_columns(numOfCols, electrodes_len, cols):
    newCols = []
    for i in range(electrodes_len):
        name = cols[i*192].split('.')[0]
        newCols.append(cols[i*192:i*192+numOfCols])
    return np.array(newCols).flatten()

def time_intervals_features(pos, neg, interval, numOfCols, electrodes_len, cols):
    #cols = list(pos)
    newCols = make_columns(numOfCols, electrodes_len, cols)
    mean_features_pos = pd.DataFrame(columns = newCols)
    mean_features_neg = pd.DataFrame(columns = newCols)
    cols = list(pos)
    step = int((len(cols)-1)/len(newCols))
    for i in range(0, electrodes_len):
        for j in range(0, numOfCols):
            mean_features_pos[newCols[i*numOfCols + j]] = np.mean(pos[cols[i*interval+step*j:i*interval+numOfCols*j + step]], axis = 1).values
            mean_features_neg[newCols[i*numOfCols + j]] = np.mean(neg[cols[i*interval+step*j:i*interval+numOfCols*j + step]], axis = 1).values
            #print(mean_features_neg[newCols[i*numOfCols + j]])
    return mean_features_pos, mean_features_neg

def get_drop_cols(i1, electrodes_len, newCols):
    dropCols = []
    nums = np.arange(i1, 192)
    for i in range(electrodes_len):
        name = newCols[i*192].split('.')[0]
        dropCols.append([name + '.' + str(num) for num in nums])
    return np.array(dropCols).flatten()

def apply_filter(pos, neg):
    fc = 0.02
    b = 0.08
    N = int(np.ceil((4 / b)))
    if not N % 2: N += 1
    n = np.arange(N)

    sinc_func = np.sinc(2 * fc * (n - (N - 1) / 2.))
    window = 0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
    sinc_func = sinc_func * window
    sinc_func = sinc_func / np.sum(sinc_func)
    
    filter_pos = np.zeros(pos.shape)
    filter_neg = np.zeros(neg.shape)
    
    for i in range(len(pos)):
        for j in range(14):
            s = list(pos.iloc[i][j*192:j*192+192])
            filter_pos[i][j*192:j*192+192] = np.convolve(s, sinc_func)[:192]
            
    for i in range(len(neg)):
        for j in range(14):
            s = list(neg.iloc[i][j*192:j*192+192])
            filter_neg[i][j*192:j*192+192] = np.convolve(s, sinc_func)[:192]
            
    filter_pos =  pd.DataFrame(data=filter_pos, columns=pos.columns)
    filter_neg =  pd.DataFrame(data=filter_neg, columns=neg.columns) 
            
    return filter_pos, filter_neg

def train_test_split_data(pos, neg, test_size):
    pos_size_test = int(len(pos)*test_size)
    neg_size_test = int(len(neg)*test_size)
    all_test = pos[:pos_size_test].append(neg[:neg_size_test])
    all_test.sample(frac=1)
    y_test = all_test['y']
    X_test = all_test.drop(['y'], axis = 1)
    all_train = pos[pos_size_test:].append(neg[neg_size_test:])
    all_train.sample(frac=1)
    y_train = all_train['y']
    X_train = all_train.drop(['y'], axis = 1)
    return X_train, X_test, y_train, y_test

def classify_diff_intervals(fnames, electrodes, filter_apply):
    LDAClassifier = LinearDiscriminantAnalysis()
    cols = make_columns_drawing(electrodes)
    newCols = make_columns_drawing(electrodes)
    electrodes_len = len(electrodes)
    fi = 0
    for f in fnames:
        print(f)
        for i in np.arange(12, 180, 12):
            pos, neg = upload_pos_neg(f)
            if(filter_apply):
                pos, neg = apply_filter(pos, neg)
            pos, neg = select_electrodes(electrodes, pos, neg)
            dropCols = get_drop_cols(i, electrodes_len, newCols)
            #print(dropCols)
            pos = pos.drop(dropCols, axis = 1)
            neg = neg.drop(dropCols, axis = 1)
            mean_features_pos, mean_features_neg = time_intervals_features(pos, neg, i, int(i*6/12), electrodes_len, cols)
            mean_features_pos['y'] = 1
            mean_features_neg['y'] = 0
            #all_data = mean_features_pos.append(mean_features_neg)
            #y = all_data['y']
            #X = all_data.drop(['y'], axis=1)
            #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1000)
            X_train, X_test, y_train, y_test = train_test_split_data(mean_features_pos, mean_features_neg, test_size=0.3)
            X_train = np.nan_to_num(X_train)
            X_test = np.nan_to_num(X_test)
            #X_train = preprocessing.scale(X_train)
            #X_test = preprocessing.scale(X_test)
            LDAClassifier.fit(X_train, y_train)
            y_predict = LDAClassifier.predict(X_test)
            #probs = LDAClassifier.predict_proba(X_test)
            #print(y_predict.shape)
            #print(probs.shape)
            #for i in range(len(probs)):
            #    print('{0:.10f}'.format(probs[i][0]))
            #    print('{0:.10f}'.format(probs[i][1]))
            print(str(i*7.8) + "ms")
            print(classification_report(y_test, y_predict))
            fpr, tpr, thresholds = metrics.roc_curve(y_test, y_predict)
            acc_auc = metrics.auc(fpr, tpr)
            print("AUC: " + str(acc_auc))
            print("-----------------------")
        fi += 1
    