import csv
import range_tree as rt
import pandas as pd
import pprint

pp = pprint.PrettyPrinter(indent=4)


# print tree: pre-order traversal
def pre_order(root, string=""):
    if root:
        print(string + str(root.coords) + "|Name:" + str(root.name))
        pre_order(root.left, "\t" + string + "-left-")
        pre_order(root.right, "\t" + string + "-right-")


# range search: print result

def print_nodes(nodes_list):
    for node in nodes_list:
	    print(str(node.coords) + "\t|\tName:" + str(node.name))


#euclidean distance variation for kNN - exclude the root

def euclidean_dist(pointa, pointb):
    return sum((pointa[i] - pointb[i]) ** 2 for i in range(rt.DIMENSIONS))


#kNN
#geitones (+1 gia ton eauto tou), to node, tou opoiou psaxnw tous geitones
def knn_algorithm(k, point, root):
    
    #tyxaia arxikopoihsh toy [[x_min, x_max],[y_min, y_max]] gia range search
    my_range = [[point.coords[0]-3, point.coords[0]+3],[point.coords[1]-3, point.coords[1]+3]]
    
    #range search sto arxiko diastima gyrw apo to simeio endiaferontos
    temp_nodes = rt.range_search(root, my_range)
    
    # calculate each node distance returned by range search
    # starting from the point of interest 
    temp_distances = [[euclidean_dist(point.coords, node.coords), node.name, node.coords] for node in temp_nodes]
    temp_distances = sorted(temp_distances)
    
    #prosarmozoume to diastima wste na psaxnoume aristera apo to x_min,y_min
    #kai deksia apo to x_max, y_max kai epanalamvanoume mexri na vroume k geitones
    while len(temp_nodes) < k:
        
        #pairnoume to max giati mporei na exoume vrei mono ton eauto tou
        #opote h apostash tha einai 0 
        my_range[0][1] += max(temp_distances[int(len(temp_distances)/2)][0],1)
        my_range[1][1] += max(temp_distances[int(len(temp_distances)/2)][0],1)
        my_range[0][0] -= max(temp_distances[int(len(temp_distances)/2)][0],1)
        my_range[1][0] -= max(temp_distances[int(len(temp_distances)/2)][0],1)
        
        temp_nodes = rt.range_search(root, my_range)
        temp_distances = [[euclidean_dist(point.coords, node.coords), node.name, node.coords] for node in temp_nodes]
        temp_distances = sorted(temp_distances)

    return temp_distances[0:k]


my_nodes = []
nodes_counter = 0
 # ********************** Προσοχή στο path *********************
filename = r'C:\Users\fear1\Desktop\polidiastates\polidiastates_all\Range-tree\demo_file.csv'     # read csv file while creating node_objects
with open(filename, mode='r',  encoding='cp1252') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)        #skip fist row (header)
        for row in csv_reader:
            my_nodes.append(rt.Node([float(row[0].replace(',','.')), float(row[1].replace(',','.'))], row[3]))  #error
            nodes_counter += 1
        print('Number of Nodes: ' + str(nodes_counter))

scientists = pd.read_csv("demo_file.csv", encoding='cp1252')
scnt = scientists.values.tolist()
# print(scnt)
#   sortaroume tis syntetagmenes twn komvwn kai ftiaxnoume to dentro
sorted_nodes = sorted(my_nodes, key=lambda l:(l.coords[0], l.coords[1]))
# print(sorted_nodes)
my_root, _ = rt.create_range_tree(sorted_nodes)

# perivallon menu
print("\nMENU")
print("0 - Print Tree")
print("1 - Range Search")
print("2 - kNN")
print("-1 - Exit Program\n")

choice = int(input())

while choice != -1:

    # Print Tree
    if choice == 0:
        print('-----------------------')
        pre_order(my_root)
        print('-----------------------')

    # Range Search
    elif choice == 1:
        my_range = []
        
        for d in range(rt.DIMENSIONS):
            d_range = []
            
            print("Give minimum coordinate for dimension " + str(d))
            d_range.append(int(input()))
            
            print("Give maximum coordinate for dimension " + str(d))
            d_range.append(int(input()))
            
            my_range.append(d_range)            
        print('-----------------------')
        
        res_list = rt.range_search(my_root, my_range)
        
        if len(res_list) == 0:
            print('-----------------------')
            print("Not Found!")
            print('-----------------------')
            
        else:
            print('-----------------------')
            print('Nodes found (' + str(len(res_list)) + ')')
            print_nodes(res_list)
            print('-----------------------')

    #kNN
    elif choice == 2:
            name = input("Give your Scientist's name: ")
            #k+1 giati perilamvanei kai ton eauto tou, distance = 0
            k = int(input("Number of scientists you want: ")) + 1
            
            pcoords = [0,0]
            flag = 0
            # check
            for i in range(len(scnt)):
                if scnt[i][3] == name:
                    pcoords[0] = scnt[i][0]
                    pcoords[1] = scnt[i][1]
                    flag = 1

            if flag != 1:
                print("Scientist doesn't exist")
            
            else:
                #theloume ton komvo pou zitithike san node object
                res = rt.range_search(my_root, [[pcoords[0], pcoords[0]],[pcoords[1], pcoords[1]]])
                print('-----------------------')
                
                neighboring_scnt = knn_algorithm(k, res[0], my_root)
                
                for i in range(len(neighboring_scnt)):
                    print("|Distance:" + str(neighboring_scnt[i][0]) + "\t|\tName:" + str(neighboring_scnt[i][1]) + "\t|\tCoordinates:" + str(neighboring_scnt[i][2]))
                    print("\n")
                    
            print('-----------------------')

    choice = int(input())
