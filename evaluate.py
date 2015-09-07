#!/usr/bin/python
# -*- coding: utf-8 -*-

from transToStdDataframe import *
import graphTool
import random
import dataTager
import operator


class dataIniter():
        def __init__(self,followRelFilePath,cliqueResultFilePath,tagDataPath,dataType):
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

                self.tagDataDic = dataTager.getTagData(tagDataPath) 
                self.nodeSet = set(self.tagDataDic.keys())
                self.tagSet = set()
                for i in self.tagDataDic:
                        self.tagSet.update(self.tagDataDic[i])


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
                self.tagClusterDic = {}


        def evaluateUid(self,uid):
                cliqueOwnUidDic = self.getCliqueByUid(uid)
                print '%d exit in %d clique'%(uid,len(cliqueOwnUidDic))
                mvalueDic = {}
                for c in cliqueOwnUidDic:
                        mvalueDic[c] = graphTool.getMvalue(cliqueOwnUidDic[c],self.data.m,self.data.interestNumDic,\
                                self.data.fanNumDic,self.data.interestDic)
                #获得倒排索引列表
                sortedList = self.getInvertedList(mvalueDic)
                
                tagShareRateDic = {}
                mostNumTagDic = {}
                length = 2
                for c in sortedList:
                        overlapNode = cliqueOwnUidDic[c] & self.data.nodeSet
                        mostNumTagList = self.getMostNumTags(overlapNode,length)
                        tagShareRateList = []
                        for i in range(0,len(mostNumTagList)):
                                tags = set(mostNumTagList[0:i+1])
                                tagShareRate = self.calShareRate(overlapNode,tags)
                                tagShareRateList.append(tagShareRate)
                        tagShareRateDic[c] = tagShareRateList
                        mostNumTagDic[c] = mostNumTagList
                avgShareRateList = self.calAvgShareRate(tagShareRateDic,length)
                #打印结果
                f = open('cliqueMeasure_'+str(uid),'w')
                for c in sortedList:
                        #s = '%d -- m value : %.6f -- chosed node : %s'%(c,mvalueDic[c],','.join(map(str,chosedDic[c])))
                        sm = '%d -- length : %d -- m value : %.6f --'%(c,len(cliqueOwnUidDic[c]),mvalueDic[c])
                        ss = ''
                        for i in range(0,length):
                                ss += ' %s : %.4f'%(mostNumTagDic[c][i],tagShareRateDic[c][i])
                        f.write(sm+ss+'\n')
                s = 'average share rate -- '
                for i in range(0,length):
                        s += ' %d tag : %.4f'%(i,avgShareRateList[i])
                f.write(s+'\n')
                f.close()


        def choseNodeByUid(self,uid):
                cliqueOwnUidDic = self.getCliqueByUid(uid)
                chosedDic = {}
                allNode = []
                for c in cliqueOwnUidDic:
                        chosedNum = self.getChoseNum(len(cliqueOwnUidDic[c]))
                        chosedDic[c] = random.sample(list(cliqueOwnUidDic[c]),chosedNum)
                        allNode.extend(chosedDic[c])
                        #chosedDic[c] = set(chosedDic[c])
                allNode = set(allNode)
                print 'chosed %d node to evaluate'%(len(allNode))

                f = open('relNode'+str(uid),'w')
                for n in allNode:
                        f.write(str(n)+'\n')
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


        def getInvertedList(self,dic,r=False):
                sortedList = sorted(dic.items(),key=operator.itemgetter(1),reverse=r)
                return map(operator.itemgetter(0),sortedList)


        def getMostNumTags(self,nodeSet,num=2):
                tagSizeDic = {}
                for n in nodeSet:
                        for tag in self.data.tagDataDic[n]:
                                if tag in tagSizeDic:
                                        tagSizeDic[tag] += 1
                                else:
                                        tagSizeDic[tag] = 1
                sortedList = self.getInvertedList(tagSizeDic,True)
                #print ','.join(sortedList)
                mostNumTagList = []
                count = 0
                while count < num:
                        mostNumTagList.append(sortedList[count])
                        count += 1
                return mostNumTagList


        def calShareRate(self,nodeSet,tags):
                l = len(nodeSet)
                shareNum = 0
                for n in nodeSet:
                        #if tag in self.data.tagDataDic[n]:
                        if tags & self.data.tagDataDic[n]:
                                shareNum += 1
                return float(shareNum)/float(l)


        def calAvgShareRate(self,tagShareRateDic,length=2):
                l = len(tagShareRateDic)
                avgShareRateList = [0.0]*length
                for i in tagShareRateDic:
                        for n in range(0,length):
                                avgShareRateList[n] += tagShareRateDic[i][n]
                for n in range(0,length):
                        avgShareRateList[n] = avgShareRateList[n]/float(l)
                return avgShareRateList


        def calAvgShareRateMostMClique(self,sortedList,tagShareRateDic,num,length=2):
                avgShareRateList = [0.0]*length
                count = 0
                while count < num:
                        for n in range(0,length):
                                avgShareRateList[n] += tagShareRateDic[sortedList[count]][n]
                for n in range(0,length):
                        avgShareRateList[n] = avgShareRateList[n]/float(l)
                return  avgShareRateList


if __name__ == '__main__':
        relFilePath = '../input/coworkerFellowRel.data'
        resultFilePath = '../result/coworker_total_duplex_expand_1'
        tagDataPath = '../input/1036663592_1_tag_done'
        dataType = 'duplex'
        di = dataIniter(relFilePath,resultFilePath,tagDataPath,dataType)
        e = evaluater(di)
        e.evaluateUid(1036663592)

