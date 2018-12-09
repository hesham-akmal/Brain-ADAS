import datetime
import pandas as pd
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_curve, auc
from sklearn.linear_model import LogisticRegression  # Logistic Regression model
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split  # to obtain train and test datasets for the same file
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis  # LDA model
import numpy as np

np.set_printoptions(threshold=np.inf, linewidth=300)

# all electrodes , emotive electrodes () lsa
# different windows to be made (decrease Num of columns/electrode) lsa
# made on all subjects (for all subjects) done

clazzifiersNames = ["Linear Discriminant Analyzer", "Logistic Regressor"]
subjectsNames = ["VPae", "VPbad", "VPbax", "VPbba", "VPdx", "VPgaa", "VPgab", "VPgac", "VPgae", "VPgag", "VPgah", "VPgal", "VPgam", "VPih", "VPii", "VPja", "VPsaj", "VPsal"]
# subjectsNames = ["VPae"]

numberOfSubjects = subjectsNames.__len__()
numberOfLoopsPerSubject = 30
fileIndex = 0

LRResults = np.zeros(shape=(numberOfSubjects, 11), dtype=float)
LRwithPCAResults = np.zeros(shape=(numberOfSubjects, (numberOfLoopsPerSubject - 1), 11), dtype=float)

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
    return trainingFeatures, trainingLabels, testFeatures, actualResults


def showResults(actualResults, predictedResults, isPCA=False, n_components=-1, classifierName="", loopNum=-1):
    global LDAwithPCAResults, LDAResults, LRwithPCAResults, LRResults, clazzifiersNames, fileIndex
    print("\nResults:-")
    precision, recall, Fscore, support = precision_recall_fscore_support(y_true=actualResults, y_pred=predictedResults)
    accuracy = accuracy_score(y_true=actualResults, y_pred=predictedResults)
    fpr, tpr, thresholds = roc_curve(actualResults, predictedResults, pos_label=1)
    AUCvalue = auc(fpr, tpr)

    print("accuracy | AUCvalue | Precision0 | Precision1 | recall0 | recall1 | support0 | support 1")
    print(str(accuracy) + "|" + str(AUCvalue) + "|" + str(precision) + "|" + str(recall) + "|" + str(Fscore) + "|" + str(support))

    if classifierName == clazzifiersNames[0]:
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

    elif classifierName == clazzifiersNames[1]:
        if isPCA:
            LRwithPCAResults[fileIndex, loopNum, 0] = n_components
            LRwithPCAResults[fileIndex, loopNum, 1] = accuracy
            LRwithPCAResults[fileIndex, loopNum, 2] = AUCvalue
            LRwithPCAResults[fileIndex, loopNum, 3] = precision[0]
            LRwithPCAResults[fileIndex, loopNum, 4] = precision[1]
            LRwithPCAResults[fileIndex, loopNum, 5] = recall[0]
            LRwithPCAResults[fileIndex, loopNum, 6] = recall[1]
            LRwithPCAResults[fileIndex, loopNum, 7] = Fscore[0]
            LRwithPCAResults[fileIndex, loopNum, 8] = Fscore[1]
            LRwithPCAResults[fileIndex, loopNum, 9] = support[0]
            LRwithPCAResults[fileIndex, loopNum, 10] = support[1]
        else:
            LRResults[fileIndex, 0] = -1
            LRResults[fileIndex, 1] = accuracy
            LRResults[fileIndex, 2] = AUCvalue
            LRResults[fileIndex, 3] = precision[0]
            LRResults[fileIndex, 4] = precision[1]
            LRResults[fileIndex, 5] = recall[0]
            LRResults[fileIndex, 6] = recall[1]
            LRResults[fileIndex, 7] = Fscore[0]
            LRResults[fileIndex, 8] = Fscore[1]
            LRResults[fileIndex, 9] = support[0]
            LRResults[fileIndex, 10] = support[1]


# separate function for adding more ML models
def getClassifier(classifierName):
    global clazzifiersNames
    if classifierName == clazzifiersNames[0]:
        return LinearDiscriminantAnalysis()
    elif classifierName == clazzifiersNames[1]:
        return LogisticRegression()
    else:
        raise Exception()


def startML(trainingFeatures, trainingLabels, testFeatures, actualResults, isPCA=False, n_components=-1, classifierName="", loopNum=-1):
    classifierToUse = getClassifier(classifierName)
    print("Training ..")
    classifierToUse.fit(trainingFeatures, trainingLabels)
    print("Making Predictions ....")
    predictedResults = classifierToUse.predict(testFeatures)
    # making calculations and evaluations
    # print("Parameters trained:\n")
    # print(str(LogisticRegressionClassifier.coef_[0]))
    showResults(actualResults, predictedResults, isPCA, n_components, classifierName, loopNum)


