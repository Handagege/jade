#!/usr/bin/python
# -*- coding: utf-8 -*-


import graphTool
import time


class cliqueExpander():
	def __init__(self,interestDic,fanDic,seedCliqueList):
		self.interestDic = interestDic
		self.fanDic = fanDic
		self.interestNumDic = graphTool.getConnectNumDic(interestDic)
		self.fanNumDic = graphTool.getConnectNumDic(fanDic)
		self.m = graphTool.calTotalNumberEdges(interestDic)
		self.seedCliqueList = seedCliqueList

	
	def expand(self):
                mutiExpandCliqueList = []
                beg = time.time()
                print "seedCliqueList length : %d"%(len(self.seedCliqueList))
		newCliqueList = self.delOverlapCliqueNoShuffle(self.seedCliqueList,0.2)
                self.seedCliqueList = []
                mutiExpandCliqueList.append(newCliqueList)
                print "newCliqueList length : %d"%(len(newCliqueList))
                end = time.time()
                print "delete overlap cliques cost : %0.2f"%(end-beg)
                beg = end
		cliqueDic,cliqueMvalueDic = self.getCliqueDic(newCliqueList)
                end = time.time()
                print "calulate M clique's value cost : %0.2f"%(end-beg)
                beg = end
		newCliqueList = self.expandNode(cliqueDic,cliqueMvalueDic)
                mutiExpandCliqueList.append(newCliqueList)
                end = time.time()
                print "expand node cost : %0.2f"%(end-beg)
		return mutiExpandCliqueList


        def delOverlapCliqueNoShuffle(self,cliqueList,overlapLimitValue = 0.4):
                isMerged = True
                newCliqueList = cliqueList
                count = 0
                maxLengthDif = 2
                while isMerged:
                        count += 1
                        isMerged = False
                        l = len(newCliqueList)
                        print count,' iter length : ',len(newCliqueList)
                        tempCliqueList = []
                        removeSet = set()
                        for i in range(0,l-1):
                                maxOverlap = 0.0
                                maxIndex = 0
                                if i in removeSet:
                                        continue
                                li = len(newCliqueList[i])
                                for j in range(i+1,l):
                                        if j in removeSet:
                                                continue
                                        lj = len(newCliqueList[j])
                                        if abs(li-lj) > maxLengthDif:
                                                continue
                                        tempOverlap = self.calOverlap(newCliqueList[i],newCliqueList[j])
                                        if tempOverlap > maxOverlap:
                                                maxOverlap,maxIndex = tempOverlap,j
                                if maxOverlap >= overlapLimitValue:
                                        isMerged = True
                                        removeSet.add(maxIndex)
                                        tempCliqueList.append(newCliqueList[i] | newCliqueList[maxIndex])
				else:
					tempCliqueList.append(newCliqueList[i])
                        if l-1 not in removeSet:
                                tempCliqueList.append(newCliqueList[l-1])
                        newCliqueList = tempCliqueList
                return newCliqueList



        def delOverlapClique(self,cliqueList,overlapLimitValue = 0.4):
                isMerged = True
                newCliqueList = cliqueList
                count = 0
                while isMerged:
                        count += 1
                        isMerged = False
                        equilongCliquesList = self.shuffle(newCliqueList)
                        newCliqueList = []
                        for c in equilongCliquesList:
                                mergedCliqueList = []
                                if self.getMergedCliqueByOverlap(mergedCliqueList,c,overlapLimitValue):
                                        isMerged = True
                                newCliqueList.extend(mergedCliqueList)
                        print count,' iter length : ',len(newCliqueList)
                return newCliqueList
        
        
        #将同样大小的团放在一起
        def shuffle(self,cliqueList):
                equilongCliquesDic = {}
                for c in cliqueList:
                        l = len(c)
                        if equilongCliquesDic.has_key(l):
                                equilongCliquesDic[l].append(c)
                        else:
                                equilongCliquesDic[l] = [c]
                return equilongCliquesDic.values()


        def getMergedCliqueByOverlap(self,mergedCliqueList,originCliqueList,overlapLimitValue):
                removeList = []
                l = len(originCliqueList)
                isMerged = False
                for i in range(0,l-1):
                        maxOverlap = 0.0
                        maxIndex = 0
                        if i not in removeList:
                                for j in range(i+1,l):
                                        if originCliqueList[i] == originCliqueList[j]:
                                                removeList.append(j)
                                        else:
                                                tempOverlap = self.calOverlap(originCliqueList[i],originCliqueList[j])
                                                if tempOverlap > maxOverlap:
                                                        maxOverlap,maxIndex = tempOverlap,j
                                if maxOverlap >= overlapLimitValue:
                                        isMerged = True
                                        removeList.append(maxIndex)
                                        mergedCliqueList.append(originCliqueList[i] | originCliqueList[maxIndex])
                                else:
                                        mergedCliqueList.append(originCliqueList[i])
                if l-1 not in removeList:
                        mergedCliqueList.append(originCliqueList[l-1])
                return isMerged
                

	#依据团与点关系进行拓展
	def expandNode(self,cliqueDic,cliqueMvalueDic):
		cliqueConnectNodeDic = {}
		for c in cliqueDic:
			cliqueConnectNodeDic[c] = self.getConnectNodeOfClique(cliqueDic[c])
		newCliqueList = []
		for ck in cliqueDic:
			waitedMergeNodeList = []
			for node in cliqueConnectNodeDic[ck]:
				if self.isMergeNode(ck,node,cliqueDic,cliqueMvalueDic):
					waitedMergeNodeList.append(node)
			expandClique = cliqueDic[ck].copy()
			self.mergeNode(expandClique,waitedMergeNodeList)
			newCliqueList.append(expandClique)
		return newCliqueList
				

	#取得与团有联系的结点
	def getConnectNodeOfClique(self,clique):
		connectNodeSet = set()
		for c in clique:
			connectNodeSet = connectNodeSet | self.interestDic[c] | self.fanDic[c]
		return connectNodeSet-clique
		

	#将团编号并生成dic(原始数据、M值)
	def getCliqueDic(self,cliqueList):
		count = 1
		cliqueDic = {}
		cliqueMvalueDic = {}
                self.cliqueLCvalueDic = {}
                self.cliqueDCvalueDic = {}
		for i in cliqueList:
			cliqueDic[count] = i
                        interestNumInCliqueDic = graphTool.getConnectNumDicJoiningClique(i,self.interestDic)
                        lc = graphTool.calLC(interestNumInCliqueDic)
                        self.cliqueLCvalueDic[count] = lc
                        dc = graphTool.calDC(i,self.interestNumDic,self.fanNumDic,lc)
                        self.cliqueDCvalueDic[count] = dc
			cliqueMvalueDic[count] = graphTool.calModularityOfOneClique(self.m,lc,dc)/float(len(i))
			count += 1
		return cliqueDic,cliqueMvalueDic

		
	#判断是否合并
	def isMergeClique(self,cliqueSeedKey,candidateCliqueKey,cliqueDic,cliqueMvalueDic):
		originMvalue1 = cliqueMvalueDic[cliqueSeedKey]
		originMvalue2 = cliqueMvalueDic[candidateCliqueKey]
		finalMvalue = self.getMvalue(cliqueDic[cliqueSeedKey]|cliqueDic[candidateCliqueKey])
		return finalMvalue > originMvalue1 and finalMvalue > originMvalue2


	def isMergeNode(self,key,node,cliqueDic,cliqueMvalueDic):
		originMvalue = cliqueMvalueDic[key]
                finalMvalue = self.getMvalueByAdd(key,cliqueDic,node)
		return finalMvalue > originMvalue


        def isOverlap(self,cliqueA,cliqueB,threshold):
                overlapNum = len(cliqueA & cliqueB)
                al = len(cliqueA)
                bl = len(cliqueB)
                minLen = (al if al < bl else bl)
                defaultLen = 10
                if minLen < defaultLen:
                        minLen = defaultLen
                if float(overlapNum)/float(minLen) > threshold:
                        return True
                else:
                        return False
                

        def calOverlap(self,cliqueA,cliqueB):
                overlapNum = len(cliqueA & cliqueB)
                al = len(cliqueA)
                bl = len(cliqueB)
                minLen = (al if al < bl else bl)
                defaultLen = 10
                if minLen < defaultLen:
                        minLen = defaultLen
                return float(overlapNum)/float(minLen)
                

	#计算模块度M
	def getMvalue(self,clique):
		return graphTool.getMvalue(clique,self.m,self.interestNumDic,self.fanNumDic,self.interestDic)

	
        def getMvalueByAdd(self,seedKey,cliqueDic,node):
                oldLC = self.cliqueLCvalueDic[seedKey]
                oldDC = self.cliqueDCvalueDic[seedKey]
                clique = cliqueDic[seedKey]
                addLC = len(self.interestDic[node] & clique) + len(self.fanDic[node] & clique)
                addDC = len(self.interestDic[node]) + len(self.fanDic[node]) - addLC
                M = graphTool.calModularityOfOneClique(float(self.m),oldLC+addLC,oldDC+addDC)
                return M/float(len(clique)+1)


	#团合并
	def mergeClique(self,c,cliqueList):
                temp = []
		for i in cliqueList:
			temp.extend(list(i))
                c.update(set(temp))

		
	#单结点合并
	def mergeNode(self,c,nodeList):
                temp = []
		for i in nodeList:
			temp.append(i)
                c.update(set(temp))
