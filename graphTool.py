#!/data1/zhanghan/bin/bin
# -*- coding: utf-8 -*-

#计算单向链接数（出度、入度）
def getConnectNumDic(connectDic):
	connectNumDic = {}
	for i in connectDic:
		connectNumDic[i] = len(connectDic[i])
	return connectNumDic

#计算团内单向链接
def getConnectNumDicJoiningClique(c,connectDic):
	connectNumDic = {}
	for i in c:
		connectNumDic[i] = len(connectDic[i] & c)
	return connectNumDic
	
##########模块度指标M计算##########
#m : the total number of edges of the graph
#lc : the total number of edges joining vertices of module c
#dc : the sum of the degrees of the vertices of c

#计算m，根据单向关系词典
def calTotalNumberEdges(simplexConnectDic):
	m = 0
	for i in simplexConnectDic:
		m += len(simplexConnectDic[i])
	return m
	
#计算极大团lc,给定团内点数即可
#lc = n*(n-1)
#非极大团，要根据团内点之间的连接关系计算(calCliqueDegree)
def calLC_maximalClique(n):
	return float(n*(n-1))

def calLC(simplexDegreeDic):
	lc = 0
	for i in simplexDegreeDic:
		lc += simplexDegreeDic[i]
	return float(lc)
	
#计算DC用outDegreeDic,inDegreeDic
#参数outDegreeDic:interestNumDic关注数,inDegreeDic:fanNumDic粉丝数
def calDC(c,outDegreeDic,inDegreeDic,lc):
	cd = 0
	for i in c:
		cd += outDegreeDic[i]
		cd += inDegreeDic[i]
	return float(cd)-lc

#计算单团的模块度（Modularity）
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
