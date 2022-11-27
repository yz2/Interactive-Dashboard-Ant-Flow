import networkx as nx
import plotly.graph_objects as go
from parameters import *
import random
random.seed(2022)
seed = 2022
import scipy as sp
import scipy.sparse  # call as sp.sparse


#geometric random graph
def graph_generator(N_node=node_num, n_nests=3):

    # G = nx.random_geometric_graph(node_num, p_geom) #generate random geometric graph
    # G = nx.hypercube_graph(8)
    # N_node = 2**8
    # G = nx.random_k_out_graph(n=N_node, k=K, alpha=alpha_val, self_loops=True, seed=None)
    # G = nx.dorogovtsev_goltsev_mendes_graph(N_node)
    # A = sp.sparse.eye(N_node, N_node, 10)
    # G = nx.from_scipy_sparse_matrix(A)

    # G = nx.star_graph(N_node-1) #impossible
    # G = nx.turan_graph(N_node, 10)
    # G = nx.grid_graph(dim=(range(0, 10), range(0, 5)))
    # G = nx.fast_gnp_random_graph(N_node, p=0.2)
    # G = nx.hypercube_graph(10)
    # G = nx.krackhardt_kite_graph()

    #two graphs to experiment on now:
    # G = nx.connected_watts_strogatz_graph(N_node, k=3, p=0.3, tries=100, seed=None)
    G = nx.gnm_random_graph(n=N_node, m=2*N_node, seed=seed)
    neighbor = dict() #neighbor dictionary to store the neighbors of each node
    

    for edge in G.edges():
        if (edge[0] in neighbor.keys())&(edge[1] in neighbor.keys()):
            neighbor[edge[0]].append(edge[1])
            neighbor[edge[1]].append(edge[0])
        elif ((edge[0] in neighbor.keys())) & (not (edge[1] in neighbor.keys())):
            neighbor[edge[0]].append(edge[1])
            neighbor[edge[1]] = [edge[0]]
        elif ((edge[1] in neighbor.keys())) & (not (edge[0] in neighbor.keys())):
            neighbor[edge[1]].append(edge[0])
            neighbor[edge[0]] = [edge[1]]
        else:
            neighbor[edge[0]] = [edge[1]]
            neighbor[edge[1]] = [edge[0]]
    
    #sample source nodes uniformly on the graph: (number: n_source)
    all_nodes = list(range(N_node))
    nests = random.sample(all_nodes, n_nests)
    return G, neighbor, nests

G, neighbor, nests = graph_generator(node_num, n_nests)
    

   