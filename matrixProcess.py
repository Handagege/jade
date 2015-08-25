import pandas as pd
import numpy as np



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
	
