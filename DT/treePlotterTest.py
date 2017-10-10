#-*- coding=utf-8 -*-
'''
2017.10.09
机器学习实战 利用matplotlib绘制树形图
Author:george
'''
import matplotlib.pyplot as plt
#定义文本框和箭头格式
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle = "<-")

#绘制带箭头的注解
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
	createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',\
		xytext=centerPt, textcoords='axes fraction',\
		va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

def createPlot():
	fig = plt.figure(1, facecolor='white')
	fig.clf()
	createPlot.ax1 = plt.subplot(111,frameon=False)
	plotNode('decision node',(0.5,0.1),(0.1,0.5),decisionNode)
	plotNode('leaf node',(0.8,0.1),(0.3,0.8),leafNode)
	plt.show()
#获取叶子节点的个数
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
#获取树的深度
def getTreeDepth(myTree):
	maxDepth = 0 
	firstStr = myTree.keys()[0]
	secondDict = myTree[firstStr]
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			thisDepth = 1 + getTreeDepth(secondDict[key])
		else:
			thisDepth = 1 
		if thisDepth > maxDepth:
			maxDepth = thisDepth
	return maxDepth

#绘制决策树主函数
def plotMidText(cntrpt, parentPt, txtString):
	xMid = (parentPt[0] - cntrpt[0])/2.0 + cntrpt[0]
	yMid = (parentPt[1] - cntrpt[1])/2.0 + cntrpt[1]
	createPlot.ax1.text(xMid, yMid, txtString)

def plotTree(myTree, parentPt, nodeTxt):#if the first key tells you what feat was split on
    numLeafs = getNumLeafs(myTree)  #this determines the x width of this tree
    depth = getTreeDepth(myTree)
    firstStr = myTree.keys()[0]     #the text label for this node should be this
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes   
            plotTree(secondDict[key],cntrPt,str(key))        #recursion
        else:   #it's a leaf node print the leaf node
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)    #no ticks
    #createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses 
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(inTree, (0.5,1.0), '')
    plt.show()

def retrieveTree(i):
	listOfTrees = [{'no surfacing':{0:'no', 1:{'flippers':{0:'no',1:'yes'}}}}]
	return listOfTrees[i]

myTree = retrieveTree(0)

#myTree['no surfacing'][3] = 'maybe'
#createPlot(myTree)