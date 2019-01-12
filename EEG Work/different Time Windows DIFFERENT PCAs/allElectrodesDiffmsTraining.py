import datetime
import sys

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis  # LDA model
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_curve, auc
from sklearn.model_selection import train_test_split  # to obtain train and test datasets for the same file
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle

np.set_printoptions(threshold=np.inf, linewidth=300)

# different Time Windows with LDA as best Classifier to check PCA effects

# all electrodes , emotive electrodes () lsa
# different windows to be made (decrease Num of columns/electrode) done
# made on all subjects (for all subjects) done

subjectsNames = ["VPae", "VPbad", "VPbax", "VPbba", "VPdx", "VPgaa", "VPgab", "VPgac", "VPgae", "VPgag", "VPgah", "VPgal", "VPgam", "VPih", "VPii", "VPja", "VPsaj", "VPsal"]
#subjectsNames = ["VPae"]

numberOfSubjects = subjectsNames.__len__()
numberOfLoopsPerSubject = 30
fileIndex = 0

LDAResults = np.zeros(shape=(numberOfSubjects, 11), dtype=float)
LDAwithPCAResults = np.zeros(shape=(numberOfSubjects, (numberOfLoopsPerSubject - 1), 11), dtype=float)


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

    # drop non used features
    numberOfElectrodes = 60
    nColToKeep = int(sys.argv[1])
    print("Number OF Columns KEPT=" + str(nColToKeep))

    if (nColToKeep > 280) or ((nColToKeep % 10 != 0) and (nColToKeep != 0)):
        print("Error")
        exit()

    for i in range(1, numberOfElectrodes):
        trainingFeatures = trainingFeatures.drop(trainingFeatures.columns[(i * nColToKeep):((i * nColToKeep) + (300 - nColToKeep))], axis=1)
        testFeatures = testFeatures.drop(testFeatures.columns[(i * nColToKeep):((i * nColToKeep) + (300 - nColToKeep))], axis=1)

    return trainingFeatures, trainingLabels, testFeatures, actualResults


def showResults(actualResults, predictedResults, isPCA=False, n_components=-1, loopNum=-1):
    global LDAwithPCAResults, LDAResults, fileIndex
    precision, recall, Fscore, support = precision_recall_fscore_support(y_true=actualResults, y_pred=predictedResults)
    accuracy = accuracy_score(y_true=actualResults, y_pred=predictedResults)
    fpr, tpr, thresholds = roc_curve(actualResults, predictedResults, pos_label=1)
    AUCvalue = auc(fpr, tpr)
    if isPCA:
        LDAwithPCAResults[fileIndex, loopNum, 0] = n_components
        LDAwithPCAResults[fileIndex, loopNum, 1] = accuracy
        LDAwithPCAResults[fileIndex, loopNum, 2] = AUCvalue
        LDAwithPCAResults[fileIndex, loopNum, 3] = precision[0]
        LDAwithPCAResults[fileIndex, loopNum, 4] = precision[1]
        LDAwithPCAResults[fileIndex, loopNum, 5] = recall[0]
        LDAwithPCAResults[fileIndex, loopNum, 6] = recall[1]
        LDAwithPCAResults[fileIndex, loopNum, 7] = Fscore[0]
        LDAwithPCAResults[fileIndex, loopNum, 8] = Fscore[1]
        LDAwithPCAResults[fileIndex, loopNum, 9] = support[0]
        LDAwithPCAResults[fileIndex, loopNum, 10] = support[1]
    else:
        LDAResults[fileIndex, 0] = -1
        LDAResults[fileIndex, 1] = accuracy
        LDAResults[fileIndex, 2] = AUCvalue
        LDAResults[fileIndex, 3] = precision[0]
        LDAResults[fileIndex, 4] = precision[1]
        LDAResults[fileIndex, 5] = recall[0]
        LDAResults[fileIndex, 6] = recall[1]
        LDAResults[fileIndex, 7] = Fscore[0]
        LDAResults[fileIndex, 8] = Fscore[1]
        LDAResults[fileIndex, 9] = support[0]
        LDAResults[fileIndex, 10] = support[1]