def startMLwithPCA(trainingFeatures, trainingLabels, testFeatures, actualResults):
    global clazzifiersNames, numberOfLoopsPerSubject
    scaler = StandardScaler()
    # Fit on training set only.
    scaler.fit(trainingFeatures)
    # Apply transform to both the training set and the test set.
    train_img = scaler.transform(trainingFeatures)
    test_img = scaler.transform(testFeatures)
    # to take the number of loops as a multiple of the numberOfLoops/Subject
    theLoopsToTake = numberOfLoopsPerSubject * 100
    for i in range(100, theLoopsToTake, 100):
        print("Taking " + str(i) + " components")
        pca = PCA(n_components=i)
        pca.fit(train_img)
        PCA_training_features = pca.transform(train_img)
        PCA_testing_features = pca.transform(test_img)
        for cls in clazzifiersNames:
            print("Learning " + cls + " with PCA")
            startML(PCA_training_features, trainingLabels, PCA_testing_features, actualResults, True, i, cls, int((i / 100) - 1))


trainingAllStartTime = datetime.datetime.now().replace(microsecond=0)
for fileIndex in range(fileIndex, numberOfSubjects):
    print("Started Working on File->" + subjectsNames[fileIndex] + ".csv")
    a = datetime.datetime.now().replace(microsecond=0)
    print("getting file content")
    trainingFeatures, trainingLabels, testFeatures, actualResults = prepareFileContent("dataset/" + subjectsNames[fileIndex] + ".csv")
    for cls in clazzifiersNames:
        print("Learning Normal " + cls)
        startML(trainingFeatures, trainingLabels, testFeatures, actualResults, False, -1, cls)
    print("------------------------------------------------------------------------------------------------------------------------------")
    print("Started PCA")
    startMLwithPCA(trainingFeatures, trainingLabels, testFeatures, actualResults)
    print("Finished PCA")
    b = datetime.datetime.now().replace(microsecond=0)
    print("Finished Working on File->" + subjectsNames[fileIndex] + ".csv in " + str(b - a))
    print("-----------------------------------------------------------------------------------------------------------")
trainingAllEndTime = datetime.datetime.now().replace(microsecond=0)

print("\n==============")
print("|FINAL REPORT|")
print("==============")

print("\n-------------------------")
print("|Logistic Regression PCA|")
print("-------------------------")

print("=========================================================")
print("Logistic Regression with PCA Average")
LRwithPCAAverageVals = LRwithPCAResults.T
LRwithPCAAverageVals = LRwithPCAAverageVals.mean(axis=2, keepdims=True)
LRwithPCAAverageVals = LRwithPCAAverageVals.T
print(LRwithPCAAverageVals)
print("=========================================================")

print("Logistic Regression with PCA Best Values")
LRwithPCAResultsBestVals = np.max(LRwithPCAResults, axis=1)
print(LRwithPCAResultsBestVals)

print("Logistic Regression with PCA Number of component used for each Best")
LRwithPCAResultsBestComponentsUsed = (np.argmax(LRwithPCAResults, axis=1) + 1) * 100
print(LRwithPCAResultsBestComponentsUsed)
print("=========================================================")

print("Logistic Regression Normal Average")
print(LRResults.mean(axis=0, keepdims=True))
print("=========================================================")

print("\n----------------------------------")
print("|Linear Discriminant Analyzer PCA|")
print("----------------------------------")

print("\nLinear Discriminant Analyzer with PCA Average")
LDAwithPCAAverageVals = LDAwithPCAResults.T
LDAwithPCAAverageVals = LDAwithPCAAverageVals.mean(axis=2, keepdims=True)
LDAwithPCAAverageVals = LDAwithPCAAverageVals.T
print(LDAwithPCAAverageVals)
print("=========================================================")

print("Linear Discriminant Analyzer with PCA Best Values")
LDAwithPCAResultsBestVals = np.max(LDAwithPCAResults, axis=1)
print(LDAwithPCAResultsBestVals)

print("\nLinear Discriminant Analyzer with PCA Number of component used for each Best")
LDAwithPCAResultsBestComponentsUsed = (np.argmax(LDAwithPCAResults, axis=1) + 1) * 100
print(LDAwithPCAResultsBestComponentsUsed)
print("=========================================================")

print("Linear Discriminant Analyzer Normal Average")
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
