#!/usr/bin/python
# -*- coding: utf-8 -*-

from transToStdDataframe import *
import graphTool
import random


class dataIniter():
        def __init__(self,followRelFilePath,cliqueResultFilePath,dataType):
                #初始化关系数据
                if dataType == 'duplex':
                        self.initDuplexData(followRelFilePath)
                elif dataType == 'simplex':
                        self.initSimplexData(followRelFilePath)
                #初始化结果数据
                self.initCliqueResultData(cliqueResultFilePath)
                #根据原始数据得到一些统计数据
		self.interestNumDic = graphTool.getConnectNumDic(self.interestDic)
		self.fanNumDic = graphTool.getConnectNumDic(self.fanDic)
		self.m = graphTool.calTotalNumberEdges(self.interestDic)


        def initDuplexData(self,followRelFilePath):
                self.interestDic = getFollowDicByFile(followRelFilePath)
	        self.fanDic = getFanDicByFollowDic(self.interestDic)
	        self.duplexConnectDic = getDuplexingDic(self.interestDic,self.fanDic)
                self.interestDic = self.duplexConnectDic
                self.fanDic = self.duplexConnectDic


        def initSimplexData(self,followRelFilePath):
                #纯单向关系数据
                self.interestDic = getFollowDicByFile(followRelFilePath)
	        self.fanDic = getFanDicByFollowDic(self.interestDic)
                self.pureSimplexConnectDic = {}
                for i in self.interestDic:
                        self.pureSimplexConnectDic[i] = self.interestDic[i] ^ self.fanDic[i]
                        duplexConnectVertexs = self.interestDic[i] & self.fanDic[i]
                        self.interestDic[i] -= duplexConnectVertexs
                        self.fanDic[i] -= duplexConnectVertexs


        def initCliqueResultData(self,cliqueResultFilePath):
                self.cliqueList = []
                with open(cliqueResultFilePath,'r') as f:
                        for line in f:
                                strList = line.split(' : ')[1].split(',')
                                cliqueSet = set(map(int,strList))
                                self.cliqueList.append(cliqueSet)


class evaluater():
        def __init__(self,data):
                self.data = data


        def evaluateUid(self,uid):
                cliqueOwnUidDic = self.getCliqueByUid(uid)
                print '%d exit in %d clique'%(uid,len(cliqueOwnUidDic))
                mvalueDic = {}
                chosedDic = {}
                allNode = []
                for c in cliqueOwnUidDic:
                        mvalueDic[c] = graphTool.getMvalue(cliqueOwnUidDic[c],self.data.m,self.data.interestNumDic,\
                                self.data.fanNumDic,self.data.interestDic)
                        chosedNum = self.getChoseNum(len(cliqueOwnUidDic[c]))
                        chosedDic[c] = random.sample(list(cliqueOwnUidDic[c]),chosedNum)
                        allNode.extend(chosedDic[c])
                        #chosedDic[c] = set(chosedDic[c])
                allNode = set(allNode)
                print 'chosed %d node to evaluate'%(len(allNode))

                f = open('relNode_'+str(uid),'w')
                for n in allNode:
                        f.write(str(n)+'\n')
                f.close()

                f = open('cliqueMeasure_'+str(uid),'w')
                for c in mvalueDic:
                        s = '%d -- m value : %.6f -- chosed node : %s'%(c,mvalueDic[c],','.join(map(str,chosedDic[c])))
                        f.write(s+'\n')
                f.close()



        def getCliqueByUid(self,uid):
                count = 0
                cliqueOwnUidDic = {}
                for value in self.data.cliqueList:
                        if uid in value:
                                cliqueOwnUidDic[count] = value
                                count += 1
                return cliqueOwnUidDic        

        
        def getChoseNum(self,length):
                if length < 10:
                        return length
                num = int(float(length)*0.01)
                if num < 10:
                        return 10
                else:
                        return num


if __name__ == '__main__':
        relFilePath = '../input/coworkerFellowRel.data'
        resultFilePath = '../result/duplex_13/coworker_total_duplex_expand_0'
        dataType = 'duplex'
        di = dataIniter(relFilePath,resultFilePath,dataType)
        e = evaluater(di)
        e.evaluateUid(1824056637)

