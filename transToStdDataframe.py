# -*- coding: utf-8 -*-


import json


def getFollowDicByFile(filePath):
        followDic = {}
        with open(filePath) as f:
                for line in f:
                        splitList = line.split('\t')
                        uidKey = int(splitList[0])
                        followUidsStr = splitList[1]
                        try:
                                if followUidsStr == '\n':
                                        followUids = set()
                                else:
                                        followUids = set(map(int,followUidsStr.split(',')))
                        except ValueError:
                                print followUidsStr.split(',')
                                exit()
                        followDic[uidKey] = followUids
        return followDic


def getFollowDicByNoFilterFile(filePath):
        followDic = {}
        count = 0
        with open(filePath) as f:
                for line in f:
                        count += 1
                        splitList = line.split('\t')
                        uidKey = int(splitList[0])
                        followUidsStr = splitList[1]
                        try:
                                if followUidsStr == '\n':
                                        followUids = set()
                                else:
                                        followUids = set(map(int,followUidsStr.split(',')))
                        except ValueError:
                                print followUidsStr.split(',')
                                print count
                                exit()
                        followDic[uidKey] = followUids
        uidSet = set(followDic.keys())
        for i in followDic:
                followDic[i] = followDic[i] & uidSet
        return followDic


def getFanDicByFollowDic(followDic):
        fanDic = {}
        for u in followDic:
                fanDic[u] = set()
        for u in followDic:
                for followUid in followDic[u]:
                        fanDic[followUid].add(u)
        return fanDic


def getDuplexingDic(followDic,fanDic):
        duplexingDic = {}
        for u in followDic:
                duplexingDic[u] = set()
        for u in followDic:
                duplexingDic[u] = followDic[u] & fanDic[u]
        return duplexingDic


def checkoutIntegrity(relDic):
        flag = True
        for u in relDic:
                for i in relDic[u]:
                        result = relDic.get(i,None)
                        if result == None:
                                print(i)
                                flag = False
        return flag


def transKeyTypeToInt(dic):
        result = {}
        for i in dic:
                result[int(i)] = set(dic[i])
        return result

def test1():
        f = file('followRel_test.json')
        followDic = json.load(f)
        flag = True
        for u in followDic:
                for i in followDic[u]:
                        result = followDic.get(str(i),None)
                        if result == None:
                                print(i)
                                flag = False
        print 'data correct : ',flag
        print 'uid num : ',len(followDic)
        
        followDic = transKeyTypeToInt(followDic)

        print followDic
        fanDic = getFanDicByFollowDic(followDic)
        print fanDic
        duplexingDic = getDuplexingDic(followDic,fanDic)
        print duplexingDic
                

def test2():
        followDic = getFollowDicByFile('../input/whiteUid_10w.data')
        #followDic = getFollowDicByFile('../input/.data')
        fanDic = getFanDicByFollowDic(followDic)
        duplexingDic = getDuplexingDic(followDic,fanDic)
        myPrint(duplexingDic)
        flag = checkoutIntegrity(followDic)
        print 'data correct : ',flag
        print 'uid num : ',len(followDic)
        
def myPrint(dic):
        for i in dic:
                print i,'--',dic[i]

if __name__ == '__main__':
        test2()


