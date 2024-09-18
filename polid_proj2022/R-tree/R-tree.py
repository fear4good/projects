import csv
from typing import Union, Any
import matplotlib.pyplot
import pandas as pd
from operator import itemgetter
from itertools import islice
import sys
import cmath
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from pandas import Series, DataFrame
from pkg_resources.extern import names
import time


class Rtree:
    def __init__(self, root, maxnodes):
        self.j = 0
        self.l = 1
        self.maxnodes = maxnodes
        self.data = root
        self.child = []
        self.keys = [root]
        self.temp = []
        # self.child.append(root)
        # self.keys.append(root)

    def make_tree(self, data):

        if len(self.child) == 0:
            self.child.append(data)
            self.keys.append(data)
        else:
            for i in range(len(self.keys)):
                if data[0][0] > self.keys[i][0][0] and data[1][0] < self.keys[i][1][0]:

                    if self.l == 1:
                        self.child.insert(0, data)
                        self.l = 0
                    else:
                        self.child[0].extend(data)
                        self.l = 1

            # print(self.child)
            self.temp.append(data)

    def clear_temp(self, k):
        self.keys.extend(self.temp)
        self.temp = []
        for i in range(0, k, 1):
            self.keys.pop(0)

    def dist(self, node):

        d = [[], [], [], []]
        # print(self.child[0][0][0])

        # print(node[0])
        for i in range(len(self.child)):
            d[0].append(abs(self.child[i][0][0] - node[0]))
            d[1].append(abs(self.child[i][0][1] - node[1]))
            d[2].append(abs(self.child[i][1][0] - node[0]))
            d[3].append(abs(self.child[i][1][1] - node[1]))

        return d

    def add_node(self, node):
        j = [[], []]
        d = temp.dist(node)
        if min(d[0]) < min(d[2]):
            j[0] = [min(d[0]), len(d[0]) - 1]
            k = 0
            l = 0
        else:
            j[0] = [min(d[2]), len(d[2]) - 1]
            k = 1
            l = 0
        print(j[0][0])
        print(self.child[j[0][1]][k][l])
        s = self.child[j[0][1]][k][l] + j[0][0]
        print(s)
        self.child[j[0][1]][k][l] = s
        if min(d[1]) < min(d[3]):
            j[1] = [min(d[1]), len(d[1]) - 1]
            k = 0
            l = 1
        else:
            j[1] = [min(d[3]), len(d[3]) - 1]
            l = 1
            k = 1

        print(j[0][1])
        self.child[j[1][1]][k][l] + j[1][0]

    # j =[min(d[0]),len(d[0]),min(d[1]),len(d[1]),min(d[2]),len(d[2]),min(d[3]),len(d[3])]



    def find_node(self, node):
        j = 0
        for i in range(len(self.child)):
            if node[0] == self.child[i][0][0] or node[0] == self.child[i][1][0]:
                j += 1
            if node[1] == self.child[i][0][1] or node[1] == self.child[i][1][1]:
                j += 1

        if j == 2:
            print("Node found")

        else:
            print("Node didnt exist")


    def print_tree(self):
        for i in range(len(self.child)):
            print(self.child[i])

    def get_nearest(self, node, num_neighbors):
        distances = []
        start_time = time.time()
        for i in range(len(self.child)):
            distances.append(list(map( abs,[(node[0] - self.child[i][0][0]) * 2 + ((node[1] - self.child[i][0][1]) * 2) ** 0.5, i])))
            distances.append(list(map( abs,[(node[0] - self.child[i][1][0]) * 2 + ((node[1] - self.child[i][1][1]) * 2) ** 0.5, i])))

        distances = sorted(distances, key=itemgetter(0))
        neighbors = list()
        r = []
        for j in range(num_neighbors):
            neighbors.append(distances[j][1])
            r.append(self.child[neighbors[j]][0])
        
        knn_time = time.time() - start_time
        return r, knn_time

    def range_search(self, List, node):
        r = []

        for i in range(len(List)):
            if node[0][0] <= List[i][0] and node[0][1] <= List[i][1] and node[1][0] >= List[i][0] and node[1][1] >= \
                    List[i][1]:
                print(List[i][2])

        return r


def lenght(data, j, D):
    L = []
    # print(D)
    for i in range(len(D)):
        temp = D[i] // j
        L.append(temp)
        if D[i] % j == 0:
            L.append(temp)
        else:
            temp += 1
            L.append(temp)

    s, Nodes, leave = min_may(data, L)
    for i in range(len(L)):
        L[i] = L[i] - leave[i]

    return s, L, Nodes

def min_may(List, data):
    Temp = []
    k = 0
    i = 0
    Nodes = []
    NewTemp = []

    List = iter(List)
    NewList = [list(islice(List, k)) for k in data]

    # print(NewList)

    for k in range(0, len(NewList), 1):
        xmin = sys.maxsize
        miny = sys.maxsize
        xmax = -sys.maxsize - 1
        maxy = -sys.maxsize - 1
        for i in range(data[k]):
            tempx = NewList[k][i][0]
            tempy = NewList[k][i][1]
            if xmax < tempx:
                xmax = tempx
            if xmin > tempx:
                xmin = tempx
            if maxy < tempy:
                maxy = tempy
            if miny > tempy:
                miny = tempy

        Temp.append([[xmin, miny], [xmax, maxy]])
        temp.make_tree(Temp[k])
        # print(Temp[k],k)

    s = 0
    leave = []
    for k in range(len(NewList)):
        j = data[k]
        for i in range(0, j, 1):
            if Temp[k][0][0] < NewList[k][i][0] < Temp[k][1][0] and Temp[k][0][1] < NewList[k][i][1] < Temp[k][1][1]:
                Nodes.append(NewList[k][i])
            else:
                s += 1

        leave.append(s)
        s = 0

    # print(leave)
    s = len(Nodes)
    return s, Nodes, leave


