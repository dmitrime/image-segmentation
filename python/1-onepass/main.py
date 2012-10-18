#!/usr/bin/env python

import sys
import time
from random import randrange
import Image
import ImageFilter
from filterfft import *
from disjointset import DisjointSet
from graph import Graph

K = 300
MinCC = 20
Sigma = 0.5


def tau(C):
    return K/float(C)

def segment(w, h, ds, g):
    dist = [tau(1.0)]*(w*h)
    me = 0
    for e in g.E:
        #print('Edge %d and %d = %f' % (e.v1, e.v2, e.dist))
        p1 = ds.find(e.v1)
        p2 = ds.find(e.v2)
        if p1 != p2:
            if e.dist <= min(dist[p1.key], dist[p2.key]):
                pn = ds.unionNode(p1, p2)
                dist[pn.key] = e.dist + tau(pn.size)
                #print('Merging %d and %d, sz = %d, tau = %lf, dist = %lf, tot = %lf' % (p1.key, p2.key, pn.size, tau(pn.size), e.dist, dist[pn.key]))
                me = me + 1
    #for i in range(w*h):
    #    print dist[i],
    #print('Total merges: ',me)

def postprocess(ds, g):
    for e in g.E:
        p1 = ds.find(e.v1)
        p2 = ds.find(e.v2)
        if p1 != p2:
            if p1.size < MinCC or p2.size < MinCC:
                ds.unionNode(p1, p2)

def randomColour(w, pix, ds):
    col = {}
    for (pp, node) in ds.data.items():
        rep = ds.findNode(node)
        if col.get(rep) == None:
            col[rep] = tuple([randrange(0, 255) for _ in node.data])
        (j,i) = (pp/w, pp%w)
        pix[i,j] = col[rep]

    return len(col)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: main.py image [K min sigma]")
        sys.exit()

    if len(sys.argv) > 2:
        K = int(sys.argv[2])
    if len(sys.argv) > 3:
        MinCC = int(sys.argv[3])
    if len(sys.argv) > 4:
        Sigma = float(sys.argv[4])

    print('Processing image %s, K = %d' % (sys.argv[1], K))
    start = time.time()

# Apply gaussian filter to all color channels separately
    im = Image.open(sys.argv[1])
    (width, height) = im.size
    print('Image width = %d, height = %d' % (width, height))

    print('Blurring with Sigma = %f' % Sigma)
    source = im.split()
    blurred = []
    for c in range(len(source)):
        I = numpy.asarray(source[c])
        I = filter(I, gaussian(Sigma))
        blurred.append(Image.fromarray(numpy.uint8(I)))
    im = Image.merge(im.mode, tuple(blurred))
    #im.show()

    pix = im.load()
    ds = DisjointSet(width*height)
    for j in range(height):
        for i in range(width):
            ds.makeSet(j*width + i, pix[i,j])

    print('Number of pixels: %d' % len(ds.data))
    g = Graph(width, height, pix)
    print('Number of edges in the graph: %d' % len(g.E))
    print('Time: %lf' % (time.time() - start))

    segstart = time.time()
    segment(width, height, ds, g)
    print('Segmentation done in %lf, found %d segments' % (time.time() - segstart, ds.num))

    print('Postprocessing small components, min = %d' % MinCC)
    postproc = time.time()
    postprocess(ds, g)
    print('Postprocessing done in %lf' % (time.time() - postproc))

    l = randomColour(width, pix, ds)
    print('Regions produced: %d' % l)

    print
    print('Time total: %lf' % (time.time() - start))

    im.show()

