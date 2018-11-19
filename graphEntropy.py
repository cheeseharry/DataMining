from heapq import nlargest
import math
import networkx as nx
import sys
sys.setrecursionlimit(1000000)  # set the maximum depth as 1000000


cluster_result_list = []


# read input and initialize graph
def read_input():
    G = nx.Graph()
    inputFile = open("assignment5_small.txt")
    for line in inputFile.readlines():
        line = line.split()
        #print(line)
        G.add_edge(line[0], line[1])  # construct graph
        pass
    #print(G.edges)
    #calc_and_cut_max_betweenness(G)
    # print(nx.number_connected_components(G))
    # print(nx.is_connected(G))
    # print(list(get_subgraph_component(G)))
    # calc_and_cut_max_betweenness(G)
    # nx.density(G)
    select_seed_node(G)
    sorted_result = sort_result(cluster_result_list)
    # print(sorted_result)
    print("number of cluster: " + str(len(sorted_result)))

    for cluster_dict in sorted_result:
        print(str(cluster_dict.__getitem__('size')) + ": " + str(cluster_dict.__getitem__('cluster')))
    pass


# select seed node
def select_seed_node(G):
    list = nx.degree(G)
    print(list)


# sort result on size
def sort_result(cluster_result_list):
    # sort by size at decesding order
    sorted_result = sorted(cluster_result_list, key=lambda e: e.__getitem__('size'), reverse=True)
    return sorted_result
    pass


# Remove a neighbor of the seed
# return new cluster
def remove_neighbor_of_seed(G, cluster, seed):
    current_cluster = cluster
    current_entropy = get_cluster_entropy(G, current_cluster)

    after_removal_cluster = current_cluster
    after_removal_cluster.remove(node)


    pass


# get seed node
def get_seed_node(G):
    pass


# get degree
# return degree
def get_degree(G, node):
    return nx.degree(G, node)
    pass


# get cluster coefficient
# return cluster coefficient
def get_cluster_coefficient(G, node):
    pass


# get cluster entropy
# return entropy
def get_cluster_entropy(G, cluster):
    cluster_entropy = 0
    for node in cluster:
        cluster_entropy += get_vertex_entropy(G, cluster, node)

    return cluster_entropy


# get vertex entropy
# return entropy
def get_vertex_entropy(G, cluster, node):
    inner_link = 0
    outer_link = 0
    for vertex in G.neighbors(node):
        if vertex in cluster:
            inner_link = inner_link+1
        else:
            outer_link = outer_link+1

    pi = inner_link / (inner_link + outer_link)
    po = 1 - pi
    ev = -pi*math.log2(pi) - po*math.log2(po)
    return ev




read_input()