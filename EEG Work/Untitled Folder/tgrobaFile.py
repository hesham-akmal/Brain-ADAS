import numpy as np



x1=np.zeros([1,5])
print(x1)
print("-------------------")

x2=np.array([np.arange(1,6,1)])

print(x2)

print("-------------------")
x3=np.zeros([1,5])
print(x3)

print("-------------------")
y = np.append(x1,x2,axis=0)
print(y)


print("-------------------")
y = np.append(y,x3,axis=0)
print(y)



#File to try different pieces of codes and techniques

# # subjectsNames = ["VPae", "VPbad", "VPbax", "VPbba", "VPdx", "VPgaa", "VPgab", "VPgac", "VPgae", "VPgag", "VPgah", "VPgal", "VPgam", "VPih", "VPii", "VPja", "VPsaj", "VPsal"]
# subjectsNames = ["VPae.csv"]
# # # #
# #
# df = pd.read_csv("dataset/" + subjectsNames[0])
#
# df = df.head(2)
# print(df)
#
# df = df.drop(columns=['y'])
#
# print("=========================================================")
#
# numberOfElectrodes = 60
#
# finissh = 280
#
# nColToKeep = 200
#
# # for nColToKeep in range(280, finissh-20, -20):
# for i in range(1, numberOfElectrodes):
#     df = df.drop(df.columns[(i * nColToKeep):( (i * nColToKeep) + (300 - nColToKeep) )], axis=1)
# print("=========================================================")
# print(df.shape)
#
# for x in range(len(df.columns)):
#     print(df.columns[x])

# x = int(sys.argv[1])
#
# print(type(x))
#
# print("sys.argv[1] enetered is |"+str(x)+"|")

# nColToKeep = 60
# for i in range(1, numberOfElectrodes):
#     df = df.drop(df.columns[(i * nColToKeep):(280 + (i - 1) * nColToKeep)], axis=1)
#     print("=========================================================")
# for i in range(len(df.columns)):
#     print(df.columns[i])
# print(df.shape)

'''
x = np.loadtxt("arraykda.txt")
print(x)
print("=============")
print(x[:, 2])



# for fileIndex in range(len(subjectsNames)):
#     print("file " + subjectsNames[fileIndex] + " shape is " + str(pd.read_csv("dataset/" + subjectsNames[fileIndex]+".csv").shape))


# LRwithPCA = np.zeros(shape=(4, 3, 3), dtype=int)
#
# LRwithPCA[0, 0] = [100, 2, 3]
# LRwithPCA[0, 1] = [200, 8, 9]
# LRwithPCA[0, 2] = [300, 5, 6]
#
# LRwithPCA[1, 0] = [100, 12, 13]
# LRwithPCA[1, 1] = [200, 15, 16]
# LRwithPCA[1, 2] = [300, 18, 19]
#
# LRwithPCA[2, 0] = [100, 22, 23]
# LRwithPCA[2, 1] = [200, 25, 26]
# LRwithPCA[2, 2] = [300, 28, 29]
#
# LRwithPCA[3, 0] = [100, 32, 33]
# LRwithPCA[3, 1] = [200, 35, 36]
# LRwithPCA[3, 2] = [300, 38, 39]
#
# print("================")
# print("Original Matrix")
# print(LRwithPCA)
#
# print("================")
# print("matrix Transpose")
# x = LRwithPCA
# print(x)

# print("================")
# print("OPS")
# xx = np.max(x, axis=1)
# print(xx)
#
#

# #
# print("================")
# print("mean of all row")
# x = x.mean(axis=0, keepdims=True)
# print(x)

# print("================")
# print("mean of all col")
# x = LRwithPCA.mean(axis=1, keepdims=True)
# print(x)
# print("================")
# print("mean of all elements In a col")
# x = LRwithPCA.mean(axis=2, keepdims=True)
# print(x)

# print("================")
# print("mean of all elements in the first row , first col")
# x = LRwithPCA.mean(axis=(2,1,0), keepdims=True)
# print(x)

#
# x = -10
# #
# for x in range(x, 10):
#     print(x)
# print("-----------------------")
# print(x)
# #
# for x in range(x,0,-1):
#     print(x)
#
# print("-----------------------")
# print(x)
'''
