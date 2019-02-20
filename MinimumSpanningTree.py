import math
from segmentation import *


import Queue

class MinimumSpanningTree(object):

    def __init__(self, labels):
        self.d_mst = {}
        l_weight = []
        for i in labels.keys():
            for j in labels.keys():
                # l_weight.append([i, j])
                if j > i:
                    weight = self.calculate_weight(labels[i], labels[j])
                    t = [[i, j], weight]
                    l_weight.append(t)
        self.l_weight = sorted(l_weight, key=lambda x: x[1])
        self.build_tree()

    def get_mst(self):
        return self.d_mst
    @staticmethod
    def calculate_weight(l_bounding_1, l_bounding_2):
        y_mean_1 = (l_bounding_1[0] + l_bounding_1[1]) / 2.0
        y_mean_2 = (l_bounding_2[0] + l_bounding_2[1]) / 2.0
        x_mean_1 = (l_bounding_1[2] + l_bounding_1[3]) / 2.0
        x_mean_2 = (l_bounding_2[2] + l_bounding_2[3]) / 2.0
        euclidean_distance = math.sqrt(math.pow(x_mean_1 - x_mean_2, 2) + math.pow(y_mean_1 - y_mean_2, 2))
        return euclidean_distance


    def build_tree(self):
        d_mst = self.d_mst

        while self.l_weight:
            edge = self.l_weight.pop(0)
            # print 'edge', edge
            vertex1 = edge[0][0]
            vertex2 = edge[0][1]
            # print d_mst

            if self.is_disconnected(vertex1, vertex2):
                self.dictionary_add(d_mst, vertex1, [vertex2, edge[1]])
                self.dictionary_add(d_mst, vertex2, [vertex1, edge[1]])
             
        return d_mst



    def is_disconnected(self, vertex1, vertex2):
        d_mst = self.d_mst
        if (vertex1 not in d_mst.keys()) or (vertex2 not in d_mst.keys()):
            return True

        if vertex1 in self.d_mst.keys():
            return self.search(vertex1, vertex2)
        else:
            return self.search(vertex2, vertex1)


    def search(self, v1, v2):
        l_visited = []
        q = Queue.Queue()
        q.put(v1)
        while q.qsize() > 0:
            cur_v = q.get()
            l_visited.append(cur_v)

            for t in self.d_mst[cur_v]:
                neighbour = t[0]
                if v2 == neighbour:
                    return False
                if neighbour not in l_visited:
                    q.put(neighbour)
        return True

    @staticmethod
    def dictionary_add(d, key, t):
        if key not in d.keys():
            d[key] = []
        if t not in d[key]:
            d[key].append(t)

if __name__ == '__main__':
   
    fname = './equations/SKMBT_36317040717260_eq6.png'
    seg = Segmentation(fname)
    d = seg.get_labels()
    mst = MinimumSpanningTree(d)
    print mst.get_mst()