def main():
    data = pd.read_csv("demo_file.csv", delimiter=',')
    data = data.iloc[0:670]

    Data = pd.DataFrame(data)
    l1 = Data['cord'].values.tolist()
    l2 = Data['award'].values.tolist()
    l3 = Data['Name'].values.tolist()

    """
    new_l1 = []
    new_L2 = []

    for i in l1:
        new_l = i.replace(",", ".")
        new_l1.append(new_l)

    for i in l2:
        new_l = i.replace(",", ".")
        new_L2.append(new_l)
    """
    List = list(zip(l1, l2))
    List = [[int(int(j)) for j in i] for i in List]

    for i in range(len(List)):
        List[i].append(l3[i])

    xmin = sys.maxsize
    miny = sys.maxsize
    xmax = -sys.maxsize - 1
    maxy = -sys.maxsize - 1

    maxnodes = 4
    minnodes = int(maxnodes / 2)

    xmax = max(List[i][0] for i in range(len(List)))
    maxy = max(List[i][1] for i in range(len(List)))
    xmin = min(List[i][0] for i in range(len(List)))
    miny = min(List[i][1] for i in range(len(List)))

    Temp = []
    Temp = [[xmin, miny], [xmax, maxy]]
    print(Temp)
    global temp
    temp = Rtree(Temp, maxnodes)

    List = sorted(List, key=itemgetter(0))
    print(List)
    NewList = []
    D = []

    for i in range(len(List)):
        if xmin < List[i][0] < xmax and miny < List[i][1] < maxy: NewList.append(List[i])

    D.append(len(NewList))
    s, l, NewList = lenght(NewList, minnodes, D)
    i = 0
    k = 2 ** i
    temp.clear_temp(k)

    S = max(l)

    while S > maxnodes:
        s, l, NewList = lenght(NewList, minnodes, l)
        i += 1
        k = 2 ** i
        temp.clear_temp(k)
        S = max(l)
        # print(S)
        # print(l)
    temp.print_tree()
    return List

#------------pass add and ------

def add_node(node):
    pass

#---------------------------------



if __name__ == "__main__":
        global temp
        List = main()

        print("Give  choice what you want to do:")
        print("1:Find node")
        print("2:Get n nearest")
        print("3:Range search")
        print("4:Search by [A-Z] , awards and cords")
        print("5:Add node")
        print("6:Exit")
        i = int(input())
        while i != 6:
            if i == 1:
                print("Give node coordinates you want to find:")
                print("Give cord first:")
                x = input()
                print("Then award:")
                y = input()
                node = [int(x), int(y)]
                for i in range(len(List)):
                    if int(x)==List[i][0] and int(y)==List[i][1]:
                        print(List[i][2])
            elif i == 2:
                print("Give node coordinates you want to find:")
                print("Give cord first:")
                x = input()
                print("Then award :")
                y = input()
                print("Give number of nearest:")
                z = input()
                node = [int(x), int(y)]
                nodes, knn_time = temp.get_nearest(node, int(z))
                l = 0
                for i in range(len(nodes)):
                    for j in List:
                        if nodes[i][0] == j[0] or nodes[i][1] == j[1]:
                            print(j[2])
                            break
                print("KNN search took {:.4f} seconds".format(knn_time))
                
            elif i == 3:
                print("Give cordmin")
                x = input()
                print("Give awardmin:")
                y = input()
                print("Give cordmax:")
                z = input()
                print("Give awardmax:")
                u = input()
                node = [[int(x), int(y)], [int(z), int(u)]]
                start_time = time.time()
                temp.range_search(List, node)
                range_time = time.time() - start_time
                print("Range search took {:.4f} seconds".format(range_time))
                
            elif i == 4:
                first_char = input("Enter the First character: ")
                last_char = input("Enter the Second character: ")
                award = int(input("Enter the max award:"))
                cord = int(input("Enter the max cord:"))

                df = pd.read_csv("demo_file.csv")
                filtered_df = df[df['award'] <= award]
                filtered_df = filtered_df[
                    (filtered_df['Name'].str[0] >= first_char) & (filtered_df['Name'].str[0] <= last_char)]
                filtered_df = filtered_df[(filtered_df['cord'] <= cord)]
                names_with_award_le = filtered_df['Name'].tolist()
                sorted_names = sorted(names_with_award_le)
                print('The names in the namelist with awards less than or equal to', award,
                      'and with cords less than or equal to', cord, 'sorted by character:',
                      sorted_names)
            elif i==5:
                print("Give cords:")
                x = input()
                print("Then awards:")
                y = input()
                print("And Name:")
                n = input()
                node = [int(x), int(y),str(n)]
                print(node)
                temp: add_node(node)


            print("Give  choice what you want to do:")
            print("1:Find node")
            print("2:Get n nearest")
            print("3:Range search")
            print("4:Search by [A-Z] , awards and cords")
            print("5:Add node")
            print("6:Exit")
            i = int(input())
