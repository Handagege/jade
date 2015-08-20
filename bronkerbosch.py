#!/usr/bin/python
# -*- coding: utf-8 -*-

#vertexConnectDic 存储与key值点连接的点集合
#verterConnectNumDic 存储与key值点连接的点总数
def bronkerbosch(p,r,x,vertexConnectDic,result):
	if p|x == set():
		result.append(r)
	#	print r
	#v = choiceOptimalVertex(p,verterConnectNumDic)
	else:
		while p != set():
			vertex = p.pop()
			#vertexSet = set([vertex])
			new_r = r.copy()
			new_r.add(vertex)
			connectVertex = vertexConnectDic.get(vertex,None)
			bronkerbosch(p&connectVertex,new_r,x&connectVertex,vertexConnectDic,result)
			x.add(vertex)

def bronkerboschSimplePivot(p,r,x,vertexConnectDic,limitNum,result):
        if len(p)+len(r) < limitNum:
                return
	if p|x == set():
		result.append(r)
	else:
		u = 0
		rejectConnectVertexSet = set()
		if p != set():
			u = p.pop()
			rejectConnectVertexSet = vertexConnectDic.get(u,set())
			p.add(u)
		for vertex in p-rejectConnectVertexSet:
			p.remove(vertex)
			new_r = r.copy()
			new_r.add(vertex)
			connectVertex = vertexConnectDic.get(vertex,set())
                        #f.write(str(vertex)+' : '+ str(connectVertex) + '\n')
			bronkerboschSimplePivot(p&connectVertex,new_r,x&connectVertex,vertexConnectDic,limitNum,result)
                        #f.write(str(p&connectVertex)+' : '+ str(new_r) +'\n')
			x.add(vertex)

def findMaximalClique(graph,method='base'):
	l = len(graph)
	vertexList = range(0,l)
	p = set(vertexList)
	r = set()
	x = set()
	vertexConnectDic = {}
	for vertex_id_i in vertexList:
		connectVertexList = []
		for vertex_id_j in vertexList:
			if graph[vertex_id_i][vertex_id_j]:
				connectVertexList.append(vertex_id_j)
		vertexConnectDic[vertex_id_i] = set(connectVertexList)
        result = []
	if method == 'base':
		bronkerbosch(p,r,x,vertexConnectDic,result)
	elif method == 'pivot':
		bronkerboschSimplePivot(p,r,x,vertexConnectDic,result)
        print result

def test1(graph):
	import time

	beg = time.time()
	for i in range(0,1):
		findMaximalClique(graph)
	end = time.time()
	print('base bron-kerbosch-alg cost time : %f'%(end-beg))

def test2(graph):
	import time

	beg = time.time()
	for i in range(0,1):
		findMaximalClique(graph,'pivot')
	end = time.time()
	print('add pivot vertex bron-kerbosch-alg cost time : %f'%(end-beg))

if __name__=='__main__':
	graph = []
	graph.append([0,1,1,1,0,0,1])
	graph.append([1,0,0,1,1,0,0])
	graph.append([1,0,0,1,0,0,0])
	graph.append([1,1,1,0,1,1,0])
	graph.append([0,1,0,1,0,0,0])
	graph.append([0,0,0,1,0,0,0])
	graph.append([1,0,0,0,0,0,0])
	
	test1(graph)
	test2(graph)

	graph = []
	graph.append([0,1,1,1,0,0,1,1])
	graph.append([1,0,0,1,1,0,0,0])
	graph.append([1,0,0,1,0,0,0,1])
	graph.append([1,1,1,0,1,1,0,0])
	graph.append([0,1,0,1,0,0,0,0])
	graph.append([0,0,0,1,0,0,0,0])
	graph.append([1,0,0,0,0,0,0,1])
	graph.append([1,0,1,0,0,0,1,0])
	test1(graph)
	test2(graph)

	graph = []
	graph.append([0,1,0,1,1,0,0,0,0,0])
	graph.append([1,0,1,0,1,1,0,0,0,0])
	graph.append([0,1,0,0,0,1,1,0,0,0])
	graph.append([1,0,0,0,1,0,0,1,0,0])
	graph.append([1,1,0,1,0,0,0,1,1,0])
	graph.append([0,1,1,0,0,0,0,0,1,1])
	graph.append([0,0,1,0,0,0,0,0,0,1])
	graph.append([0,0,0,1,1,0,0,0,1,0])
	graph.append([0,0,0,0,1,1,0,1,0,1])
	graph.append([0,0,0,0,0,1,1,0,1,0])
	test1(graph)
	test2(graph)

