import pandas as pd
import pprint
import heapq
from math import dist

# ----------------------------- Options ------------------------
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

dim = 2
pp = pprint.PrettyPrinter(indent=4)
# --------------------------------------------------------------


def kdtree(point_list, i=0):
    # https://en.wikipedia.org/wiki/K-d_tree#Example_implementation

    if point_list is None:
        return [None, None, point_list[0]]

    elif len(point_list) > 1:
        i = (i + 1) % dim
        point_list.sort(key=lambda point: point[i])
        median = len(point_list) // 2

        return [
            kdtree(point_list[:median], i),
            kdtree(point_list[median + 1:], i),
            point_list[median]
        ]


def insert(node, point, i=0):
    if node is not None:
        dx = node[2][i] - point[i]
        for j, c in ((0, dx >= 0), (1, dx < 0)):
            if c and node[j] is None:
                node[j] = [None, None, point]
            elif c:
                insert(node[j], point, (i + 1) % dim)


def delete(point_list, point):
    if point in point_list:
        point_list.remove(point)
        return kdtree(point_list)
    else:
        return print("Point doesn't exist")


def range_search(points, range_min, range_max):
    result = []
    for i in points:
        if (i[0] >= range_min[0]) and (i[0] <= range_max[0]) and (i[1] >= range_min[1]) and (i[1] <= range_max[1]):
            result.append(i)
    return result


def get_knn(kd_node, point, k, return_distances=True, i=0, heap=None):
    is_root = not heap
    if is_root:
        heap = []
    if kd_node is not None:
        d = int(dist(point, kd_node[2]))
        dx = kd_node[2][i] - point[i]
        if len(heap) < k:
            heapq.heappush(heap, (-d, kd_node[2]))
        elif d < -heap[0][0]:
            heapq.heappushpop(heap, (-d, kd_node[2]))
        i = (i + 1) % dim
        for b in [dx < 0] + [dx >= 0] * (dx * dx < -heap[0][0]):
            get_knn(kd_node[b], point, k, return_distances, i, heap)
    if is_root:
        neighbors = sorted((-h[0], h[1]) for h in heap)
        return neighbors if return_distances else [n[1] for n in neighbors]


def main():
    scientists = pd.read_csv("demo_file.csv", encoding='cp1252')
    points = scientists[['cord', 'education']].values.tolist()
    test_point = [1, 1]
    tree = kdtree(points)
    pp.pprint(tree)
    # insert(tree, test_point)
    # pp.pprint(tree)
    # pp.pprint(delete(points, test_point))
    # print(range_search(points, [1, 1], [6, 1]))
    print(get_knn(tree, [6, 1], 4))


if __name__ == "__main__":
    main()
