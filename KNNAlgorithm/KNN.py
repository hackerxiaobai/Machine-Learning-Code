from numpy import *
import operator
from os import listdir

def createDataSet():
    groups = array([[1.0, 1.1], [1.0, 1.0], [0., 0.], [0., 0.1]])
    lables = ['A', 'A', 'B', 'B']
    return groups, lables

def classify0(inX, groups, lables, key):
    dataSetSize = groups.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - groups
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    # print (sortedDistIndicies)
    classCount = {}
    for i in range(key):
        voteLable = lables[sortedDistIndicies[i]]
        # print (voteLable)
        classCount[voteLable] = classCount.get(voteLable, 0) + 1
        # print classCount
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr = open(filename)
    arrayOfLines = fr.readlines()
    numberOfLines = len(arrayOfLines)
    returnMat = zeros((numberOfLines, 3))
    classLableVertor = []
    index = 0
    for line in arrayOfLines:
        line = line.strip()
        listFormLine = line.split('\t')
        returnMat[index, :] = listFormLine[0:3]
        classLableVertor.append(int(listFormLine[-1]))
        index += 1
    fr.close()
    return returnMat, classLableVertor

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet/tile(ranges, (m, 1))
    # print minVals,maxVals
    return normDataSet, ranges, minVals

def datingClassTest():
    hoRatio = 0.10
    datingDataMat, datingDataLables = file2matrix('datingTestSet2.txt')
    normDataSet, ranges, minVals = autoNorm(datingDataMat)
    m = normDataSet.shape[0]
    numTestvecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestvecs):
        classifierResult = classify0(normDataSet[i, :], normDataSet[numTestvecs:m, :],
                                     datingDataLables[numTestvecs:m], 3)
        print ('the classifier came back with:  %d, the real answer is:  %d'%(classifierResult, datingDataLables[i]))
        if(classifierResult != datingDataLables[i]):
            errorCount+=1.0
    print ('the total error rate is:  %f'%(errorCount/float(numTestvecs)))
    print errorCount

def classifyPerson():
    resultList = ['not at all', 'in small does', 'in large does']
    percentTats = float(raw_input('percentage of time spent playing video games:'))
    ffMiles = float(raw_input('frequent flier miles earned per year:'))
    iceCream = float(raw_input('liters of ice cream consumed per year:'))
    datingDataMat, datingDataLables = file2matrix('datingTestSet2.txt')
    normDataSet, ranges, minVals = autoNorm(datingDataMat)
    inX = array([ffMiles, percentTats, iceCream])
    classfierResult = classify0((inX-minVals)/ranges, normDataSet, datingDataLables, 3)
    print'You will probably like this person:', resultList[classfierResult - 1]

def img2vector(filename):
    returnVect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        line = fr.readline()
        for j in range(32):
            returnVect[0, 32*i+j] = int(line[j])
    return returnVect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i, :] = img2vector('trainingDigits/%s'%(fileNameStr))
    testFileList = listdir('testDigits')
    mTest = len(testFileList)
    errorCount = 0.0
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorTest = img2vector('testDigits/%s'%(fileNameStr))
        classifierResult = classify0(vectorTest, trainingMat, hwLabels, 3)
        print 'the classifier came back with: %d, the real answer is %d'%(classifierResult, classNumStr)
        if(classifierResult != classNumStr):
            errorCount+=1.0
    print '\n the total number of errors is %d'%(errorCount)
    print '\n the total error rate is %f'%(errorCount/float(mTest))

if __name__ == '__main__':
    groups, lables = createDataSet()
    print classify0([1.9, 1.8], groups, lables, 3)
    print '---------------------------------------------------------------------'
    datingClassTest()
    print '---------------------------------------------------------------------'
    classifyPerson()
    print '---------------------------------------------------------------------'
    handwritingClassTest()
