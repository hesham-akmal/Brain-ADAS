from sklearn.linear_model import LogisticRegression  # Logisitic Regression model
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis  # LDA model
from sklearn.model_selection import train_test_split  # to obtain train and test datasets for the same file
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_curve, auc
from sklearn.decomposition import PCA

import pandas as pd
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

accuracyTotal = 0
aucTotal = 0
precisionTotal = [0, 0]
recallTotal = [0, 0]
fscoreTotal = [0, 0]

precisionBest = [0, 0]
recallBest = [0, 0]
aucBest = 0
accuracyBest = 0
numberOfComponentss = -1;
classifierNameG = ""


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
    trainingFeatures, testFeatures, trainingLabels, actualResults = train_test_split(trainingFeaturesX, trainingLabely,test_size=0.33, random_state=42)
    return trainingFeatures, trainingLabels, testFeatures, actualResults


def printResultsSklearn(actualResults, predictedResults, isPCA=False, n_components=-1, classifierName=""):
    global accuracyTotal
    global precisionTotal
    global recallTotal
    global fscoreTotal
    global aucTotal
    global numberOfComponentss
    global classifierNameG
    global precisionBest
    global recallBest
    global aucBest
    global accuracyBest

    print("\nResults:-")
    precision, recall, Fscore, support = precision_recall_fscore_support(y_true=actualResults, y_pred=predictedResults)
    accuracy = accuracy_score(y_true=actualResults, y_pred=predictedResults)
    fpr, tpr, thresholds = roc_curve(actualResults, predictedResults, pos_label=1)
    AUCvalue = auc(fpr, tpr)

    # to check for best PCA
    b1 = precision[0] >= precisionBest[0] and precision[1] >= precisionBest[1]
    b2 = recall[0] >= recallBest[0] and recall[1] >= precisionBest[1]
    if b1 or b2:
        classifierNameG = classifierName
        precisionBest[0] = precision[0]
        precisionBest[1] = precision[1]
        recallBest[0] = recall[0]
        recallBest[1] = recall[1]
        aucBest = AUCvalue
        accuracyBest = accuracy
        if (isPCA):
            numberOfComponentss = n_components
        else: 
            numberOfComponentss=-1

    aucTotal += AUCvalue
    accuracyTotal += accuracy
    precisionTotal[0] += precision[0]
    precisionTotal[1] += precision[1]
    recallTotal[0] += recall[0]
    recallTotal[1] += recall[1]
    fscoreTotal[0] += Fscore[0]
    fscoreTotal[1] += Fscore[1]

    print("accuracy =" + str(accuracy))
    print("AUCvalue =" + str(AUCvalue))
    print("Precision=" + str(precision))
    print("recall   =" + str(recall))
    print("Fscore   =" + str(Fscore))
    print("support  =" + str(support))

    # runs the main Machine Learning code with preparations using scikit-learn Framework


def LDAclassification(traningFeatures, trainingLabels, testFeatures, actualResults, isPCA=False, n_components=-1):
    print("---Creating Linear Discriminant Analyzer---")
    LDAClassifier = LinearDiscriminantAnalysis()
    # training the model
    print("Training ..")
    LDAClassifier.fit(traningFeatures, trainingLabels)
    # testing the model
    print("Testing ....")
    predictedResults = LDAClassifier.predict(testFeatures)
    # making calcuations and evaluations
    # print("Parameters trained:\n")
    # print(str(LDAClassifier.coef_[0]))
    printResultsSklearn(actualResults=actualResults, predictedResults=predictedResults, classifierName="LDA",isPCA=isPCA, n_components=n_components)
    print("---Finished LDA---\n")


def LRClassification(traningFeatures, trainingLabels, testFeatures, actualResults, isPCA=False, n_components=-1):
    print("---Creating Logistic Regressor---")
    LogisticRegressionClassifier = LogisticRegression()
    # training the model
    print("Training ..")
    LogisticRegressionClassifier.fit(traningFeatures, trainingLabels)
    # testing the model
    print("Testing ....")
    predictedResults = LogisticRegressionClassifier.predict(testFeatures)
    # making calcuations and evaluations
    # print("Parameters trained:\n")
    # print(str(LogisticRegressionClassifier.coef_[0]))
    printResultsSklearn(actualResults=actualResults, predictedResults=predictedResults, classifierName="LR",isPCA=isPCA, n_components=n_components)
    print("---Finished Logistic Regression---")