######################################

def test4delOverlapClique():
        seedCliqueList = []
        with open('../result/coworker_') as f:
                for line in f:
                        line.rstrip('\n')
                        seedCliqueList.append(set(map(int,line.split(','))))
        ce = cliqueExpander({},{},seedCliqueList)
        newCliqueList = ce.expand()
        beg = time.time()
        #smax,smin = getMaxMinOverlap(seedCliqueList)
        #nmax,nmin = getMaxMinOverlap(newCliqueList)
        #print 'seedCliqueList overlap -- max : %.4f min : %.4f'%(smax,smin)
        #print 'newCliqueList overlap -- max : %.4f min : %.4f'%(nmax,nmin)
        getAvgOverlap(seedCliqueList)
        getAvgOverlap(newCliqueList)
        end = time.time()
        print 'cal overlap cost : %0.4f'%(end-beg)


def funcTest():
        s1 = set([1,2,3,4,5,6,7])
        s2 = set([3,4,5,6,7,8,9,10,23,45])
        s3 = set([4,7,11,13,15,17,56,55,67,77,88])
        s4 = set([3,4,5,6,7,8,9,10,23,55])
        s5 = set([45,56,78,98,34,43,67,89,99,32])
        s6 = set([6,7,8,9,10,23])
        seedCliqueList = [s1,s2,s3,s4,s5,s6]
        ce = cliqueExpander({},{},seedCliqueList)
        ce.delOverlapCliqueNoShuffle(seedCliqueList,0.5)


def writeCliqueListTofile(filePath,cliqueList):
        f = open(filePath,'w')
        for c in cliqueList:
                f.write(str(len(c))+' : '+','.join(map(str,c))+'\n')
        f.close()


def test1():
        seedCliqueList = []
        with open('../result/coworker_total_duplex_18') as f:
                count = 0
                for line in f:
                        count += 1
                        line.rstrip('\n')
                        seedCliqueList.append(set(map(int,line.split(','))))
        print len(seedCliqueList)
        ce = cliqueExpander({},{},seedCliqueList)
        beg = time.time()
        newCliqueList = ce.delOverlapCliqueNoShuffle(seedCliqueList,0.3)
        end = time.time()
        print "delete overlap cliques noshuffle cost : %0.2f"%(end-beg)
        beg = end
        newCliqueList = ce.delOverlapClique(seedCliqueList,0.3)
        end = time.time()
        print "delete overlap cliques cost : %0.2f"%(end-beg)
        #writeCliqueListTofile('../result/delOverlapClique',newCliqueList)
        


if __name__ == '__main__':
        #funcTest()
        test1()
