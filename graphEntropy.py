from heapq import nlargest
from collections import Counter
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
    #select_seed_node(G)
    #print(cluster_coefficient(G))
    #get_degree(G)
    #sorted_result = sort_result(cluster_result_list)
    # print(sorted_result)
    #print("number of cluster: " + str(len(sorted_result)))
    sort_node(G)

    #for cluster_dict in sorted_result:
     #   print(str(cluster_dict.__getitem__('size')) + ": " + str(cluster_dict.__getitem__('cluster')))
    #pass


# select seed node
def select_seed_node(G):
    node_degree_list = nx.degree(G)
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

    #for node in G.neighbors(seed):
    seed_neighbors = G.neighbors(seed)
    seed_neighbors_degreeView = G.degree(seed_neighbors)
    seed_neighbors_degreeView_sorted = sort_by_degree(seed_neighbors_degreeView)
    print(seed_neighbors_degreeView_sorted)

    #for node in seed_neighbors_degreeView_sorted

    current_cluster = cluster
    current_entropy = get_cluster_entropy(G, current_cluster)

    after_removal_cluster = current_cluster
    after_removal_cluster.remove(node)


    pass


# sort by degree then by cluster coefficient
def sort_node(G):
    node_attribute_list = []
    for node in G.nodes():
        degree = nx.degree(G, node)
        cluster_coef = cluster_coefficient(G, node)
        node_dict = {"node": node, "degree": degree, "cluster_coef": cluster_coef}
        node_attribute_list.append(node_dict)

    sorted_node_list = sorted(node_attribute_list, key=lambda x: (-x.__getitem__("degree"), -x.__getitem__("cluster_coef")))

    print(sorted_node_list)


# get seed node
def get_seed_node(G):
    pass


# get degree
# return degree
def get_degree(G, node):
    return nx.degree(G, node)
    pass


# sort by degree
def sort_by_degree(nd_view):
    sorted_degree = sorted(nd_view, key=lambda x: x[1], reverse=True)
    # print(sorted_degree)  # [('1', 11), ('22', 11), ('2', 10), ('15', 9),
    return sorted_degree
    pass


# get cluster coefficient
# return cluster coefficient
def cluster_coefficient(G, nodes=None):
    td_iter = count_triangle(G, nodes)
    clusterc = {v: 0 if t == 0 else t / (d * (d - 1)) for
                v, d, t, _ in td_iter}

    if nodes in G:
        # Return the value of the sole entry in the dictionary.
        return clusterc[nodes]
    return clusterc


# number of triangle in neighbors
def count_triangle(G, nodes=None):
    if nodes is None:
        nodes_nbrs = G.adj.items()
    else:
        nodes_nbrs = ((n, G[n]) for n in G.nbunch_iter(nodes))

    for v, v_nbrs in nodes_nbrs:
        vs = set(v_nbrs) - {v}
        gen_degree = Counter(len(vs & (set(G[w]) - {w})) for w in vs)
        ntriangles = sum(k * val for k, val in gen_degree.items())
        yield (v, len(vs), ntriangles, gen_degree)


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