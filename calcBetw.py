from heapq import nlargest
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
    calc_and_cut_max_betweenness(G)
    # print(nx.number_connected_components(G))
    # print(nx.is_connected(G))
    # print(list(get_subgraph_component(G)))
    # calc_and_cut_max_betweenness(G)
    # nx.density(G)
    sorted_result = sort_result(cluster_result_list)
    # print(sorted_result)
    print("number of cluster: " + str(len(sorted_result)))

    for cluster_dict in sorted_result:
        print(str(cluster_dict.__getitem__('size')) + ": " + str(cluster_dict.__getitem__('cluster')))
    pass


# get subgraph component
def get_subgraph_component(G):
    #print(G.number_of_nodes())  # 5606
    #sub = (G.subgraph(c).copy() for c in nx.connected_components(G))
    #print(list(sub))
    #print(nx.number_connected_components(G))
    for c in nx.connected_components(G):
        subGraph = G.subgraph(c).copy()
        #print(nx.number_connected_components(subGraph))
        #print(subGraph.number_of_nodes())  # 5606
        #print("\n")
        #print(list(subGraph))
        get_cluster(subGraph)
        pass
    #print("sssss")
    pass


# check if graph is connected
def is_connected(G):
    return nx.is_connected(G)
    pass


# get cluster
def get_cluster(subGraph):
    if get_density(subGraph) >= 0.65 and number_of_nodes(subGraph) > 2:
        cluster_list = list(subGraph)  # look if correct
        cluster_size = subGraph.number_of_nodes()
        cluster_dict = {"cluster": cluster_list, "size": cluster_size}
        cluster_result_list.append(cluster_dict)
        #print(cluster_result_list)
        #print(cluster_result_list[0].__getitem__('size'))
        #print(cluster_result_list[0].__getitem__('cluster'))
    if get_density(subGraph) < 0.65 and number_of_nodes(subGraph) > 2:  # recursively cut
        #print(list(subGraph))
        calc_and_cut_max_betweenness(subGraph)
    pass


# sort result on size
def sort_result(cluster_result_list):
    # sort by size at decesding order
    sorted_result = sorted(cluster_result_list, key=lambda e: e.__getitem__('size'), reverse=True)
    return sorted_result
    pass


# calc and remove max betweenness
# return betweenness dictionary
# dictionary of edges with betweenness as the value. Ex: {('YBR160W', 'YBR135W'): 26754.0707,
def calc_and_cut_max_betweenness(G):
    betw_dict = calc_edge_betweenness(G)
    cut_max_betweeness_edge(G, betw_dict)

    if is_connected(G):
        calc_and_cut_max_betweenness(G)
    else:
        get_subgraph_component(G)  # get subgraph after cutting edge
    #return betw_dict
    pass


# find max betw edge
# return the edge with two nodes edge[0], edge[1]
def cut_max_betweeness_edge(G, betw_dict):

    max_edge = max(betw_dict.items(), key=lambda x: x[1])
    #print(max_edge)

    #for max_edge in betw_dict.items():


    #max_edge = max(betw_dict.items(), key=lambda e: e[1])
    #sorted_betw = sorted(betw_dict.items(), key=lambda x: x[1], reverse=True)  # sort betw(value) by descending order
    #print(sorted_betw)
    #print(max_edge)
    remove_max_edge(G, max_edge[0])
    '''
    for index, val in enumerate(sorted_betw):
        if is_connected(G):
            remove_max_edge(G, sorted_betw[index][0])  # tuple('YBR160W', 'YBR135W')
    '''
    pass


# remove edge of the greatest betweennes
# return the graph after cutting
def remove_max_edge(G, edge):
    #print(G.number_of_edges())
    G.remove_edge(edge[0], edge[1])
    #print(edge[0], edge[1])
    #print(G.number_of_edges())
    #get_subgraph_component(G)  # get subgraph after cutting edge
    #return G
    pass


# calc edge betweenness
def calc_edge_betweenness(G):

    betweenness = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    # b[e]=0 for e in G.edges()
    betweenness.update(dict.fromkeys(G.edges(), 0.0))
    nodes = G
    for s in nodes:
        # partial betweeneess
        S, P, sigma = bfs_shortest_path(G, s)
        # accumulate betweeneess
        betweenness = accumulate_betweenness(betweenness, S, P, sigma, s)
    for n in G:  # remove nodes to only return edges
        del betweenness[n]
    return betweenness  # Dictionary of edges with betweenness as the value. Ex: {('YBR160W', 'YBR135W'): 26754.0707,
    pass


# bfs for partial betweenness
def bfs_shortest_path(G, s):
    S = []  # empty stack
    P = {}  # empty list
    for v in G:
        P[v] = []
    sigma = dict.fromkeys(G, 0.0)    # sigma[v]=0 for v in G
    D = {}
    sigma[s] = 1.0
    D[s] = 0
    Q = [s]  # enqueue s → Q
    while Q:   # use BFS to find shortest paths
        v = Q.pop(0)  # dequeue v ← Q
        S.append(v)   # push v → S
        Dv = D[v]
        sigmav = sigma[v]
        for w in G[v]:
            if w not in D:
                Q.append(w)
                D[w] = Dv + 1
            if D[w] == Dv + 1:   # this is a shortest path, count paths
                sigma[w] += sigmav
                P[w].append(v)  # predecessors
    return S, P, sigma
    pass


# accumulate betweenness
def accumulate_betweenness(betweenness, S, P, sigma, s):
    delta = dict.fromkeys(S, 0)
    while S:  # while S not empty do
        w = S.pop()  # pop w ← S
        coeff = (1 + delta[w]) / sigma[w]
        for v in P[w]:
            c = sigma[v] * coeff
            if (v, w) not in betweenness:
                betweenness[(w, v)] += c
            else:
                betweenness[(v, w)] += c
            delta[v] += c
        if w != s:
            betweenness[w] += delta[w]
    return betweenness
    pass


# calc density
# return density value
def get_density(G):
    n = number_of_nodes(G)
    m = number_of_edges(G)
    if m == 0 or n <= 1:
        return 0
    d = m / (n * (n - 1))
    d *= 2
    return d
    pass


# number of nodes
def number_of_nodes(G):
    return G.number_of_nodes()
    pass


# number of edges
def number_of_edges(G):
    return G.number_of_edges()
    pass


read_input()
#Gtest = nx.random_graphs.barabasi_albert_graph(100,3)
#T = calc_edge_betweenness(Gtest)
#print(T)
