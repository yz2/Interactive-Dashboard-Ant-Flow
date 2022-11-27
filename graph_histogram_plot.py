import igraph
from igraph import Graph, EdgeSeq
from parameters import *
from graph_generator import *

    #nr_vertices = N_node - 1

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

def make_annotations(pos, text, labels, M, font_size=10, font_color='rgb(250,250,250)'):
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
    
    for k in nests:
        annotations.append(
            dict(
                text=labels[k],
                x=pos[k][0], y=2*M-pos[k][1],
                xref='x1', yref='y1',
                font=dict(color='green', size=font_size)
            )
        )
        
    return annotations