def startML(trainingFeatures, trainingLabels, testFeatures, actualResults, isPCA=False, n_components=-1, loopNum=-1):
    classifierToUse = LinearDiscriminantAnalysis()
    classifierToUse.fit(trainingFeatures, trainingLabels)
    predictedResults = classifierToUse.predict(testFeatures)
    showResults(actualResults, predictedResults, isPCA, n_components, loopNum)


def startMLwithPCA(trainingFeatures, trainingLabels, testFeatures, actualResults):
    global numberOfLoopsPerSubject
    scaler = StandardScaler()
    scaler.fit(trainingFeatures)
    train_img = scaler.transform(trainingFeatures)
    test_img = scaler.transform(testFeatures)
    # to take the number of loops as a multiple of the numberOfLoops/Subject
    theLoopsToTake = numberOfLoopsPerSubject * 100
    for i in range(100, theLoopsToTake, 100):
        if theLoopsToTake <= train_img.shape[1]:
            pca = PCA(n_components=i)
        else:
            pca = PCA(n_components=train_img.shape[1])
        pca.fit(train_img)
        PCA_training_features = pca.transform(train_img)
        PCA_testing_features = pca.transform(test_img)
        startML(PCA_training_features, trainingLabels, PCA_testing_features, actualResults, True, i, int((i / 100) - 1))


trainingAllStartTime = datetime.datetime.now().replace(microsecond=0)
for fileIndex in range(fileIndex, numberOfSubjects):
    print("------------------------------------------------------------------------------------------------------------------------------")
    print("Started Working on File->" + subjectsNames[fileIndex] + ".csv")
    a = datetime.datetime.now().replace(microsecond=0)
    print("Getting File Content")
    trainingFeatures, trainingLabels, testFeatures, actualResults = prepareFileContent("dataset/" + subjectsNames[fileIndex] + ".csv")
    print("Training Features Shape:" + str(trainingFeatures.shape))
    print("Testing Features Shape:" + str(testFeatures.shape))
    startML(trainingFeatures, trainingLabels, testFeatures, actualResults, False, -1, -1)
    print("Started PCA")
    startMLwithPCA(trainingFeatures, trainingLabels, testFeatures, actualResults)
    print("Finished PCA")
    b = datetime.datetime.now().replace(microsecond=0)
    print("Finished Working on File->" + subjectsNames[fileIndex] + ".csv in " + str(b - a))
    print("-----------------------------------------------------------------------------------------------------------")
trainingAllEndTime = datetime.datetime.now().replace(microsecond=0)

print("\n=========================================================")
print("|FINAL REPORT for " + sys.argv[1] + " columns/Electrode| ")
print("=========================================================")
print("=========================================================")
print("=========================================================")
print("ALL Values OF LDA-PCA")
print(LDAwithPCAResults)
print("=========================================================")
print("=========================================================")
print("=========================================================")
print("\nAverage VALUES OF LDA-PCA")
LDAwithPCAAverageVals = LDAwithPCAResults.T
LDAwithPCAAverageVals = LDAwithPCAAverageVals.mean(axis=2, keepdims=True)
LDAwithPCAAverageVals = LDAwithPCAAverageVals.T
print(LDAwithPCAAverageVals)
print("=========================================================")
print("\nBEST VALUES OF LDA-PCA")
LDAwithPCAResultsBestVals = np.max(LDAwithPCAResults, axis=1)
print(LDAwithPCAResultsBestVals)
print("=========================================================")
print("=========================================================")
print("=========================================================")
print("All Of All LDA-Only")
print(LDAResults)
print("=========================================================")
print("=========================================================")
print("=========================================================")
print("Average LDA-Only")
print(LDAResults.mean(axis=0, keepdims=True))
print("=========================================================")
print("The Whole Training took |" + str(trainingAllEndTime - trainingAllStartTime) + "|")

# df.drop(df.columns[0:1800], axis=1, inplace=True)
# df.drop(df.columns[300:1200], axis=1, inplace=True)
# df.drop(df.columns[600:4500], axis=1, inplace=True)
# df.drop(df.columns[900:1200], axis=1, inplace=True)
# df.drop(df.columns[1200:1500], axis=1, inplace=True)
# df.drop(df.columns[1500:5700], axis=1, inplace=True)
# df.drop(df.columns[1800:2700], axis=1, inplace=True)
# df.drop(df.columns[2100:len(df.columns) - 1], axis=1, inplace=True)
