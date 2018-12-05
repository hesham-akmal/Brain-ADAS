import pandas as pd
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_curve, auc
from sklearn.linear_model import LogisticRegression  # Logistic Regression model
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split  # to obtain train and test datasets for the same file
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis  # LDA model

# different windows to be made (decrease Num of Electrodes) lsa
# made on all subjects (for all subjects) done 
# all electrodes , emotive electrodes () lsa

clazzifiersNames = ["Linear Discriminant Analyzer", "Logistic Regressor"]
clazzifiers = {clazzifiersNames[0]: LinearDiscriminantAnalysis(), clazzifiersNames[1]: LogisticRegression()}

subjectsNames = ["VPae", "VPbad", "VPbax", "VPbba", "VPdx", "VPgaa", "VPgab", "VPgac", "VPgae", "VPgag", "VPgah", "VPgal", "VPgam", "VPih", "VPii", "VPja","VPsaj", "VPsal"]
# subjectsNames = ["VPae"]



aucBest = {clazzifiersNames[0]: 0, clazzifiersNames[1]: 0}
aucTotal = {clazzifiersNames[0]: 0, clazzifiersNames[1]: 0}
accuracyBest = {clazzifiersNames[0]: 0, clazzifiersNames[1]: 0}
accuracyTotal = {clazzifiersNames[0]: 0, clazzifiersNames[1]: 0}
precisionBest = {clazzifiersNames[0]: [0, 0], clazzifiersNames[1]: [0, 0]}
precisionTotal = {clazzifiersNames[0]: [0, 0], clazzifiersNames[1]: [0, 0]}
recallBest = {clazzifiersNames[0]: [0, 0], clazzifiersNames[1]: [0, 0]}
recallTotal = {clazzifiersNames[0]: [0, 0], clazzifiersNames[1]: [0, 0]}
FscoreBest = {clazzifiersNames[0]: [0, 0], clazzifiersNames[1]: [0, 0]}
FscoreTotal = {clazzifiersNames[0]: [0, 0], clazzifiersNames[1]: [0, 0]}
numberOfComponentss = -1
classifierNameFound = ""


def prepareDataSKLearn(fileNameOrPath):
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


def startML(trainingFeatures, trainingLabels, testFeatures, actualResults, isPCA=False, n_components=-1, classifierName=""):
    global clazzifiers
    classifierToUse = clazzifiers[classifierName]
    # training the model
    print("Training ..")
    classifierToUse.fit(trainingFeatures, trainingLabels)
    # testing the model
    print("Testing ....")
    predictedResults = classifierToUse.predict(testFeatures)
    # making calculations and evaluations
    # print("Parameters trained:\n")
    # print(str(LogisticRegressionClassifier.coef_[0]))
    printResultsSklearn(actualResults, predictedResults, isPCA, n_components, classifierName)


def startMLwithPCA(trainingFeatures, trainingLabels, testFeatures, actualResults, classifierName=""):
    scaler = StandardScaler()
    # Fit on training set only.
    scaler.fit(trainingFeatures)
    # Apply transform to both the training set and the test set.
    train_img = scaler.transform(trainingFeatures)
    test_img = scaler.transform(testFeatures)
    for i in range(1, 31):
        print("Taking " + str(i * 100) + " components")
        pca = PCA(n_components=(i * 100))
        pca.fit(train_img)
        PCA_training_features = pca.transform(train_img)
        PCA_testing_features = pca.transform(test_img)
        startML(PCA_training_features, trainingLabels, PCA_testing_features, actualResults, True, (i * 100), classifierName)


