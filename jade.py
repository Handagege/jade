#!/data1/zhanghan/bin/bin
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from cliqueExpander import *
from bronkerbosch import *
from transToStdDataframe import *
from graphTool import *
import time


#根据关注关系列表获得被关注列表
def getFanNumDic(interestNumDic):
	pass

#取得单向连接关系
def getSimplexConnectDic(matrixValues):
	l = len(matrixValues)
	vertexList = range(0,l)
	simplexConnectDic = {}	
	for vertex_id_i in vertexList:
		simplexConnectList = []
		for vertex_id_j in vertexList:
			if matrixValues[vertex_id_i,vertex_id_j]:
				simplexConnectList.append(vertex_id_j+1)
		simplexConnectDic[vertex_id_i+1] = set(simplexConnectList)
	return simplexConnectDic

#取得双向连接关系
def getDuplexConnectDic(matrixValues):
	l = len(matrixValues)
	vertexList = range(0,l)
	duplexConnectDic = {}	
	#print(matrixValues)
	#print(matrixValues.T)
	for vertex_id_i in vertexList:
		duplexingConnectList = []
		for vertex_id_j in vertexList:
			if matrixValues[vertex_id_i,vertex_id_j] and matrixValues[vertex_id_j,vertex_id_i]:
				duplexingConnectList.append(vertex_id_j+1)
		duplexConnectDic[vertex_id_i+1] = set(duplexingConnectList)
	return duplexConnectDic
	
def readCsvToMatrix(fname='m.csv'):
	#第一行是列名,如果没有列名header=None	
	m = pd.read_csv(fname,delimiter=' ',header=None)
	return m.values

def removeSimpleClique(maximalCliqueList,minLen = 2):
	#tdata = maximalCliqueList.copy()
	removeList = []
	restList = []
	for c in maximalCliqueList:
		if len(c) < minLen:
			removeList.append(c)
		else:
			restList.append(c)

	return restList


def test1():
        #输入数据为矩阵形式

	#获得关注矩阵，转置后成为被关注矩阵
	mv = readCsvToMatrix()
	print(mv)
	#单向，双向关系字典(单向关系删除)
	interestDic = getSimplexConnectDic(mv)
	fanDic = getSimplexConnectDic(mv.T)
	duplexConnectDic = getDuplexConnectDic(mv)
	
	p = set(duplexConnectDic.keys())
	r = set()
	x = set()
	maximalCliqueList = []
	#发现极大团-利用枢纽点减少回溯次数的bk算法
	bronkerboschSimplePivot(p,r,x,duplexConnectDic,maximalCliqueList)
	

def test2():
        f = file('../input/followRel_10w.json')
        interestDic = json.load(f)
        interestDic = transKeyTypeToInt(interestDic)
        jade(interestDic)

def test3():
        interestDic = getFollowDicByFile('../input/coworkerFellowRel.data')
        jade(interestDic)

def jade(interestDic):
	#**************
        beg = time.time()
        print(len(interestDic))
	fanDic = getFanDicByFollowDic(interestDic)
	duplexConnectDic = getDuplexingDic(interestDic,fanDic)
	p = set(duplexConnectDic.keys())
	r = set()
	x = set()
	maximalCliqueList = []
        end = time.time()
        print "data prepare cost time : %0.2f"%(end-beg)
        beg1 = end
        #**************

	#发现极大团-利用枢纽点减少回溯次数的bk算法
        limitNodeInSeedNum = 24
	bronkerboschSimplePivot(p,r,x,duplexConnectDic,limitNodeInSeedNum,maximalCliqueList)
	print "maximal clique number : ",len(maximalCliqueList)
        end = time.time()
        print "maximal clique detect cost time : %0.2f"%(end-beg1)
        maxOverlapList,minOverlapList = getOverlapMeasures(maximalCliqueList) 
        #**************

        #团拓展
	ce = cliqueExpander(interestDic,fanDic,maximalCliqueList)
	#newCliqueList = ce.expand()
        #end = time.time()
        #print "total cost time : %0.2f"%(end-beg)
        #**************

        #结果数据处理
        f = open('../result/coworker_result_24_1w','w')
        for index, value in enumerate(maximalCliqueList):
                cl = map(str,value)
                f.write(str(index)+'    '+','.join(cl)+'\n')
        f.close()

        f = open('../result/coworker_measure_24_1w','w')
        for index, value in enumerate(maximalCliqueList):
		modularityOfOneClique = getMvalue(value,ce.m,ce.interestNumDic,ce.fanNumDic,interestDic)
                sIndex = str(index)+'--'
                sM = ' Mvalue : %.3f '%(modularityOfOneClique)
                sMaxOverlap = ' maxOverlap : %.3f '%(maxOverlapList[index])
                sMinOverlap = ' minOverlap : %.3f '%(minOverlapList[index])
                sLen = 'length : %d'%(len(value))
                f.write(sIndex+sM+sMaxOverlap+sMinOverlap+'\n')
        f.close() 

if __name__ == "__main__":
	test3()


