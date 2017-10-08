#-*- coding=utf-8 -*-
from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt
def file2matrix(filename):
	fr = open(filename)
	arrayOLines = fr.readlines()
	numberOfLines = len(arrayOLines)
	returnMat = zeros((numberOfLines,3))
	classLabelVector = []
	index = 0
	for line in arrayOLines:
		line = line.strip()
		listFromLine = line.split('\t')
		returnMat[index,:] = listFromLine[0:3]
		classLabelVector.append(int(listFromLine[-1]))
		index += 1
	return returnMat,classLabelVector
def autoNorm(dataSet):
	minVals = dataSet.min(0)
	maxVals = dataSet.max(0)
	ranges = maxVals - minVals
	normDataSet = zeros(shape(dataSet))#norm 标准，规范
	m = dataSet.shape[0]
	normDataSet = dataSet - tile(minVals,(m,1))
	normDataSet = normDataSet/tile(ranges, (m,1))
	return normDataSet,ranges,minVals
def classify0(inX, dataSet, lables, k):
	dataSetSize = dataSet.shape[0]
	#print dataSetSize
	diffMat = tile(inX, (dataSetSize,1))-dataSet
	#print tile(inX,(dataSetSize,1))-dataSet
	sqDiffMat = diffMat**2
	sqDistances = sqDiffMat.sum(axis=1)
	distances = sqDistances**0.5
	sortedDistIndicies =  distances.argsort()
	#print sortedDistIndicies
	classCount = {}
	for i in range(k):
		voteILable = lables[sortedDistIndicies[i]]
		#print voteILable
		classCount[voteILable] = classCount.get(voteILable,0)+1
		#print classCount[voteILable]
	sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
	#print sortedClassCount[0][0]
	return sortedClassCount[0][0]
def datingClassTest():
	hoRatio = 0.10 #ratio 比例
	datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
	normMat,ranges,minVals = autoNorm(datingDataMat)
	m = normMat.shape[0]
	numTestVecs = int(m*hoRatio)
	errorCount = 0.0
	for i in range(numTestVecs):
		classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],5)
		print "come back %d,real %d",(classifierResult,datingLabels[i])
		if(classifierResult != datingLabels[i]):
			errorCount += 1.0
	print "error rate %f",(errorCount/float(numTestVecs))
datingClassTest()
'''
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(datingDataMat[:,0], datingDataMat[:,1],15.0*array(datingLabels),15.0*array(datingLabels))
plt.show()
'''