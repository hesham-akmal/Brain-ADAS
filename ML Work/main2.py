import datetime

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis  # LDA model
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_curve, auc
from sklearn.model_selection import train_test_split  # to obtain train and test datasets for the same file
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle

np.set_printoptions(threshold=np.inf, linewidth=3000)

# all electrodes , emotive electrodes () lsa
# different windows to be made (decrease Num of columns/electrode) lsa
# made on all subjects (for all subjects) done

subjectsNames = ["VPae", "VPbad", "VPbax", "VPbba", "VPdx", "VPgaa", "VPgab", "VPgac", "VPgae", "VPgag", "VPgah", "VPgal", "VPgam", "VPih", "VPii", "VPja", "VPsaj", "VPsal"]
#subjectsNames = ["VPae"]
numberOfSubjects = subjectsNames.__len__()
numberOfElectrodes = 60

fileIndex = 0
# LDAwith1000PCAResult dim is (numSubjects,timeIntervals(1->14),results)
LDAwith1000PCAResults = np.zeros(shape=(numberOfSubjects, 14, 11), dtype=float)


def prepareFileContent(fileNameOrPath):
    # read file data ( subject file )
    FileContent = pd.read_csv(fileNameOrPath)
    # randomize the order of data
    FileContent = shuffle(FileContent)
    # change brake and normal into 1 and 0
    FileContent['y'] = (FileContent['y'] == "brake").astype(int)
    # get features and labels
    featuresColumns = FileContent.columns[0:len(FileContent.columns) - 1]
    labelsColumn = FileContent.columns[len(FileContent.columns) - 1]
    trainingFeaturesX = FileContent.loc[:, featuresColumns]
    trainingLabely = FileContent.loc[:, labelsColumn]
    # split the data into training and test
    trainingFeatures, testFeatures, trainingLabels, actualResults = train_test_split(trainingFeaturesX, trainingLabely, test_size=0.33, random_state=42)
    return trainingFeatures, trainingLabels, testFeatures, actualResults


def showResults(actualResults, predictedResults, n_components=-1, loopNum=-1):
    global LDAwith1000PCAResults, fileIndex
    print("\nResults:-")
    precision, recall, Fscore, support = precision_recall_fscore_support(y_true=actualResults, y_pred=predictedResults)
    accuracy = accuracy_score(y_true=actualResults, y_pred=predictedResults)
    fpr, tpr, thresholds = roc_curve(actualResults, predictedResults, pos_label=1)
    AUCvalue = auc(fpr, tpr)
    print("accuracy | AUCvalue | Precision0 | Precision1 | recall0 | recall1 | support0 | support 1")
    print(str(accuracy) + "|" + str(AUCvalue) + "|" + str(precision) + "|" + str(recall) + "|" + str(Fscore) + "|" + str(support))
    LDAwith1000PCAResults[fileIndex, loopNum, 0] = n_components
    LDAwith1000PCAResults[fileIndex, loopNum, 1] = accuracy
    LDAwith1000PCAResults[fileIndex, loopNum, 2] = AUCvalue
    LDAwith1000PCAResults[fileIndex, loopNum, 3] = precision[0]
    LDAwith1000PCAResults[fileIndex, loopNum, 4] = precision[1]
    LDAwith1000PCAResults[fileIndex, loopNum, 5] = recall[0]
    LDAwith1000PCAResults[fileIndex, loopNum, 6] = recall[1]
    LDAwith1000PCAResults[fileIndex, loopNum, 7] = Fscore[0]
    LDAwith1000PCAResults[fileIndex, loopNum, 8] = Fscore[1]
    LDAwith1000PCAResults[fileIndex, loopNum, 9] = support[0]
    LDAwith1000PCAResults[fileIndex, loopNum, 10] = support[1]


