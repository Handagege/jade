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
	#print(m,lc,dc)
	modularityOfOneClique = calModularityOfOneClique(float(m),lc,dc)
	return modularityOfOneClique/float(len(clique))


def calCliqueOverlap(cliqueA,cliqueB,minLen):
        tempOverlap = float(len(cliqueA & cliqueB))/float(minLen)
        return tempOverlap


def getOverlapMeasures(cliqueList):
        l = len(cliqueList)
        maxOverlapList = []
        minOverlapList = []
        for i in range(0,l-1):
                overlapList = []
                for j in range(i+1,l):
                        a = len(cliqueList[i])
                        b = len(cliqueList[j])
                        minLen = (a if a < b else b)
                        tempOverlap = float(len(cliqueList[i] & cliqueList[j]))
                        overlapList.append(tempOverlap/float(minLen))
                maxOverlapList.append(max(overlapList))
                minOverlapList.append(min(overlapList))
        maxOverlapList.append(0)
        minOverlapList.append(0)
        return maxOverlapList,minOverlapList


def getAvgOverlap(cliqueList):
        l = len(cliqueList)
        overlap = 0.0
        total = 0
        for i in range(0,l-1):
                for j in range(i+1,l):
                        a = len(cliqueList[i])
                        b = len(cliqueList[j])
                        minLen = (a if a < b else b)
                        total += minLen
                        tempOverlap = float(len(cliqueList[i] & cliqueList[j]))
                        overlap += tempOverlap
        overlap = overlap/float(total)
        print "overlap weigting average : %f"%(overlap)
        return overlap


def getMaxMinOverlap(cliqueList):
        l = len(cliqueList)
        maxOverlapList = []
        minOverlapList = []
        for i in range(0,l):
                overlapList = []
                for j in range(0,l):
                        if i != j:
                                a = len(cliqueList[i])
                                b = len(cliqueList[j])
                                minLen = float(a if a < b else b)
                                tempOverlap = float(len(cliqueList[i] & cliqueList[j]))
                                overlapList.append(tempOverlap/minLen)
                maxOverlapList.append(max(overlapList))
                minOverlapList.append(min(overlapList))
        flag = True
        for i in maxOverlapList:
                if i == 1.0:
                        flag = False
        print flag
        avgMaxOverlap = avg(maxOverlapList)
        avgMinOverlap = avg(minOverlapList)
        return avgMaxOverlap,avgMinOverlap
        

def avg(list):
        total = 0.0
        for i in list:
                total += i
        return total/float(len(list))


##################################

if __name__ == '__main__':
        c = [set([1,2,3]),set([2,4,5,6])]
        maxo,mino = getMaxMinOverlap(c)
        print c
        print maxo,mino
