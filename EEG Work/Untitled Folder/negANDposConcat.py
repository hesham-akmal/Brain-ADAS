import os
import pandas as pd
import re
import sys
from sklearn.utils import shuffle

# concatenate +ve and -ve events files in one subject file


def concatFiles(file1Path, file2Path, desFilePath, shuffleIterations=1000):
    file1Content = pd.read_csv(file1Path)
    print("file1 shape :" + str(file1Content.shape))
    file2Content = pd.read_csv(file2Path)
    print("file2 shape :" + str(file2Content.shape))
    file1Content = file1Content.append(file2Content)
    print("Shuffling 1000 times the data, please wait ...")
    for i in range(shuffleIterations):
        file1Content = shuffle(file1Content)
    file1Content.to_csv(desFilePath, index=False)
    print("file3 shape :" + str(pd.read_csv(desFilePath).shape))
    print("file concatenation Is Complete Check the new File in " + desFilePath)


print("-----------------------------------------------------------------")
print("inFile1:->" + sys.argv[1])
file1 = sys.argv[1]
print("inFile2:->" + sys.argv[2])
file2 = sys.argv[2]
print("outFile:->" + sys.argv[3])
file3 = sys.argv[3]

if file1 == "" or file2 == "" or file3 == "":
    print("can't execute: file names are required")
# check that they are csv files
elif bool(re.match("([a-zA-Z0-9_])+(.csv)$", file1)) == False or \
        bool(re.match("([a-zA-Z0-9_])+(.csv)$", file2)) == False or \
        bool(re.match("([a-zA-Z0-9_])+(.csv)$", file3)) == False:
    print("Can't execute , regex doesn't match")
else:
    concatFiles(file1Path="dataset/" + file1,
                file2Path="dataset/" + file2,
                desFilePath="dataset/" + file3)
#    if sys.argv[4] == "1":
#        os.system("rm dataset/" + file1 + " dataset/" + file2)
print("-----------------------------------------------------------------")
