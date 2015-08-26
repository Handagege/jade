#!/usr/bin/python
# -*- coding: utf-8 -*-


class cliqueDataProcesser():
        def __init__(self,multiExpandCliqueList):
                self.nodeToCliqueData = []
                self.cliqueLengthData = []
                for i in multiExpandCliqueList:
                        self.nodeToCliqueData.append(self.getNodeToCliqueDic(i))
                        self.cliqueLengthData.append(self.getLengthDic(i))


        def getNodeToCliqueDic(self,cliqueList):
                ntc = {}
                for index,value in enumerate(cliqueList):
                        for i in value:
                                if i in ntc:
                                        ntc[i].add(index) 
                                else:
                                        ntc[i] = set([index])
                return ntc


        def getLengthDic(self,cliqueList):
                ld = {}
                for index,value in enumerate(cliqueList):
                        ld[index] = len(value)
                return ld


        def clearData(self):
                self.nodeToCliqueData = []
                self.cliqueLengthData = [] 


class edgeTemplate():
        '''
                根据挖掘出的关系圈数据，建立模板表示关注关系
                模板根据不同挖掘层次的关系圈，初步确定为俩维：
                第一维表示边（及关注关系）是否存在于同一个关系圈，1表示在，0表示不在
                第二维根据第一维的数据含义也不相同
                若边不在同一个关系圈，则第二维表示两点的位置关系，
                0表示两点均不在任何关系圈
                1表示有一点存在所属关系圈，另外一点不存在
                2表示两点均存在所属关系圈，也说明边是跨关系圈的
                若存在至少一个关系圈包含这条边，则第二维表示边所属的关系圈特征：
                由于考虑到关系圈的大小可以反应关系圈内的人的社交类型
                所以将利用所有包含该边的关系圈大小规模，计算均值和标准差作为第二维特征

                例：
                nodeA->nodeB ：[[0,1],[0,2],[1,8.4,5.2]]
                表示在种子团也就是第一次挖掘的关系圈中，
                该边不在任何关系圈且只有一个点在至少一个关系圈中，另外一个不在任何关系圈中
                在第二次挖掘的关系圈中，该边是跨关系圈的
                在第三次挖掘的关系圈中，该边存在于至少一个关系圈，且所在关系圈大小的均值为8.4，标准差为5.2
        '''
        
        
        joinFlagIndex = 0
        nodesPosRelFlagIndex = 1
        avgPos = 1
        stdDevPos = 2


        def __init__(self,cliqueDataProcesser):
                self.nodeToCliqueData = cliqueDataProcesser.nodeToCliqueData
                self.cliqueLengthData = cliqueDataProcesser.cliqueLengthData
                #self.edgeDic = cliqueDataProcesser.edgeDic
                #self.vertexsList = self.edgeDic.keys()


        def expressBatchEdge(self,edgeDic):
                self.expressVectorDic = {}
                for nodeA in edgeDic:
                        for nodeB in edgeDic[nodeA]:
                                expressVectorList = self.expressEdge(nodeA,nodeB)
                                key = str(nodeA) + '->' + str(nodeB)
                                self.expressVectorDic[key] = expressVectorList
                return self.expressVectorDic


        def expressEdge(self,nodeA,nodeB):
                expressVectorList = []
                for index,cliqueData in enumerate(self.nodeToCliqueData):
                        nodeAJoinedCliquesID = self.getCliquesIDWhoOwnNode(nodeA,index)
                        nodeBJoinedCliquesID = self.getCliquesIDWhoOwnNode(nodeB,index)
                        edgeJoinedCliquesID = self.getCliquesIDWhoOwnEdge(nodeA,nodeB,index)
                        feature = []
                        if not edgeJoinedCliquesID:
                                feature.append(0)
                                if nodeAJoinedCliquesID and nodeBJoinedCliquesID:
                                        feature.append(2)
                                elif nodeAJoinedCliquesID or nodeBJoinedCliquesID:
                                        feature.append(1)
                                else:
                                        feature.append(0)
                        else:
                                feature.append(1)
                                cliquesLengthList = self.getLengthListOfcliques(edgeJoinedCliquesID,index)
                                avg = self.calAvg(cliquesLengthList)
                                stdDev = self.calStdDev(cliquesLengthList,avg)
                                feature.append(avg)
                                feature.append(stdDev)
                        expressVectorList.append(feature)
                return expressVectorList
                                


        def getCliquesIDWhoOwnNode(self,node,iterNum):
                cliquesIDSet = self.nodeToCliqueData[iterNum].get(node,set())
                return cliquesIDSet


        def getLengthListOfcliques(self,cliquesID,iterNum):
                lengthList = []
                for i in cliquesID:
                        lengthList.append(self.cliqueLengthData[iterNum].get(i,0))
                return lengthList


        def getCliquesIDWhoOwnEdge(self,nodeA,nodeB,iterNum):
                cliquesIDSet = self.getCliquesIDWhoOwnNode(nodeA,iterNum) & self.getCliquesIDWhoOwnNode(nodeB,iterNum)
                return cliquesIDSet


        def calAvg(self,values):
                total = 0
                for i in values:
                        total += i
                return float(total)/float(len(values))


        def calStdDev(self,values,avg):
                total = 0.0
                for i in values:
                        total += (float(i) - avg)**2
                return (total/float(len(values)))**0.5


if __name__ == '__main__':
        l1 = [set([1,2,3]),set([3,4,5])]
        l2 = [set([1,2,3,4]),set([3,4,5])]
        l3 = [l1,l2]
        cdp = cliqueDataProcesser(l3)
        et = edgeTemplate(cdp)

        edgeDic = {1:set([2,3,4,5]),2:set([3,5]),3:set([4])}
        et.expressBatchEdge(edgeDic)

        for i in et.expressVectorDic:
                print i,et.expressVectorDic[i]

       # print cdp.nodeToCliqueData
       # print cdp.cliqueLengthData
       # print et.expressEdge(6,7)
       # print et.expressEdge(3,4)
        

