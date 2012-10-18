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

    #def dist(self, v1, v2):
    #    return sum(map(lambda a,b: (a-b)*(a-b), v1, v2))**.5

    def dist(self, a, b):
        return ((a-b)*(a-b))**.5

class Graph2:
    def __init__(self, w, h, pix, rad, take):
        self.w = w
        self.h = h
        self.E = []
        for j in range(h):
            for i in range(w):
                nearest = []
                for k in range(rad):
                    cur = j*w + i
                    if i < w-k:
                      d = self.dist((i,j) + pix[i,j], (i+k,j) + pix[i+k,j])
                      nearest.append(Edge(cur, j*w + (i+k), d))
                    if j < h-k:
                      d = self.dist((i,j) + pix[i,j], (i,j+k) + pix[i,j+k])
                      nearest.append(Edge(cur, (j+k)*w + i, d))
                    if i < w-k and j < h-k:
                      d = self.dist((i,j) + pix[i,j], (i+k,j+k) + pix[i+k,j+k])
                      nearest.append(Edge(cur, (j+k)*w + (i+k), d))
                    if i < w-k and j > k:
                      d = self.dist((i,j) + pix[i,j], (i+k, j-k) + pix[i+k,j-k])
                      nearest.append(Edge(cur, (j-k)*w + (i+k), d))
                nearest.sort(lambda a,b: cmp(a.dist, b.dist))
                self.E.extend(nearest[:take])
        self.E.sort(lambda a,b: cmp(a.dist, b.dist))

    def dist(self, v1, v2):
        return sum(map(lambda a,b: (a-b)*(a-b), v1, v2))**.5