def printResultsSklearn(actualResults, predictedResults, isPCA=False, n_components=-1, classifierName=""):
    global numberOfComponentss, classifierNameFound, aucBest, aucTotal, accuracyBest, accuracyTotal, precisionBest, precisionTotal, recallBest, recallTotal, FscoreBest, FscoreTotal
    print("\nResults:-")
    precision, recall, Fscore, support = precision_recall_fscore_support(y_true=actualResults, y_pred=predictedResults)
    accuracy = accuracy_score(y_true=actualResults, y_pred=predictedResults)
    # AUC calculation
    fpr, tpr, thresholds = roc_curve(actualResults, predictedResults, pos_label=1)
    AUCvalue = auc(fpr, tpr)
    print("accuracy =" + str(accuracy))
    print("AUCvalue =" + str(AUCvalue))
    print("Precision=" + str(precision))
    print("recall   =" + str(recall))
    print("Fscore   =" + str(Fscore))
    print("support  =" + str(support))
    # to check for best PCA
    b1 = precision[0] >= precisionBest[classifierName][0] and precision[1] >= precisionBest[classifierName][1]
    b2 = recall[0] >= recallBest[classifierName][0] and recall[1] >= recallBest[classifierName][1]
    if b1 and b2:
        classifierNameFound = classifierName
        aucBest[classifierName] = AUCvalue
        accuracyBest[classifierName] = accuracy
        precisionBest[classifierName][0] = precision[0]
        precisionBest[classifierName][1] = precision[1]
        recallBest[classifierName][0] = recall[0]
        recallBest[classifierName][1] = recall[1]
        FscoreBest[classifierName][0] = Fscore[0]
        FscoreBest[classifierName][1] = Fscore[1]
        if (isPCA):
            numberOfComponentss = n_components
        else:
            numberOfComponentss = -1
    aucTotal[classifierName] += AUCvalue
    accuracyTotal[classifierName] += accuracy
    recallTotal[classifierName][0] += recall[0]
    recallTotal[classifierName][1] += recall[1]
    FscoreTotal[classifierName][0] += Fscore[0]
    FscoreTotal[classifierName][1] += Fscore[1]
    precisionTotal[classifierName][0] += precision[0]
    precisionTotal[classifierName][1] += precision[1]


for subName in subjectsNames:
    print("Started Working on File->" + subName + ".csv")
    trainingFeatures, trainingLabels, testFeatures, actualResults = prepareDataSKLearn("dataset/" + subName + ".csv")
    for clsName in clazzifiersNames:
        print("Started " + clsName)
        startML(trainingFeatures, trainingLabels, testFeatures, actualResults, False, -1, clsName)
        print("Finished " + clsName)
        print("Started " + clsName + " with PCA")
        startMLwithPCA(trainingFeatures, trainingLabels, testFeatures, actualResults, clsName)
        print("Finished " + clsName + " with PCA")
    print("Finished Working on File->" + subName + ".csv")
    print("-----------------------------------------------------------------------------------------------------------")
numberOfSubjects = subjectsNames.__len__()
numberOfLoopsPerSubject = 31
print("--------------")
print("|FINAL REPORT|")
print("--------------")

for cls in clazzifiersNames:
    print("----------------------")
    print(cls + " OF ALL SUBJECTS")
    print("-------")
    print("AVERAGE")
    print("-------")
    print("Accuracy  =" + str(accuracyTotal[cls] / (numberOfLoopsPerSubject * numberOfSubjects)))
    print("AUCvalue  =" + str(aucTotal[cls] / (numberOfLoopsPerSubject * numberOfSubjects)))
    print("Precision0=" + str(precisionTotal[cls][0] / (numberOfLoopsPerSubject * numberOfSubjects)))
    print("Precision1=" + str(precisionTotal[cls][1] / (numberOfLoopsPerSubject * numberOfSubjects)))
    print("recall0   =" + str(recallTotal[cls][0] / (numberOfLoopsPerSubject * numberOfSubjects)))
    print("recall1   =" + str(recallTotal[cls][1] / (numberOfLoopsPerSubject * numberOfSubjects)))
    print("Fscore0   =" + str(FscoreTotal[cls][0] / (numberOfLoopsPerSubject * numberOfSubjects)))
    print("Fscore1   =" + str(FscoreTotal[cls][1] / (numberOfLoopsPerSubject * numberOfSubjects)))
    print("\n----")
    print("BEST")
    print("------")
    print("Accuracy  =" + str(accuracyBest[cls]))
    print("AUCvalue  =" + str(aucBest[cls]))
    print("Precision0=" + str(precisionBest[cls][0]))
    print("Precision1=" + str(precisionBest[cls][1]))
    print("recall0   =" + str(recallBest[cls][0]))
    print("recall1   =" + str(recallBest[cls][1]))
    print("Fscore0   =" + str(FscoreBest[cls][0]))
    print("Fscore1   =" + str(FscoreBest[cls][1]))
print("\nbest Classifier is " + classifierNameFound)
print("N_components is " + numberOfComponentss.__str__())

# df.drop(df.columns[0:1800], axis=1, inplace=True)
# df.drop(df.columns[300:1200], axis=1, inplace=True)
# df.drop(df.columns[600:4500], axis=1, inplace=True)
# df.drop(df.columns[900:1200], axis=1, inplace=True)
# df.drop(df.columns[1200:1500], axis=1, inplace=True)
# df.drop(df.columns[1500:5700], axis=1, inplace=True)
# df.drop(df.columns[1800:2700], axis=1, inplace=True)
# df.drop(df.columns[2100:len(df.columns) - 1], axis=1, inplace=True)
