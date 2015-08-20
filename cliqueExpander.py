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
                beg = time.time()
		cliqueDic,cliqueMvalueDic = self.getCliqueDic(self.seedCliqueList)
                end = time.time()
                print "calulate M clique's value cost : %0.2f"%(end-beg)
                beg = end
		#newCliqueList = self.expandClique(cliqueDic,cliqueMvalueDic)
                #end = time.time()
                #print "expand cliques cost : %0.2f"%(end-beg)
                #beg = end
		#cliqueDic,cliqueMvalueDic = self.getCliqueDic(newCliqueList)
		#newCliqueList = self.expandNode(cliqueDic,cliqueMvalueDic)
                #end = time.time()
                #print "expand node cost : %0.2f"%(end-beg)
		#cliqueDic,cliqueMvalueDic = self.getCliqueDic(newCliqueList)
		newCliqueList = self.expandNode(cliqueDic,cliqueMvalueDic)
                end = time.time()
                print "expand node cost : %0.2f"%(end-beg)
		return newCliqueList
	

	#依据团与团关系拓展
	def expandClique(self,cliqueDic,cliqueMvalueDic):
		cliqueKeyList = list(cliqueDic.keys())
		#print(type(cliqueKeyList))
		l = len(cliqueKeyList)
		newCliqueList = []
		waitedMergeCliqueDic = {}
		for index in range(0,l-1):
			waitedMergeNodeList = []
			for subIndex in range(index+1,l):
				if self.isMergeClique(cliqueKeyList[index],cliqueKeyList[subIndex],cliqueDic,cliqueMvalueDic):
					#print('True')
					if cliqueKeyList[index] in waitedMergeCliqueDic:
						waitedMergeCliqueDic[cliqueKeyList[index]].append(cliqueDic[cliqueKeyList[subIndex]])
					else:
						waitedMergeCliqueDic[cliqueKeyList[index]] = [cliqueDic[cliqueKeyList[subIndex]]]
					if cliqueKeyList[subIndex] in waitedMergeCliqueDic:
						waitedMergeCliqueDic[cliqueKeyList[subIndex]].append(cliqueDic[cliqueKeyList[index]])
					else:
						waitedMergeCliqueDic[cliqueKeyList[subIndex]] = [cliqueDic[cliqueKeyList[index]]]
		#print(waitedMergeCliqueDic)
		for ck in cliqueKeyList:
			expandClique = cliqueDic[ck].copy()
			expandClique = self.mergeClique(expandClique,waitedMergeCliqueDic.get(ck,set()))
			#print(expandClique)
			newCliqueList.append(expandClique)
                print ".......expand clique end......"
		return newCliqueList
	

	#依据团与点关系进行拓展
	def expandNode(self,cliqueDic,cliqueMvalueDic):
		cliqueConnectNodeDic = {}
		for c in cliqueDic:
			cliqueConnectNodeDic[c] = self.getConnectNodeOfClique(cliqueDic[c])
                #for c in cliqueConnectNodeDic:
                #        print "connect num: %d"%(len(cliqueConnectNodeDic[c]))
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
			cliqueMvalueDic[count] = graphTool.calModularityOfOneClique(self.m,lc,dc)
			count += 1
		return cliqueDic,cliqueMvalueDic
		
	#判断是否合并
	def isMergeClique(self,cliqueSeedKey,candidateCliqueKey,cliqueDic,cliqueMvalueDic):
		originMvalue1 = cliqueMvalueDic[cliqueSeedKey]
		originMvalue2 = cliqueMvalueDic[candidateCliqueKey]
		finalMvalue = self.getMvalue(cliqueDic[cliqueSeedKey]|cliqueDic[candidateCliqueKey])
		#print(cliqueSeedKey,' : ',cliqueDic[cliqueSeedKey],' - ',originMvalue1)
		#print(candidateCliqueKey,' : ',cliqueDic[candidateCliqueKey],' - ',originMvalue2)
		#print(finalMvalue)
		return finalMvalue > originMvalue1 and finalMvalue > originMvalue2

	def isMergeNode(self,key,node,cliqueDic,cliqueMvalueDic):
		originMvalue = cliqueMvalueDic[key]
		#finalClique = cliqueDic[cliqueSeedKey].copy()
		#finalClique.add(node)
		#finalMvalue = self.getMvalue(finalClique)
                finalMvalue = self.getMvalueByAdd(key,cliqueDic,node)
		return finalMvalue > originMvalue

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
                return M


	#团合并
	def mergeClique(self,c,cliqueList):
                temp = []
		for i in cliqueList:
			temp.extend(list(i))
                c = c | set(temp)
		return c
		
	#单结点合并
	def mergeNode(self,c,nodeList):
		for i in nodeList:
			c.add(i)
######################################
