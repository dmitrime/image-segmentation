#!/usr/bin/env python

class Node:
    '''An element in the set.'''
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.parent = self
        self.rank = 0
        self.size = 1
    def __str__(self):
        return "[data = " + str(self.data) + ", rank = %d, size = %d]" % (self.rank, self.size)

class DisjointSet:
    '''Disjoin set implementation with union by rank and path compression
    heuristics. Keeps a dictionary that maps input data to Nodes.'''
    def __init__(self, num):
        self.data = {}
        self.num = num

    def makeSet(self, k, v):
        self.data[k] = Node(k, v)

    def unionNode(self, x, y):
        rep1 = self.findNode(x)
        rep2 = self.findNode(y)
        return self.link(rep1, rep2)

    def union(self, x, y):
        rep1 = self.findNode(self.data[x])
        rep2 = self.findNode(self.data[y])
        return self.link(rep1, rep2)

    def link(self, x, y):
        self.num = self.num - 1
        if x.rank > y.rank:
            y.parent = x
            x.size = x.size + y.size
            return x
        else:
            x.parent = y
            y.size = y.size + x.size
            if x.rank == y.rank:
                y.rank = y.rank + 1
            return y

    def findNode(self, x):
        if x != x.parent:
            x.parent = self.findNode(x.parent)
        return x.parent

    def find(self, x):
        return self.findNode(self.data[x])

