from heapq import nlargest
from collections import Counter
import copy
import math
import networkx as nx
import sys
sys.setrecursionlimit(1000000)  # set the maximum depth as 1000000


cluster_node = set()
cluster_result_list = []


# read input and initialize graph
def read_input():
    G = nx.Graph()
    inputFile = open("assignment5_input.txt")
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

    # print(sorted_result)
    #print("number of cluster: " + str(len(sorted_result)))
    sorted_node_list = sort_node(G)

    for seed_node in sorted_node_list:
        #print(seed_node.__getitem__('node'))
        if seed_node.__getitem__('node') not in cluster_node:
            #print(cluster_node)
            #print(seed_node.__getitem__('node'))
            find_cluster(G, seed_node.__getitem__('node'))
            pass
        pass

    sorted_result = sort_result(cluster_result_list)
    #print(cluster_result_list)
    #print(cluster_node)
    #print(added_cluster, iter_added_entropy)
    print("number of cluster: " + str(len(sorted_result)))
    for cluster_dict in sorted_result:
        print(str(cluster_dict.__getitem__('size')) + ": " + str(cluster_dict.__getitem__('cluster')))


# iteratively find cluster
def find_cluster(G, seed_node):
    removed_cluster, iter_remove_entropy = remove_neighbor_of_seed(G, seed_node)
    last_added_cluster, last_iter_added_entropy = add_node_on_outer_boundary(G, removed_cluster)
    new_added_cluster, new_iter_added_entropy = add_node_on_outer_boundary(G, last_added_cluster)

    while new_iter_added_entropy < last_iter_added_entropy:
        last_iter_added_entropy = copy.deepcopy(new_iter_added_entropy)
        new_added_cluster, new_iter_added_entropy = add_node_on_outer_boundary(G, new_added_cluster)

    for node in new_added_cluster:
        cluster_node.add(node)
        pass

    if len(new_added_cluster) > 2:
        cluster_dict = {"cluster": new_added_cluster, "size": len(new_added_cluster)}
        cluster_result_list.append(cluster_dict)

        pass


# sort result on size
def sort_result(cluster_result_list):
    # sort by size at decesding order
    sorted_result = sorted(cluster_result_list, key=lambda e: e.__getitem__('size'), reverse=True)
    return sorted_result
    pass


# Add node on outer boundary
def add_node_on_outer_boundary(G, removed_cluster):
    candidate_node = set()
    for incluster_node in removed_cluster:
        for incluster_node_neighbors in G.neighbors(incluster_node):
            if incluster_node_neighbors not in removed_cluster:
                outcluster_node = incluster_node_neighbors
                candidate_node.add(outcluster_node)  # set remove duplicate neighbors

    sorted_outnode = sort_neighbors(G, candidate_node)
    #print(sorted_outnode)

    current_cluster = copy.deepcopy(removed_cluster)
    current_entropy = get_cluster_entropy(G, current_cluster)

    for neighbors in sorted_outnode:
        after_add_cluster = copy.deepcopy(current_cluster)
        after_add_cluster.add(neighbors.__getitem__('node'))
        after_add_entropy = get_cluster_entropy(G, after_add_cluster)

        if after_add_entropy < current_entropy:
            current_cluster.add(neighbors.__getitem__('node'))
            current_entropy = copy.deepcopy(after_add_entropy)

    #for node in current_cluster:
        #cluster_node.append(node)

    #print(current_cluster)
    return current_cluster, current_entropy



    pass


# Remove a neighbor of the seed
def remove_neighbor_of_seed(G, seed):
    init_cluster = set()
    init_cluster.add(seed)
    for node in G.neighbors(seed):
        init_cluster.add(node)

    sorted_neighbors = sort_neighbors(G, G.neighbors(seed))
    #print(sorted_neighbors)
    #seed_neighbors = G.neighbors(seed)
    #seed_neighbors_degreeView = G.degree(seed_neighbors)
    #seed_neighbors_degreeView_sorted = sort_by_degree(seed_neighbors_degreeView)
    #print(seed_neighbors_degreeView_sorted)

    current_cluster = init_cluster
    current_entropy = get_cluster_entropy(G, current_cluster)

    for neighbors in sorted_neighbors:
        after_removal_cluster = copy.deepcopy(current_cluster)
        after_removal_cluster.remove(neighbors.__getitem__('node'))
        after_removal_entropy = get_cluster_entropy(G, after_removal_cluster)

        if after_removal_entropy < current_entropy:
            current_cluster.remove(neighbors.__getitem__('node'))
            current_entropy = copy.deepcopy(after_removal_entropy)

    #for node in current_cluster:
        #cluster_node.append(node)

    #print(cluster_node)
    return current_cluster, current_entropy
    pass


# sort by degree then by cluster coefficient
def sort_neighbors(G, neighbors):
    node_attribute_list = []
    for node in neighbors:
        degree = nx.degree(G, node)
        cluster_coef = cluster_coefficient(G, node)
        node_dict = {"node": node, "degree": degree, "cluster_coef": cluster_coef}
        node_attribute_list.append(node_dict)

    # [{'node': '1', 'degree': 11, 'cluster_coef': 0.2909090909090909},
    # {'node': '22', 'degree': 11, 'cluster_coef': 0.23636363636363636}],
    sorted_node_list = sorted(node_attribute_list, key=lambda x: (-x.__getitem__("degree"), -x.__getitem__("cluster_coef")))
    return sorted_node_list
    #print(sorted_node_list)


# sort by degree then by cluster coefficient
def sort_node(G):
    node_attribute_list = []
    for node in G.nodes():
        degree = nx.degree(G, node)
        cluster_coef = cluster_coefficient(G, node)
        node_dict = {"node": node, "degree": degree, "cluster_coef": cluster_coef}
        node_attribute_list.append(node_dict)

    # [{'node': '1', 'degree': 11, 'cluster_coef': 0.2909090909090909},
    # {'node': '22', 'degree': 11, 'cluster_coef': 0.23636363636363636}],
    sorted_node_list = sorted(node_attribute_list, key=lambda x: (-x.__getitem__("degree"), -x.__getitem__("cluster_coef")))
    return sorted_node_list
    #print(sorted_node_list)


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
    for node in G.nodes():
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
    if pi == 1 or pi == 0 or po == 0 or po == 1:
        ev = 0
    else:
        ev = -pi*math.log2(pi) - po*math.log2(po)
    return ev


read_input()
