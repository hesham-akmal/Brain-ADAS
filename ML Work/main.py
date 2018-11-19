from sklearn.linear_model import LogisticRegression  # Logisitic Regression model
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis  # LDA model
from sklearn.model_selection import train_test_split  # to obtain train and test datasets for the same file
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import pandas as pd
import pandas.api.types as ptypes
from sklearn.decomposition import PCA

import tensorflow as tf

tf.enable_eager_execution()

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# def prepareDataTF(fileNameOrPath):
#     # read file data ( subject file )
#     FileContent = pd.read_csv(fileNameOrPath).head(4)
#     # randomize the order of data
#
#     print(FileContent.shape)
#     print(FileContent)
#     print(FileContent.values)
#
#     featuresColumns = FileContent.columns[0:len(FileContent.columns) - 1]
#     labelsColumn = FileContent.columns[len(FileContent.columns) - 1]
#
#     print(featuresColumns)
#     print(labelsColumn)
#
#     training_dataset = (tf.data.Dataset.from_tensor_slices((tf.cast(FileContent[featuresColumns].values, tf.float32),tf.cast(FileContent[labelsColumn].values, tf.string))))
#     #
#     # for features_tensor, target_tensor in training_dataset:
#     #     print("features:{"+str(features_tensor)+"} target:{"+str(target_tensor)+"}")
#
#     print(training_dataset[0])

# my_columns = []
#
# for col in FileContent.columns:
#     if ptypes.is_string_dtype(FileContent[col]):  # is_string_dtype is pandas function
#         my_columns.append(tf.feature_column.categorical_column_with_hash_bucket(col,hash_bucket_size=len(FileContent[col].unique())))
#
#     elif ptypes.is_numeric_dtype(FileContent[col]):  # is_numeric_dtype is pandas function
#         my_columns.append(tf.feature_column.numeric_column(col))
#
#
# return trainingFeatures, trainingLabels, testFeatures, actualResults, my_columns


def prepareDataSKLearn(fileNameOrPath):
    # read file data ( subject file )
    FileContent = pd.read_csv(fileNameOrPath)
    # randomize the order of data
    FileContent = shuffle(FileContent)
    # get features and labels
    featuresColumns = FileContent.columns[0:len(FileContent.columns) - 1]
    labelsColumn = FileContent.columns[len(FileContent.columns) - 1]
    trainingFeaturesX = FileContent.loc[:, featuresColumns]
    trainingLabely = FileContent.loc[:, labelsColumn]
    # split the data into training and test
    trainingFeatures, testFeatures, trainingLabels, actualResults = train_test_split(trainingFeaturesX, trainingLabely,test_size=0.33, random_state=42)
    return trainingFeatures, trainingLabels, testFeatures, actualResults


def printResultsSklearn(actualResults, predictedResults):
    print("\nResults:-")
    precision, recall, Fscore, support = precision_recall_fscore_support(y_true=actualResults, y_pred=predictedResults)
    accuracy = accuracy_score(y_true=actualResults, y_pred=predictedResults)
    print("accuracy =" + str(accuracy))
    print("Precision=" + str(precision))
    print("recall   =" + str(recall))
    print("Fscore   =" + str(Fscore))
    print("support  =" + str(support))


# runs the main Machine Learning code with preparations using scikit-learn Framework
def LDAclassification(traningFeatures, trainingLabels, testFeatures, actualResults):
    print("---Creating Linear Discriminant Analyzer---")
    LDAClassifier = LinearDiscriminantAnalysis()
    # training the model
    print("Training ..")
    LDAClassifier.fit(traningFeatures, trainingLabels)
    # testing the model
    print("Testing ....")
    predictedResults = LDAClassifier.predict(testFeatures)
    # making calcuations and evaluations
    print("Parameters trained:\n")
    print(str(LDAClassifier.coef_[0]))
    printResultsSklearn(actualResults=actualResults, predictedResults=predictedResults)
    print("---Finished LDA---\n")


def LRClassification(traningFeatures, trainingLabels, testFeatures, actualResults):
    print("---Creating Logistic Regressor---")
    LogisticRegressionClassifier = LogisticRegression()
    # training the model
    print("Training ..")
    LogisticRegressionClassifier.fit(traningFeatures, trainingLabels)
    # testing the model
    print("Testing ....")
    predictedResults = LogisticRegressionClassifier.predict(testFeatures)
    # making calcuations and evaluations
    print("Parameters trained:\n")
    print(str(LogisticRegressionClassifier.coef_[0]))
    printResultsSklearn(actualResults=actualResults, predictedResults=predictedResults)
    print("---Finished Logistic Regression---")


def executeSKLearnModels(trainingFeatures, trainingLabels, testFeatures, actualResults):
    LRClassification(trainingFeatures, trainingLabels, testFeatures, actualResults)
    LDAclassification(trainingFeatures, trainingLabels, testFeatures, actualResults)


def executeSKLearnModelsPCA(traningFeatures, trainingLabels, testFeatures, actualResults):
    print("----------")
    print("AFTER PCA")
    print("----------")
    
    scaler = StandardScaler()
    # Fit on training set only.
    scaler.fit(traningFeatures)
    # Apply transform to both the training set and the test set.
    train_img = scaler.transform(traningFeatures)
    test_img = scaler.transform(testFeatures)

    pca = PCA(.95)
    pca.fit(train_img)
    PCA_training_features = pca.transform(train_img)
    PCA_testing_features = pca.transform(test_img)

    LRClassification(PCA_training_features, trainingLabels, PCA_testing_features, actualResults)
    LDAclassification(PCA_training_features, trainingLabels, PCA_testing_features, actualResults)


# def executeTensorFlowModel(traningFeatures, trainingLabels, testFeatures, actualResults, featuresCol):
#     LinearRegressorTF = tf.estimator.LinearClassifier(feature_columns=featuresCol)
#     pass


# runs the main Machine Learning code with preparations using scikit-learn Framework
trainingFeatures, trainingLabels, testFeatures, actualResults = prepareDataSKLearn("dataset/VPae.csv")
executeSKLearnModels(trainingFeatures, trainingLabels, testFeatures, actualResults)
executeSKLearnModelsPCA(trainingFeatures, trainingLabels, testFeatures, actualResults)

# runs the main Machine Learning code with preparations using TensorFlow Framework

# trainingFeatures, trainingLabels, testFeatures, actualResults, my_columns = prepareDataTF("dataset/VPae.csv")
# prepareDataTF("dataset/VPae.csv")

# executeTensorFlowModel(trainingFeatures, trainingLabels, testFeatures, actualResults, my_columns )

# meeting notes
# -------------
# PCA before applying a classifier (X)
# data normalization X
# get rid of useless electrodes
