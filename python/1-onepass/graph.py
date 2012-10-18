#!/usr/bin/env python

class Edge:
    def __init__(self, v1, v2, dist):
        self.v1 = v1
        self.v2 = v2
        self.dist = dist
        #print('(%d, %d) = %lf' % (self.v1,self.v2,self.dist))

class Graph:
    def __init__(self, w, h, pix):
        self.w = w
        self.h = h
        self.E = []
        for j in range(h):
            for i in range(w):
                cur = j*w + i
                if i < w-1:
                  self.E.append(Edge(cur, j*w + (i+1), self.dist(pix[i,j], pix[i+1,j])))
                if j < h-1:
                  self.E.append(Edge(cur, (j+1)*w + i, self.dist(pix[i,j], pix[i,j+1])))
                if i < w-1 and j < h-1:
                  self.E.append(Edge(cur, (j+1)*w + (i+1), self.dist(pix[i,j], pix[i+1,j+1])))
                if i < w-1 and j > 0:
                  self.E.append(Edge(cur, (j-1)*w + (i+1), self.dist(pix[i,j], pix[i+1,j-1])))
        self.E.sort(lambda a,b: cmp(a.dist, b.dist))

    def dist(self, v1, v2):
        return sum(map(lambda a,b: (a-b)*(a-b), v1, v2))**.5

