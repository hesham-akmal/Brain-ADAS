from sklearn import linear_model as sk_models
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

import pandas as pd


# concatenate +ve and -ve events files in one subject file
def concatFiles(negFilePath, posFilePath, desFilePath):
    negFileContent = pd.read_csv(negFilePath)
    posFileContent = pd.read_csv(posFilePath)
    fileContent = negFileContent.append(posFileContent)
    fileContent.to_csv(desFilePath, index=False)



#runs the main Machine Learning code with preparations using scikit-learn Framework
def executeSKLearn(fileNameOrPath):
    # read file data ( subject file )
    FileContent = pd.read_csv(fileNameOrPath)
    # randomize the order of data
    FileContent = shuffle(FileContent)
    # get features and labels
    featuresColumns = FileContent.columns[0:len(FileContent.columns) - 1]
    lablesColumn = FileContent.columns[len(FileContent.columns) - 1]
    trainingFeaturesX = FileContent.loc[:, featuresColumns]
    trainingLabely = FileContent.loc[:, lablesColumn]
    # split the data into training and test
    traningFeatures, testFeatures, trainingLabels, actualResults = train_test_split(trainingFeaturesX, trainingLabely,test_size=0.33, random_state=42)
    classifier = sk_models.LogisticRegression(max_iter=1000)
    #training the model
    classifier.fit(traningFeatures, trainingLabels)
    #testing the model
    predictedResults = classifier.predict(testFeatures)
    #making calcuations and evaluations
    precision, recall, Fscore, support = precision_recall_fscore_support(y_true=actualResults, y_pred=predictedResults)
    accuracy = accuracy_score(y_true=actualResults, y_pred=predictedResults)

    print("the accuracy is :" + str(accuracy))
    print("Precision = " + str(precision))
    print("recall = " + str(recall))
    print("Fscore = " + str(Fscore))
    print("support = " + str(support))

#runs the main Machine Learning code with preparations using TensorFlow Framework (later)
#runs the main Machine Learning code with preparations using scikit-learn Framework (later)


concatFiles("dataset/negVPae.csv", "dataset/posVPae.csv","dataset/VPae.csv")
executeSKLearn("dataset/VPae.csv")


#meeting notes
#-------------
#PCA befor applying a classifier
#data normalization
#get rid of useless electrodes



