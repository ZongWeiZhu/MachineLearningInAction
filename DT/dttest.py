#-*- coding=utf-8 -*-
'''
2017.10.07
机器学习实战 决策树实验
Author:george
'''
from math import log
import operator 
#计算给定数据的香农熵
def calcShannonEnt(dataSet):
	numEntries = len(dataSet)
	labelCounts = {}
	for featVec in dataSet:
		currentLabel = featVec[-1]
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel] = 0
		labelCounts[currentLabel] += 1
	shannonEnt = 0.0
	for key in labelCounts:
		prob = float(labelCounts[key])/numEntries
		shannonEnt -= prob*log(prob,2)
	return shannonEnt

#自定义生成数据
def creatDataSet():
	dataSet = [[1,1,'yes'],
			[1,1,'yes'],
			[1,0,'no'],
			[0,1,'no'],
			[0,1,'no']]
	labels = ['no surfacing','flippers']
	return dataSet,labels 

#划分数据集
#返回 第几维数据axis等于value 的不包含该维的子集
def splitDataSet(dataSet, axis, value):
	retDataSet = []
	for featVec in dataSet:
		if featVec[axis] == value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis+1:])
			retDataSet.append(reducedFeatVec)
	return retDataSet

#选择信息熵最好的特征进行划分
def chooseBestFeatureSplit(dataSet):
	numFeature = len(dataSet[0])-1
	baseEntropy = calcShannonEnt(dataSet)
	bestInfoGain = 0.0; bestFeature = -1
	for i in range(numFeature):
		featList = [example[i] for example in dataSet] #把第i维的数据存进lIST中
		#print featList
		uniqueVals = set(featList)
		#print uniqueVals
		newEntropy = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob*calcShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy
		if(infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeature = i
	return bestFeature

#majority 多数 reverse 相反
def majorityCnt(classList):
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys():
			classCount[vote] = 0
		classCount += 1
	sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
	return sortedClassCount[0][0]
#创建决策树
def createTree(dataSet,labels):
	classList = [example[-1] for example in dataSet]
	if classList.count(classList[0]) == len(classList):
		return classList[0]
	if len(dataSet) == 1:
		return majorityCnt(classList)
	bestFeat = chooseBestFeatureSplit(dataSet)
	bestFeatLabel = labels[bestFeat]
	myTree = {bestFeatLabel:{}}
	del(labels[bestFeat])
	featValues = [example[bestFeat] for example in dataSet]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:]
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels)

	return myTree
def classify(inputTree, featLabels, testVec):
	firstStr = inputTree.keys()[0]
	secondDict = inputTree[firstStr]
	featIndex = featLabels.index(firstStr)
	print "featIndex",featIndex
	for key in secondDict.keys():
		if testVec[featIndex] == key:
			if type(secondDict[key]).__name__ == 'dict':
				classLabel = classify(secondDict[key],featLabels,testVec)
			else:
				classLabel = secondDict[key]
	return classLabel
def retrieveTree(i):
	listOfTrees = [{'no surfacing':{0:'no', 1:{'flippers':{0:'no',1:'yes'}}}}]
	return listOfTrees[i]

#存储决策树
def storeTree(inputTree,filename):
	import pickle
	fw = open(filename,'w')
	pickle.dump(inputTree,fw)
	fw.close()

#取出决策树
def grabTree(filename):
	import pickle
	fr = open(filename)
	return pickle.load(fr)


dataSet,labels = creatDataSet()
#print labels
#print calcShannonEnt(dataSet)
#print splitDataSet(dataSet,0,0)
#print "best feature",chooseBestFeatureSplit(dataSet)
myTree = createTree(dataSet,labels)
#myTree = retrieveTree(0)
#storeTree(myTree,'decisionTree.txt')
print grabTree('decisionTree.txt')
#print "labels",labels
#classLabels = classify(myTree, labels, [1,0])
#print "classLabels",classLabels