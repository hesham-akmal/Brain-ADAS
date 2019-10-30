
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis 
from sklearn import preprocessing
from sklearn import metrics
from visualization import make_columns_drawing
from visualization import mean_zero
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

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
    return mean_features_pos, mean_features_neg

def get_drop_cols(i1, electrodes_len, newCols):
    dropCols = []
    nums = np.arange(i1, 192)
    for i in range(electrodes_len):
        name = newCols[i*192].split('.')[0]
        dropCols.append([name + '.' + str(num) for num in nums])
    return np.array(dropCols).flatten()

def apply_filter(pos, neg, fc):
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
    #out_bound = int((new_signal_pos.shape[0] - 192)/2)
    
    for i in range(len(pos)):
        for j in range(14):
            s = list(pos.iloc[i][j*192:j*192+192])
            mean = np.mean(s)
            s -= mean
            filter_pos[i][j*192:j*192+192] = np.convolve(s, sinc_func)[25:242-25]
            
    for i in range(len(neg)):
        for j in range(14):
            s = list(neg.iloc[i][j*192:j*192+192])
            mean = np.mean(s)
            s -= mean
            filter_neg[i][j*192:j*192+192] = np.convolve(s, sinc_func)[25:242-25]
            
    filter_pos =  pd.DataFrame(data=filter_pos, columns=pos.columns)
    filter_neg =  pd.DataFrame(data=filter_neg, columns=neg.columns) 
            
    return filter_pos, filter_neg

def train_test_split_data(pos, neg, test_size):
    pos_size_test = int(len(pos)*test_size)
    neg_size_test = int(len(neg)*test_size)
    all_test = pos[:pos_size_test].append(neg[:neg_size_test])
    all_test = all_test.sample(frac=1)
    y_test = all_test['y']
    X_test = all_test.drop(['y'], axis = 1)
    all_train = pos[pos_size_test:].append(neg[neg_size_test:])
    all_train = all_train.sample(frac=1)
    y_train = all_train['y']
    X_train = all_train.drop(['y'], axis = 1)
    return X_train, X_test, y_train, y_test


def classify_diff_intervals(fnames, electrodes, preprocess, filter_apply, fc, apply_pca):
    LDAClassifier = LinearDiscriminantAnalysis()
    cols = make_columns_drawing(electrodes + ["CVprob"])
    newCols = make_columns_drawing(electrodes + ["CVprob"])
    electrodes_len = len(electrodes)
    fi = 0
    n = 0
    for f in fnames:
        print(f)
        for i in np.arange(12, 180, 12):
            pos, neg = upload_pos_neg(f)
            #all_cols = pos.columns
            if(filter_apply):
                posElec, negElec = apply_filter(pos.drop(pos.columns[pos.columns.str.startswith('CVprob.')], axis=1)
                                        , neg.drop(neg.columns[pos.columns.str.startswith('CVprob.')], axis=1), fc)
                pos =  pd.concat([posElec, pos[pos.columns[pos.columns.str.startswith('CVprob.')]]], axis=1)
                neg =  pd.concat([negElec, neg[neg.columns[neg.columns.str.startswith('CVprob.')]]], axis=1)
            #pos, neg = select_electrodes(electrodes, pos, neg)
            dropCols = get_drop_cols(i, electrodes_len, newCols)
            pos = pos.drop(dropCols, axis = 1)
            neg = neg.drop(dropCols, axis = 1)
            mean_features_pos, mean_features_neg = time_intervals_features(pos, neg, i, int(i*6/12), electrodes_len, cols)
            mean_features_pos['y'] = 1
            mean_features_neg['y'] = 0
            #pos['y'] = 1
            #neg['y'] = 0
            X_train, X_test, y_train, y_test = train_test_split_data(mean_features_pos, mean_features_neg, test_size=0.3)
            #X_train, X_test, y_train, y_test = train_test_split_data(pos, neg, test_size=0.3)
            X_train = np.nan_to_num(X_train)
            X_test = np.nan_to_num(X_test)
            if(apply_pca):
                #scaler = MinMaxScaler(feature_range=[0, 1])
                #X_train = scaler.fit_transform(X_train)
                #X_test = scaler.fit_transform(X_test)
                #n += 100
                print(X_train.shape[1])
                #print(n)
                for k in np.arange(168, 10, 10):
                    print("PCA:" + str(k))
                    pca = PCA(n_components = 168)
                    X_train = pca.fit_transform(X_train)
                    X_test = pca.transform(X_test)
                    if (preprocess):
                        X_train = preprocessing.scale(X_train)
                        X_test = preprocessing.scale(X_test)
                    LDAClassifier.fit(X_train, y_train)
                    y_predict = LDAClassifier.predict(X_test)
                    #probs = LDAClassifier.predict_proba(X_test)
                    #print(y_predict.shape)
                    #print(probs.shape)
                    #for i in range(len(probs)):
                    #    print('{0:.10f}'.format(probs[i][0]))
                    #    print('{0:.10f}'.format(probs[i][1]))
                    print(str(i*7.8125) + "ms")
                    print(classification_report(y_test, y_predict))
                    fpr, tpr, thresholds = metrics.roc_curve(y_test, y_predict)
                    acc_auc = metrics.auc(fpr, tpr)
                    print("AUC: " + str(acc_auc))
                    print("-----------------------")
            if (preprocess):
                X_train = preprocessing.scale(X_train)
                X_test = preprocessing.scale(X_test)
            LDAClassifier.fit(X_train, y_train)
            y_predict = LDAClassifier.predict(X_test)
            #print(y_predict)
            probs = LDAClassifier.predict_proba(X_test)
            #print(probs)
            #print(y_predict.shape)
            #print(probs.shape)
            #for i in range(len(probs)):
            #    print('{0:.10f}'.format(probs[i][0]))
            #    print('{0:.10f}'.format(probs[i][1]))
            print(str(i*7.8125) + "ms")
            print(classification_report(y_test, y_predict))
            fpr, tpr, thresholds = metrics.roc_curve(y_test, y_predict)
            acc_auc = metrics.auc(fpr, tpr)
            print("AUC: " + str(acc_auc))
            print("-----------------------")
        fi += 1
    