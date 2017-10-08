#-*- coding=utf-8 -*-
'''
1006
这个文件用于对某个点进行KNN实验 
它的本质就是计算这个点距离样本点的欧氏距离，之后进行排序取K个最近，然后进行比较大小。。。

'''
from numpy import *
import operator

def creatDataSet():
	group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
	labels = ['A','A','B','B']
	return group,labels

def classify0(inX, dataSet, lables, k):
	dataSetSize = dataSet.shape[0]
	print dataSetSize
	diffMat = tile(inX, (dataSetSize,1))-dataSet
	print tile(inX,(dataSetSize,1))-dataSet
	sqDiffMat = diffMat**2
	sqDistances = sqDiffMat.sum(axis=1)
	distances = sqDistances**0.5
	sortedDistIndicies =  distances.argsort()
	print sortedDistIndicies
	classCount = {}
	for i in range(k):
		voteILable = labels[sortedDistIndicies[i]]
		print voteILable
		classCount[voteILable] = classCount.get(voteILable,0)+1
		print classCount[voteILable]
	sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
	print sortedClassCount[0][0]
	return sortedClassCount[0][0]
group,labels = creatDataSet()
sortedClassCount = classify0([2,0], group,labels,3)
print sortedClassCount