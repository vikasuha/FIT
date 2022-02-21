import os

from rect import NullRect
from tests.testutil import take


import rtree
from rect import *

import collections
import unittest as ut
import random
import math
from tests.testutil import *
from tests.test_rtree import RectangleGen, TstO



def rr():
    return random.uniform(0.0, 10.0)



class my_tree():

    def __init__(self, size_point=0.01):
        self.size_point = size_point
        self.list_rect = []
        self.rt = rtree.RTree()
        self.visual = False

    def BuildTree(self, num_of_elements):
        G = RectangleGen()
        xs = [TstO(r) for r in take(num_of_elements, G.rect, self.size_point)]
        for x in xs:
            self.rt.insert(x, x.rect)
            self.invariants(self.rt)
            print("")
            self.list_rect.append(x.rect)

    def AddData(self, x, y):
        rect = Rect(x, y, x + self.size_point, y + self.size_point)
        obj = TstO(rect)
        self.rt.insert(obj, obj.rect)
        self.invariants(self.rt)
        print("")
        self.list_rect.append(rect)

    def invariants(self, tree):
        self._invariants(tree.cursor, {})

    def _invariants(self, node, seen):
        idx = node.index
        seen[idx] = True

        if node.holds_leaves():
            print("node: %d, children: %r" % (node.index, [c.index for c in node.children()]))
            if self.visual:
                print("Node rect:")
                node.rect.ToString()
                print("Children rect:")
                for c in node.children():
                    print(str(c.index)+": ", end="")
                    c.rect.ToString()

        r = Rect(node.rect.x, node.rect.y, node.rect.xx, node.rect.yy)
        for c in node.children():
            if not c.is_leaf(): self._invariants(c, seen)

    def FindPoint(self, x, y):
        node = self.rt.cursor
        answer_list = []
        queue = []
        visited = []
        queue.append(node)
        answer_list.append(node)
        while queue:
            my_node = queue.pop(0)
            for c in my_node.children():
                if c.rect.does_containpoint1(x, y) and visited.count(c) == 0:
                    visited.append(c)
                    answer_list.append(c)
                    queue.append(c)
                    print(c.index)
        for c in answer_list:
            print(c.index)

        # while True:
        #     for c in answer_list[-1].children():
        #         if c.rect.does_containpoint(point):
        #             answer_list.append(c)
        #             print(c.index)
        #             run = True
        # while()
        # if node.rect.does_containpoint(point):
        #     for c in node.children():

        # res2 = list([ro for ro in self.rt.query_point(point)])
        # for obj in res2:
        #     print(obj.first_child)
        #     print(obj.index, end=" ")
        #     obj.rect.ToString()



    def LoadTree(self, file_name):
        f = open(file_name, "r")
        lines = f.readlines()
        objs = []
        for line in lines:
            coordinates = line.split()
            x = float(coordinates[0])
            y = float(coordinates[1])
            xx = float(coordinates[2])
            yy = float(coordinates[3])
            rect = Rect(x,y,xx,yy)
            obj = TstO(rect)
            objs.append(obj)

        for obj in objs:
            self.rt.insert(obj, obj.rect)
            # self.invariants(self.rt)

        f.close()

    def SaveTree(self, file_name):
        f = open("rt_"+file_name + ".txt", "w+")
        for rect in self.list_rect:
            f.write(str(rect.x) + " " + str(rect.y) + " " + str(rect.xx) + " " + str(rect.yy) + "\n")
        f.close()

