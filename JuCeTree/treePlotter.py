# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt

decisionNode = dict(boxstyle='sawtooth', fc='0.6')
leafNode = dict(boxstyle='round4', fc='0.8')
arrow_args = dict(arrowstyle='<-')


def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt, textcoords='axes fraction', \
                            va='center', ha='center', bbox=nodeType, arrowprops=arrow_args)


# def createPlot():
#    fig = plt.figure(U'标题', figsize=(10, 5), facecolor='white')
#   fig.clf()
#   createPlot.ax1 = plt.subplot(111, frameon=False)
#   plotNode('decisionMakeNode', (0.5, 0.1), (0.1, 0.5), decisionNode)
#   plotNode('leafNode', (0.8, 0.1), (0.3, 0.8), leafNode)
#   plt.show()

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs


def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisType = 1 + getTreeDepth(secondDict[key])
        else:
            thisType = 1
        if thisType > maxDepth:
            maxDepth = thisType
    return maxDepth


def retrieveTree(i):
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                   {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}},
                                     3: {'body': {0: 'no', 1: 'yes'}}}},
                   {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}]
    return listOfTrees[i]


def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)


def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    print numLeafs
    depth = getTreeDepth(myTree)
    firstStr = myTree.keys()[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
    print (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW
    print cntrPt
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    # 下面这句话可以不要，不影响
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD


def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    # 如果axprops在createPlot.ax1函数中不使用的话，则画出的图就会有XY轴坐标显示
    axprops = dict(xticks=[], yticks=[])
    # 类似下面的变量定义的是全局变量
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = getNumLeafs(inTree)
    plotTree.totalD = getTreeDepth(inTree)
    plotTree.xOff = -0.5 / plotTree.totalW
    print plotTree.xOff
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()


if __name__ == '__main__':
    print '---------------------------------------------------'
    print retrieveTree(2)
    print getTreeDepth(retrieveTree(2))
    print '----------------------------------------------------'
    createPlot(retrieveTree(2))
