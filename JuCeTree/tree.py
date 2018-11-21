from math import log
import operator
import treePlotter

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCount = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCount.keys():
            labelCount[currentLabel] = 0
        labelCount[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCount:
        prob = float(labelCount[key])/numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reduceFeatVec = featVec[:axis]
            reduceFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reduceFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def selectNumMaxLabel(labelList):
    labelCount = {}
    for feat in labelList:
        if feat not in labelCount.keys():
            labelCount[feat] = 0
        labelCount[feat] += 1
    sortedLabelCount = sorted(labelCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedLabelCount[0][0]

def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return selectNumMaxLabel(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del(labels[bestFeat])
    featValue = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValue)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree

def classifier0(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    labelIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[labelIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classifier0(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

def lensesTest():
    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
    lensesTree = createTree(lenses, lensesLabels)
    treePlotter.createPlot(lensesTree)

def add(x):
    if x<=3:
        return 1
    else:
        return add(x-2) + add(x-4) +1

if __name__ == '__main__':
    # dataSet, labels = createDataSet()
    # print calcShannonEnt(dataSet)
    # print '---------------------------------------------------'
    # print splitDataSet(dataSet, 0, 1)
    # print '---------------------------------------------------'
    # print chooseBestFeatureToSplit(dataSet)
    # print '----------------------------------------------------'
    # print createTree(dataSet, labels)
    # print '----------------------------------------------------'
    # myTree = treePlotter.retrieveTree(0)
    # dataSet, labels = createDataSet()
    # print classifier0(myTree, labels, [1, 0])
    # print '-----------------------------------------------------'
    # storeTree(myTree, 'classifierStorage.txt')
    # print grabTree('classifierStorage.txt')
    # print '-----------------------------------------------------'
    # lensesTest()

    print add(8)