def startMLwithPCA(trainingFeatures, trainingLabels, testFeatures, actualResults, loopNum):
    scaler = StandardScaler()
    # Fit on training set only.
    scaler.fit(trainingFeatures)
    # Apply transform to both the training set and the test set.
    train_img = scaler.transform(trainingFeatures)
    test_img = scaler.transform(testFeatures)
    # to take the number of loops as a multiple of the numberOfLoops/Subject
    pca = PCA(n_components=1000)
    pca.fit(train_img)
    PCA_training_features = pca.transform(train_img)
    PCA_testing_features = pca.transform(test_img)

    classifierToUse = LinearDiscriminantAnalysis()
    print("Training ..")
    classifierToUse.fit(PCA_training_features, trainingLabels)
    print("Making Predictions ....")
    predictedResults = classifierToUse.predict(PCA_testing_features)
    # making calculations and evaluations
    showResults(actualResults, predictedResults, 1000, loopNum)


trainingAllStartTime = datetime.datetime.now().replace(microsecond=0)

for fileIndex in range(fileIndex, numberOfSubjects):
    print("Started Working on File->" + subjectsNames[fileIndex] + ".csv")
    a = datetime.datetime.now().replace(microsecond=0)
    print("getting file content")
    trainingFeatures, trainingLabels, testFeatures, actualResults = prepareFileContent("dataset/" + subjectsNames[fileIndex] + ".csv")

    loopNum = 0
    for nColToKeep in range(280, 0, -20):
        for i in range(1, numberOfElectrodes):
            trainingFeatures = trainingFeatures.drop(trainingFeatures.columns[(i * nColToKeep):((nColToKeep + 20) + (i - 1) * nColToKeep)], axis=1)
            testFeatures = testFeatures.drop(testFeatures.columns[(i * nColToKeep):((nColToKeep + 20) + (i - 1) * nColToKeep)], axis=1)
        print("====================================")
        print("====================================")
        print("====================================")
        print("====================================")
        print("at nColtoKeep=" + str(nColToKeep))
        print("index in axis 1=" + str(nColToKeep / 20-1))
        print("Training Shape=" + str(trainingFeatures.shape))
        print("Testing Shape=" + str(testFeatures.shape))
        print("Started ML with PCA")
        startMLwithPCA(trainingFeatures, trainingLabels, testFeatures, actualResults, int((nColToKeep / 20) - 1))
        print("Finished ML with PCA")
    b = datetime.datetime.now().replace(microsecond=0)
    print("Finished Working on File->" + subjectsNames[fileIndex] + ".csv in " + str(b - a))
    print("-----------------------------------------------------------------------------------------------------------")

trainingAllEndTime = datetime.datetime.now().replace(microsecond=0)


print("\n==============")
print("|FINAL REPORT|")
print("==============")
print("\n----------------------------------")
print("|Linear Discriminant Analyzer PCA|")
print("----------------------------------")
print("\nLinear Discriminant Analyzer with PCA Average")
LDAwithPCAAverageVals = LDAwith1000PCAResults.T
LDAwithPCAAverageVals = LDAwithPCAAverageVals.mean(axis=2, keepdims=True)
LDAwithPCAAverageVals = LDAwithPCAAverageVals.T
print(LDAwithPCAAverageVals)
print("=========================================================")
print("Linear Discriminant Analyzer with PCA Best Values")
LDAwithPCAResultsBestVals = np.max(LDAwith1000PCAResults, axis=1)
print(LDAwithPCAResultsBestVals)
print("The Whole Training took |" + str(trainingAllEndTime - trainingAllStartTime) + "|")

#EMOTIV ELECTRODES
# df.drop(df.columns[0:1800], axis=1, inplace=True)
# df.drop(df.columns[300:1200], axis=1, inplace=True)
# df.drop(df.columns[600:4500], axis=1, inplace=True)
# df.drop(df.columns[900:1200], axis=1, inplace=True)
# df.drop(df.columns[1200:1500], axis=1, inplace=True)
# df.drop(df.columns[1500:5700], axis=1, inplace=True)
# df.drop(df.columns[1800:2700], axis=1, inplace=True)
# df.drop(df.columns[2100:len(df.columns) - 1], axis=1, inplace=True)
