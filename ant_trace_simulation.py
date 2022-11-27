from graph_generator import *
from ant_flow_MC import *
from graph_histogram_plot import *
from parameters import *


v_seq, eta_seq, ant_trace = simulation(node_num,nests,alpha,a0,b,gamma,T)

Xe, Ye, Xn, Yn, labels, M, new_position = graph_structure(node_num, G)

# annotations = make_annotations(new_position,labels,labels,M)
# print(annotations[0])

