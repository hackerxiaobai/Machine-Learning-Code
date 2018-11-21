#-*-encoding:utf8-*-
from numpy import *
import re
import feedparser
import operator

def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec

def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    #下面的意思是扩展成len（）长的全0列表
    returnVec = [0] * len(vocabList)
    #print returnVec
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print 'the word : %s is not in my vocabList!' %(word)
    return returnVec

def bagOfWords2Vec(vocabList, inputSet):
    #下面的意思是扩展成len（）长的全0列表
    returnVec = [0] * len(vocabList)
    #print returnVec
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        else:
            print 'the word : %s is not in my vocabList!' %(word)
    return returnVec

def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denmo = 2.0
    p1Denmo = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            #统计每个侮辱性词出现的次数
            p1Num += trainMatrix[i]
            #统计侮辱性词的总数
            p1Denmo += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denmo += sum(trainMatrix[i])
    p1Vect = log(p1Num / p1Denmo)
    p0Vect = log(p0Num / p0Denmo)
    return p0Vect, p1Vect, pAbusive

def classifierNB(vec2Classifier, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classifier * p1Vec) + log(pClass1)
    p0 = sum(vec2Classifier * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    if p1 < p0:
        return 0

def testingNB():
    postingList, classVec = loadDataSet()
    myVocabList = createVocabList(postingList)
    trainMat = []
    for postingDoc in postingList:
        trainMat.append(setOfWords2Vec(myVocabList, postingDoc))
    p0V, p1V, pAb = trainNB0(array(trainMat), array(classVec))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as:',classifierNB(thisDoc, p0V, p1V, pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as:', classifierNB(thisDoc, p0V, p1V, pAb)

def textParse(bigString):
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def spamTest():
    docList = []
    classList = []
    fullText = []
    for i in range(1, 26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50)
    testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])
        if classifierNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the erroe rate is :', float(errorCount) / len(testSet)

def calcMostFreq(vocabList, fullText):
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedFreq[:30]

def localWords(feed1, feed0):
    docList = []
    classList = []
    fullText = []
    minLen = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    top30Words = calcMostFreq(vocabList, fullText)
    for pairW in top30Words:
        if pairW[0] in top30Words:
            vocabList.remove(pairW[0])
    trainingSet = range(2*minLen)
    testSet = []
    for i in range(20):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del (trainingSet[randIndex])
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2Vec(vocabList, docList[docIndex])
        if classifierNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the erroe rate is :', float(errorCount) / len(testSet)
    return vocabList, p0V, p1V

def getTopWords(ny, sf):
    vocabList, p0V, p1V = localWords(ny, sf)
    topNY = []
    topSF = []
    for i in range(len(p0V)):
        if p0V[i] > -6.0:
            topSF.append((vocabList[i], p0V[i]))
        if p1V[i] > -6.0:
            topNY.append((vocabList[i], p1V[i]))
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)
    print 'SF***SF***SF***SF***SF***SF***SF***SF***SF***'
    for item in sortedSF:
        print item[0]
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
    print 'NY***NY***NY***NY***NY***NY***NY***NY***NY***'
    for item in sortedSF:
        print item[0]

if __name__ == '__main__':
    postingList, classVec = loadDataSet()
    myVocabList = createVocabList(postingList)
    print setOfWords2Vec(myVocabList, postingList[0])
    print '----------------------------------------------------'
    trainMat = []
    for postingDoc in postingList:
        trainMat.append(setOfWords2Vec(myVocabList, postingDoc))
    p0V, p1V, pAb = trainNB0(trainMat, classVec)
    print pAb
    print p0V
    print p1V
    print '-------------------------------------------------------'
    testingNB()
    print '--------------------------------------------------------'
    spamTest()
    print '---------------------------------------------------------'
    ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
    sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
    vocabList, pSF, pNF = localWords(ny, sf)
    print '-----------------------------------------------------------'
    getTopWords(ny, sf)