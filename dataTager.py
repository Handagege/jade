#!/usr/bin/python
# -*- coding: utf-8 -*-

def getTagData(path):
        tagDataDic = {}
        with open(path,'r') as f:
                for line in f:
                        data = line.split('\t')
                        uid = int(data[0])
                        if len(data) > 1:
                                tag = data[1].strip('\n')
                                tagDataDic[uid] = set(tag.split(','))
        f.close()
        return tagDataDic 

def tagDataByTaged():
        tagDataDic = {}
        with open('1036663592_0_tag_done','r') as f:
                for line in f:
                        data = line.split('\t')
                        uid = int(data[0])
                        tag = data[1]
                        tag = tag.strip('\n')
                        tagDataDic[uid] = tag
        f.close()

        waitedTagDataDic = {}
        with open('relNode_expand_1_1036663592','r') as f:
                for line in f:
                        if line:
                                waitedTagDataDic[int(line)] = ''
        f.close()

        for i in waitedTagDataDic:
                if i in tagDataDic:
                        waitedTagDataDic[i] = tagDataDic[i]

        f = open('1036663592_1_tag_done','w')
        for i in waitedTagDataDic:
                if waitedTagDataDic[i]:
                        s = '%d %s'%(i,waitedTagDataDic[i])
                        f.write(s+'\n')
                else:
                        f.write(str(i)+'\n')
        f.close()


if __name__ == '__main__':
        tagDataDic = getTagData('1036663592_0_tag_done')
        tagSet = set()
        for i in tagDataDic:
                tagSet.update(tagDataDic[i])
        tagSizeDic = {}
        for i in tagSet:
                tagSizeDic[i] = 0
        for i in tagDataDic:
                for j in tagDataDic[i]:
                        tagSizeDic[j] += 1
        for i in tagSet:
                print '%s -- %d'%(i,tagSizeDic[i])



