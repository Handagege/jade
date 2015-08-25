import pandas as pd
import numpy as np



#ȡ�õ������ӹ�ϵ
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

#ȡ��˫�����ӹ�ϵ
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
	#��һ��������,���û������header=None	
	m = pd.read_csv(fname,delimiter=' ',header=None)
	return m.values


def test1():
        #��������Ϊ������ʽ
	#��ù�ע����ת�ú��Ϊ����ע����
	mv = readCsvToMatrix()
	print(mv)
	#����˫���ϵ�ֵ�(�����ϵɾ��)
	interestDic = getSimplexConnectDic(mv)
	fanDic = getSimplexConnectDic(mv.T)
	duplexConnectDic = getDuplexConnectDic(mv)
	p = set(duplexConnectDic.keys())
	r = set()
	x = set()
	maximalCliqueList = []
	#���ּ�����-������Ŧ����ٻ��ݴ�����bk�㷨
	bronkerboschSimplePivot(p,r,x,duplexConnectDic,maximalCliqueList)
	
