#!/data1/zhanghan/bin/bin
# -*- coding: utf-8 -*-

#���㵥�������������ȡ���ȣ�
def getConnectNumDic(connectDic):
	connectNumDic = {}
	for i in connectDic:
		connectNumDic[i] = len(connectDic[i])
	return connectNumDic

#�������ڵ�������
def getConnectNumDicJoiningClique(c,connectDic):
	connectNumDic = {}
	for i in c:
		connectNumDic[i] = len(connectDic[i] & c)
	return connectNumDic
	
##########ģ���ָ��M����##########
#m : the total number of edges of the graph
#lc : the total number of edges joining vertices of module c
#dc : the sum of the degrees of the vertices of c

#����m�����ݵ����ϵ�ʵ�
def calTotalNumberEdges(simplexConnectDic):
	m = 0
	for i in simplexConnectDic:
		m += len(simplexConnectDic[i])
	return m
	
#���㼫����lc,�������ڵ�������
#lc = n*(n-1)
#�Ǽ����ţ�Ҫ�������ڵ�֮������ӹ�ϵ����(calCliqueDegree)
def calLC_maximalClique(n):
	return float(n*(n-1))

def calLC(simplexDegreeDic):
	lc = 0
	for i in simplexDegreeDic:
		lc += simplexDegreeDic[i]
	return float(lc)
	
#����DC��outDegreeDic,inDegreeDic
#����outDegreeDic:interestNumDic��ע��,inDegreeDic:fanNumDic��˿��
def calDC(c,outDegreeDic,inDegreeDic,lc):
	cd = 0
	for i in c:
		cd += outDegreeDic[i]
		cd += inDegreeDic[i]
	return float(cd)-lc

#���㵥�ŵ�ģ��ȣ�Modularity��
def calModularityOfOneClique(m,lc,dc):
	return lc/(2.0*m) - (dc/(2.0*m))**2
	
def getMvalue(clique,m,interestNumDic,fanNumDic,interestDic):
	interestNumInCliqueDic = getConnectNumDicJoiningClique(clique,interestDic)
	lc = calLC(interestNumInCliqueDic)
	dc = calDC(clique,interestNumDic,fanNumDic,lc)
#	print(m,lc,dc)
	modularityOfOneClique = calModularityOfOneClique(float(m),lc,dc)
	return modularityOfOneClique


def calCliqueOverlap(cliqueA,cliqueB):
        a = len(cliqueA)
        b = len(cliqueB)
        min = (a if a < b else b)
        tempOverlap = float(len(cliqueA & cliqueB))/float(min)
        return tempOverlap


def getOverlapMeasures(cliqueList):
        overlapMeasureList = []
        count = 0
        l = len(cliqueList)
        overlap = 0.0
        total = 0
        maxOverlapList = []
        minOverlapList = []
        for i in range(0,l-1):
                overlapList = []
                for j in range(i+1,l):
                        a = len(cliqueList[i])
                        b = len(cliqueList[j])
                        minLen = (a if a < b else b)
                        total += minLen
                        tempOverlap = float(len(cliqueList[i] & cliqueList[j]))
                        overlap += tempOverlap
                        overlapList.append(tempOverlap/float(minLen))
                maxOverlapList.append(max(overlapList))
                minOverlapList.append(min(overlapList))
        overlap = overlap/float(total)
        maxOverlapList.append(0)
        minOverlapList.append(0)
        print "overlap weigting average : %f"%(overlap)
        return maxOverlapList,minOverlapList

##################################
