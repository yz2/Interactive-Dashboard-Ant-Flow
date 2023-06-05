import networkx as nx
from graph import *
# from networkx import hnm_harary_graph
import igraph
import numpy as np
import random
seed = 2022

#generate random graph
def graph_generator(N_node, n_nests,connectivity):
    # G = nx.gnm_random_graph(n=N_node, m=int(1.5*N_node), seed=seed)
    # G = hnm_harary_graph(n=N_node, m=N_node)
    # G =nx.erdos_renyi_graph(100, 0.5, seed=123, directed=False)
    # G = nx.connected_caveman_graph(4,20)
    G = hkn_harary_graph(connectivity, N_node, create_using=None)
    # connectivity = nx.edge_connectivity(G)
    node_num = G.number_of_nodes()
    # G = nx.hkn_harary_graph(k=3,n=N_node)
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
    all_nodes = list(range(node_num))
    nests = random.sample(all_nodes, n_nests)
    return G, neighbor, nests, node_num

#plot random graph
def graph_structure(N_node, G):
    nr_vertices = N_node 
    G_igraph = igraph.Graph.from_networkx(G)
    lay = G_igraph.layout('rt')
    position = {k: lay[k] for k in range(N_node)}
    
    v_label = list(map(str, range(nr_vertices)))

    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    # es = EdgeSeq(G_igraph) # sequence of edges
    E = [e.tuple for e in G_igraph.es] # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2*M-position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe+=[position[edge[0]][0], position[edge[1]][0], None]
        Ye+=[2*M - position[edge[0]][1],2*M-position[edge[1]][1], None]

    labels = v_label
    
    return Xe, Ye, Xn, Yn, labels, M, position

def make_annotations(pos, text, labels, M, nests, font_size=10, font_color='rgb(250,250,250)'):
    L=len(pos)
    if len(text)!=L:
        raise ValueError('The lists pos and text must have the same len')
    annotations = []

    for k in range(L):
        annotations.append(
            dict(
                text=labels[k], # or replace labels with a different list for the text within the circle
                x=pos[k][0], y=2*M-pos[k][1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
        annotations.append(
            dict(
                text=labels[k], # or replace labels with a different list for the text within the circle
                x=pos[k][0], y=2*M-pos[k][1],
                xref='x3', yref='y3',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    
    for k in nests:
        annotations.append(
            dict(
                text=labels[k],
                x=pos[k][0], y=2*M-pos[k][1],
                xref='x1', yref='y1',
                font=dict(color='green', size=font_size)
            )
        )
        annotations.append(
            dict(
                text=labels[k],
                x=pos[k][0], y=2*M-pos[k][1],
                xref='x3', yref='y3',
                font=dict(color='green', size=font_size)
            )
        )
        
    return annotations

def transition_prob(N_node, neighbor, nests, v, X, alpha, a, b, gamma,theta):
    #v is pheromone level
    eta = v * theta
    P=np.zeros((N_node,N_node)) #initialize transition matrix
    for e in range(N_node):
        if e not in nests:
            for e_prime in neighbor[e]:
                P[e,e_prime]=alpha*(1+v[e_prime])/np.sum((1+v[neighbor[e]]))+(1-alpha)/(len(neighbor[e]))
                # P[e,e_prime]=(1+v[e_prime])/np.sum((1+v[neighbor[e]]))
        
        if e in nests:
            # Lambda =np.count_nonzero(X==e)/len(X)
            Lambda = eta[e]
            congestion = 1/(a+b*pow(Lambda,gamma))
            for e_prime in neighbor[e]:
                move = alpha*(1+v[e_prime])/np.sum((1+v[neighbor[e]]))+(1-alpha)/(len(neighbor[e]))
                # move = (1+v[e_prime])/np.sum((1+v[neighbor[e]]))
                P[e,e_prime]=congestion * move 
            
            P[e,e] = 1-congestion            
    
    return P

def simulation(N_node,nests,alpha,a,b,gamma,T,N,neighbor,theta):
    v_seq = []
    eta_seq = []
    ant_trace = []
    
    #initial population is distributed randomly at nests
    #each ant uniformly "selects" which nest to start
    X0 = random.choices(nests, weights = [1]*len(nests), k = N)#sample with replacement
    
    #initial pheromone level is uniform at nests
    v0=np.zeros(N_node)
    v0[nests]=1/len(nests)
    eta0 = v0
    

    v_prev = v0
    eta_prev = eta0
    v_seq.append(v0)
    eta_seq.append(eta0)
    ant_trace.append(X0)
    
    X_prev = X0 #the position of ants at some time step
    eta_new = np.zeros(len(eta_prev))
    v_new = np.zeros(len(v_prev))
    
    for n in range(T):
        #obtain transition probability matrix
        # P = transition_prob(N_node, neighbor, nests, v_prev, X_prev, alpha, a, b, gamma)
        P = transition_prob(N_node, neighbor, nests, v_prev, X_prev, alpha, a, b, gamma,theta)
        X_new = np.zeros(len(X_prev))
        # X records the positions of each ant at each time step
        rng = np.random.default_rng()
        for i in range(len(X_prev)):
            e = int(X_prev[i])
            X_new[i]=np.nonzero(rng.multinomial(1, P[e], size=1)[0])[0][0]
        
        for e in range(N_node):
            #eta is the population distribution
            #eta_new[e] = np.count_nonzero(X_new==e)/len(X_new)
            # recursive model: 
            eta_new[e] = np.dot(eta_prev,P[:,e])
            v_new[e] = (1-theta)*v_prev[e]+eta_new[e]
        
        #print(eta_new)

        eta_seq.append(eta_new.copy())
        v_seq.append(v_new.copy())
        ant_trace.append(X_new.copy())
        
        eta_prev = eta_new.copy()
        v_prev = v_new.copy()
        X_prev = X_new.copy()
        
        
    return v_seq, eta_seq, ant_trace

   