def executeSKLearnModels(trainingFeatures, trainingLabels, testFeatures, actualResults):
    LRClassification(trainingFeatures, trainingLabels, testFeatures, actualResults)
    LDAclassification(trainingFeatures, trainingLabels, testFeatures, actualResults)


def executeSKLearnModelsPCA(traningFeatures, trainingLabels, testFeatures, actualResults):
    scaler = StandardScaler()
    # Fit on training set only.
    scaler.fit(traningFeatures)
    # Apply transform to both the training set and the test set.
    train_img = scaler.transform(traningFeatures)
    test_img = scaler.transform(testFeatures)

    for i in range(100, 3000, 100):
        print("Taking " + str(i) + " components")
        pca = PCA(n_components=i)
        pca.fit(train_img)
        PCA_training_features = pca.transform(train_img)
        PCA_testing_features = pca.transform(test_img)
        LRClassification(PCA_training_features, trainingLabels, PCA_testing_features, actualResults, isPCA=True,n_components=i)
        LDAclassification(PCA_training_features, trainingLabels, PCA_testing_features, actualResults, isPCA=True,n_components=i)


# runs the main Machine Learning code with preparations using scikit-learn Framework
FilesName = ["ae", "bad", "bax", "bba", "dx", "gaa", "gab", "gac", "gae", "gag", "gah", "gal", "gam", "ih", "ii", "ja","saj", "sal"]

for fName in FilesName:
    print("-------------------------------------------------------------------------------------------------------")
    print("Current Working on File->VP" + fName + ".csv")
    trainingFeatures, trainingLabels, testFeatures, actualResults = prepareDataSKLearn("dataset/VP" + fName + ".csv")
    print("BEFORE PCA")
    executeSKLearnModels(trainingFeatures, trainingLabels, testFeatures, actualResults)
    print("---------------------------------------")
    print("AFTER PCA")
    print("---------------------------------------")
    executeSKLearnModelsPCA(trainingFeatures, trainingLabels, testFeatures, actualResults)
    print("Finished Working on File->VP" + fName + ".csv")

numberOfClassifiers=2
numberOfloops = 30
numberOfSubjects = 18

#differnet windows to be made (decrease Num of Electrodes
#made on all subjects (for all subjects)
#all electrodes , emotive electrodes ()

print("Average Values of All Subjects")
print("accuracy =" + str(accuracyTotal / (numberOfClassifiers*numberOfloops*numberOfSubjects)))
print("AUCvalue =" + str(aucTotal / (numberOfClassifiers*numberOfloops*numberOfSubjects)))

print("Precision0=" + str(precisionTotal[0] / (numberOfClassifiers*numberOfloops*numberOfSubjects)))
print("Precision1=" + str(precisionTotal[1] / (numberOfClassifiers*numberOfloops*numberOfSubjects)))

print("recall0   =" + str(recallTotal[0] / (numberOfClassifiers*numberOfloops*numberOfSubjects)))
print("recall1   =" + str(recallTotal[1] / (numberOfClassifiers*numberOfloops*numberOfSubjects)))

print("Fscore   =" + str(fscoreTotal[0] / (numberOfClassifiers*numberOfloops*numberOfSubjects)))
print("Fscore   =" + str(fscoreTotal[1] / (numberOfClassifiers*numberOfloops*numberOfSubjects)))

print("\nbest Values of All Subjects in PCA")
print("ClassifierName=" + classifierNameG)
print("n_compnents=" + str(numberOfComponentss))
print("accuracy =" + str(accuracyBest))
print("AUCvalue =" + str(aucBest))

print("Precision0=" + str(precisionBest[0]))
print("Precision1=" + str(precisionBest[1]))

print("recall0  =" + str(recallBest[0]))
print("recall1  =" + str(recallBest[1]))
