import numpy as np
from parameters import *
from graph_generator import *
import random
random.seed(2022)

#generate graph
# G, neighbor, nests = geometric_graph(node_num, p_geom, n_nests)

#transition probability per time step
def transition_prob(N_node, neighbor, nests, v, X, alpha, a, b, gamma):
    #v is pheromone level
    P=np.zeros((N_node,N_node)) #initialize transition matrix

    for e in range(N_node):
        if e not in nests:
            for e_prime in neighbor[e]:
                P[e,e_prime]=alpha*(1+v[e_prime])/np.sum((1+v[neighbor[e]]))+(1-alpha)/(len(neighbor[e]))
                # P[e,e_prime]=(1+v[e_prime])/np.sum((1+v[neighbor[e]]))
        
        if e in nests:
            Lambda =np.count_nonzero(X==e)/len(X)
            congestion = 1/(a+b*pow(Lambda,gamma))
            for e_prime in neighbor[e]:
                move = alpha*(1+v[e_prime])/np.sum((1+v[neighbor[e]]))+(1-alpha)/(len(neighbor[e]))
                # move = (1+v[e_prime])/np.sum((1+v[neighbor[e]]))
                P[e,e_prime]=congestion * move 
            
            P[e,e] = 1-congestion            
    
    return P

def simulation(N_node,nests,alpha,a,b,gamma,T):
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
        P = transition_prob(N_node, neighbor, nests, v_prev, X_prev, alpha, a, b, gamma)
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

# v_seq, eta_seq, ant_trace = simulation(N_node,source_nodes, v0,eta0,children,parent,
#                                        X0,alpha,beta,a0,b,a1,a2,gamma,gamma1,gamma2,
#                                        T)