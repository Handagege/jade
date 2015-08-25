#!/data1/zhanghan/bin/bin
# -*- coding: utf-8 -*-

from cliqueExpander import *
from bronkerbosch import *
from transToStdDataframe import *
from graphTool import *
import time


def removeSimpleClique(maximalCliqueList,minLen = 2):
	#tdata = maximalCliqueList.copy()
	removeList = []
	restList = []
	for c in maximalCliqueList:
		if len(c) < minLen:
			removeList.append(c)
		else:
			restList.append(c)
        maximalCliqueList = []
	return restList


def test1():
        #全量数据集
        interestDic = getFollowDicByFile('../input/coworkerFellowRel.data')
	fanDic = getFanDicByFollowDic(interestDic)
	duplexConnectDic = getDuplexingDic(interestDic,fanDic)
        jade(interestDic,fanDic,duplexConnectDic,'../result/coworker_result_4_1w')


def test2():
        #纯双向关系数据
        interestDic = getFollowDicByFile('../input/coworkerFellowRel.data')
        fanDic = getFanDicByFollowDic(interestDic)
        duplexConnectDic = getDuplexingDic(interestDic,fanDic)
        jade(duplexConnectDic,duplexConnectDic,duplexConnectDic,6,'../result/coworker_total_duplex')


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
        jade(interestDic,fanDic,pureSimplexConnectDic,6,'../result/coworker_total_simplex')


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


def jade(interestDic,fanDic,duplexConnectDic,limitNodeInSeedNum,outPath):
	#**************
        beg = time.time()
        #print(len(interestDic))
	#p = set(duplexConnectDic.keys())
	#r = set()
	#x = set()
	#maximalCliqueList = []
        #**************

	#发现极大团-利用枢纽点减少回溯次数的bk算法
	#bronkerboschSimplePivot(p,r,x,duplexConnectDic,limitNodeInSeedNum,maximalCliqueList)
	#print "maximal clique number : ",len(maximalCliqueList)
        #end = time.time()
        #print "maximal clique detect cost time : %0.2f"%(end-beg)
        #**************

        seedCliqueList = []
        with open('../result/coworker_total_simplex') as f:
                for line in f:
                        line.rstrip('\n')
                        seedCliqueList.append(set(map(int,line.split(','))))
        #团拓展
	ce = cliqueExpander(interestDic,fanDic,seedCliqueList)
	newCliqueList = ce.expand()
        end = time.time()
        print "total cost time : %0.2f"%(end-beg)
        #**************

        #结果数据处理
        cliqueResult = newCliqueList
        #f = open(outPath,'w')
        #for index, value in enumerate(maximalCliqueList):
        #        cl = map(str,value)
        #        #f.write(str(index)+'    '+','.join(cl)+'\n')
        #        f.write(','.join(cl)+'\n')
        #f.close()

        f = open('../result/coworker_measure_simplex_1w','w')
        for index, value in enumerate(cliqueResult):
		modularityOfOneClique = getMvalue(value,ce.m,ce.interestNumDic,ce.fanNumDic,interestDic)
                sIndex = str(index)+'--'
                sl = ' length : %d '%(len(value))
                sM = ' Mvalue : %f '%(modularityOfOneClique)
                f.write(sIndex+sl+sM+'\n')
        f.close() 

if __name__ == "__main__":
        #test2()
	test3()
        #test4delOverlapClique()

