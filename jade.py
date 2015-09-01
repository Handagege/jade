#!/usr/bin/python
# -*- coding: utf-8 -*-

from cliqueExpander import *
from bronkerbosch import *
from transToStdDataframe import *
from graphTool import *
from edgeTemplate import *
import time


def showResult(outfilePath,cliqueResult):
        #结果数据处理
        #f = open(outPath,'w')
        #for index, value in enumerate(maximalCliqueList):
        #        cl = map(str,value)
        #        #f.write(str(index)+'    '+','.join(cl)+'\n')
        #        f.write(','.join(cl)+'\n')
        #f.close()

        f = open(outfilePath,'w')
        for index, value in enumerate(cliqueResult):
		modularityOfOneClique = getMvalue(value,ce.m,ce.interestNumDic,ce.fanNumDic,interestDic)
                sIndex = str(index)+'--'
                sl = ' length : %d '%(len(value))
                sM = ' Mvalue : %f '%(modularityOfOneClique)
                f.write(sIndex+sl+sM+'\n')
        f.close()


def test1():
        #全量数据集
        interestDic = getFollowDicByFile('../input/coworkerFellowRel.data')
	fanDic = getFanDicByFollowDic(interestDic)
	duplexConnectDic = getDuplexingDic(interestDic,fanDic)
        jade(interestDic,fanDic,duplexConnectDic,'../result/coworker_total_join')


def test2():
        #纯双向关系数据
        interestDic = getFollowDicByFile('../input/coworkerFellowRel.data')
        fanDic = getFanDicByFollowDic(interestDic)
        duplexConnectDic = getDuplexingDic(interestDic,fanDic)
        #jade(duplexConnectDic,duplexConnectDic,duplexConnectDic,6,'../result/coworker_total_duplex')
        jadeHadInitMaximalCliques(duplexConnectDic,duplexConnectDic,duplexConnectDic,'../result/coworker_total_duplex')


def test3():
        #纯单向关系数据
        interestDic = getFollowDicByFile('../input/coworkerFellowRel.data')
        fanDic = getFanDicByFollowDic(interestDic)
        pureSimplexConnectDic = {}
        for i in interestDic:
                pureSimplexConnectDic[i] = interestDic[i] ^ fanDic[i]
                duplexConnectVertexs = interestDic[i] & fanDic[i]
                interestDic[i] -= duplexConnectVertexs
                fanDic[i] -= duplexConnectVertexs
        #jade(interestDic,fanDic,pureSimplexConnectDic,12,'../result/coworker_total_simplex')
        jadeHadInitMaximalCliques(interestDic,fanDic,pureSimplexConnectDic,'../result/coworker_total_simplex')


def jade(interestDic,fanDic,duplexConnectDic,limitNodeInSeedNum,outPath):
        beg = time.time()
        print(len(interestDic))
	maximalCliqueList = []
	#发现极大团-利用枢纽点减少回溯次数的bk算法
        #**************
	findMaximalCliques(duplexConnectDic,limitNodeInSeedNum,maximalCliqueList)
	print "maximal clique number : ",len(maximalCliqueList)
        end = time.time()
        print "maximal clique detect cost time : %0.2f"%(end-beg)
        #**************

        #团拓展
        #**************
	ce = cliqueExpander(interestDic,fanDic,maximalCliqueList)
	mutiExpandCliqueList = ce.expand()
        #**************
        mutiExpandCliqueList.insert(0,maximalCliqueList)
        #边的模板表示
        #**************
        cdp = cliqueDataProcesser(mutiExpandCliqueList)
        et = edgeTemplate(cdp)
        et.expressBatchEdge(interestDic)
        #**************
        #showResult(outPath,newCliqueList)
        end = time.time()
        print "total cost time : %0.2f"%(end-beg)


def findMaximalCliques(duplexConnectDic,limitNodeInSeedNum,maximalCliqueList):
	p = set(duplexConnectDic.keys())
	r = set()
	x = set()
        bronkerboschSimplePivot(p,r,x,duplexConnectDic,limitNodeInSeedNum,maximalCliqueList)
        

def writeCliqueListTofile(filePath,cliqueList):
        f = open(filePath,'w')
        for c in cliqueList:
                f.write(str(len(c))+' : '+','.join(map(str,c))+'\n')
        f.close()


def jadeHadInitMaximalCliques(interestDic,fanDic,duplexConnectDic,outPath):
        beg = time.time()
        print(len(interestDic))
        seedCliqueList = []
        with open('../result/coworker_total_simplex_9') as f:
                for line in f:
                        line.rstrip('\n')
                        seedCliqueList.append(set(map(int,line.split(','))))
        #团拓展
	ce = cliqueExpander(interestDic,fanDic,seedCliqueList)
	mutiExpandCliqueList = ce.expand()
        #**************

        for i,value in enumerate(mutiExpandCliqueList):
                competeOutPath = outPath + '_expand_' + str(i)
                writeCliqueListTofile(competeOutPath,value)
        #边的模板表示
        #**************
        #cdp = cliqueDataProcesser(mutiExpandCliqueList)
        #et = edgeTemplate(cdp)
        #et.expressBatchEdge(interestDic)
        #**************
        #showResult(outPath,newCliqueList)
        
        end = time.time()
        print "total cost time : %0.2f"%(end-beg)


if __name__ == "__main__":
        #test2()
	test3()
