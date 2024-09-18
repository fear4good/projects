# tree dimensions
DIMENSIONS = 2


class Node:
    def __init__(self, coords, name=None, left=None, right=None, next_dimension=None):
        self.coords = coords
        self.name = name
        self.left = left
        self.right = right
        self.next_dimension = next_dimension


# input: coords list
# output: nodes list for next dimension and existing root 
def create_range_tree(nodes_list, dimension=0):

    if len(nodes_list) == 0 or dimension >= DIMENSIONS:
        return None, []

    # assign middle element of the list as root
    mid = int(len(nodes_list) / 2)
    root = nodes_list[mid]

    # left and right subtree
    root.left, left_list = create_range_tree(nodes_list[:mid], dimension)
    root.right, right_list = create_range_tree(nodes_list[mid + 1 :], dimension)

    # next dimensions
    merged_list = []

    if dimension + 1 < DIMENSIONS:  # just for 2-dimesional
        merged_list = merge(root, left_list, right_list, dimension + 1)

        
    root.next_dimension, _ = create_range_tree(merged_list, dimension + 1)

    return root, merged_list


# input: root,two sorted listes
# output: sorted final_list
def merge(root, left_list, right_list, dimension=0):

    if dimension >= DIMENSIONS:
        return []

    final_list = []
    left_index = 0
    right_index = 0

    # merge both lists and keep them sorted
    # while left, right elements exist
    while left_index < len(left_list) and right_index < len(right_list):
        if (
            left_list[left_index].coords[dimension]
            < right_list[right_index].coords[dimension]
        ):
            final_list.append(
                Node(left_list[left_index].coords, left_list[left_index].name)
            )
            left_index = left_index + 1
        else:
            final_list.append(
                Node(right_list[right_index].coords, right_list[right_index].name)
            )
            right_index = right_index + 1

    # an exoume mono aristera kai oxi deksia (case '1')
    while left_index < len(left_list):
        final_list.append(
            Node(left_list[left_index].coords, left_list[left_index].name)
        )
        left_index = left_index + 1

    # an exoume deksia kai oxi aristera (case '2')
    while right_index < len(right_list):
        final_list.append(
            Node(right_list[right_index].coords, right_list[right_index].name)
        )
        right_index = right_index + 1

    # find whether root is located at final_list or at the end 
    # eite tha einai kapou mesa sto final list h sto telos
    for i in range(0, len(final_list)):
        if root.coords[dimension] < final_list[i].coords[dimension]:
            # in
            return final_list[:i] + [Node(root.coords, root.name)] + final_list[i:]

    # end
    return final_list + [Node(root.coords, root.name)]


# search for a specific node in the tree
#input: root, searching coords
#output: list me tous komvous pou exoun autes tis syntetagmenes
def search(root, coords, dimension=0):

    if root is None:
        return []

        # an oi syntetagmenes tou node einai megalyteres tou root, search right subtree
    if coords[dimension] > root.coords[dimension]:
        return search(root.right, coords, dimension)
        # an oi syntetagmenes tou node einai mikroteres tou root, search left subtree
    elif coords[dimension] < root.coords[dimension]:
        return search(root.left, coords, dimension)
        
    else:
        nodes_list = []
        if root.coords == coords:
            nodes_list.append(root)

        return nodes_list + search(
            root.left, coords, dimension
        ) 


# search for split node, used in range search
# input: root, coords
# output: split node - found or not
def find_split_node(root, range_coords, dimension=0):
    if root:
        # case:1 min > root
        if range_coords[dimension][0] > root.coords[dimension]:
            return find_split_node(root.right, range_coords, dimension)
            # case2: max < root
        elif range_coords[dimension][1] < root.coords[dimension]:
            return find_split_node(root.left, range_coords, dimension)
        else:
            # split node or None (not found)
            return root
    return None


# an oi syntetagmenes anikoun sto given range - range search
# input: coords, given range
# output: boolean (True or false statement)
def is_in_range(coords, range_coords):
    for d in range(0, DIMENSIONS):
        # mikroteri tou min h megalyterh tou max
        if coords[d] < range_coords[d][0] or coords[d] > range_coords[d][1]:
            return False
    return True


# input: root,  searching span
# output: nodes_list mesa sto searching span
def range_search(root, range_coords, dimension=0):

    if root is None:
        return []

    # first d-1 dimensions
    if dimension + 1 < DIMENSIONS:
        # find split node -  ekei pou xwrizei i anazitisi gia to min, max
        split_node = find_split_node(root, range_coords, dimension)

        if split_node is None:
            return []

        nodes_list = []

        # put split node into list
        if is_in_range(split_node.coords, range_coords):
            nodes_list.append(split_node)

            # start search on the left subtree (min)
        left_child = split_node.left
        while left_child:
            if is_in_range(left_child.coords, range_coords):
                nodes_list.append(left_child)

                # an to min einai pio aristera
            if range_coords[dimension][0] <= left_child.coords[dimension]:
                # tha prepei na paroume ta deksia paidia tou kai stin epomeni diastasi
                if left_child.right:
                    nodes_list += range_search(
                        left_child.right.next_dimension, range_coords, dimension + 1
                    )
                    # kai na synexisoume aristera
                left_child = left_child.left
            else:
                # synexizoume deksia
                left_child = left_child.right

                # start search on the right subtree (max)
        right_child = split_node.right
        while right_child:
            if is_in_range(right_child.coords, range_coords):
                nodes_list.append(right_child)

                # an to max einai pio deksia
            if right_child.coords[dimension] <= range_coords[dimension][1]:
                # tha prepei na paroume ta aristera paidia tou kai stin epomeni diastasi
                if right_child.left:
                    nodes_list += range_search(
                        right_child.left.next_dimension, range_coords, dimension + 1
                    )
                    # right child
                right_child = right_child.right
            else:
                # left child
                right_child = right_child.left

        return nodes_list

    # teleutaia diastasi - periorizoume sta katallhla shmeia
    if dimension + 1 == DIMENSIONS:
        if root.coords[dimension] < range_coords[dimension][0]:
            return range_search(root.right, range_coords, dimension)
        elif root.coords[dimension] > range_coords[dimension][1]:
            return range_search(root.left, range_coords, dimension)
        else:
            
            nodes_list = (
                [root]
                + range_search(root.right, range_coords, dimension)
                + range_search(root.left, range_coords, dimension)
            )
            return nodes_list
        

