Run ```python3 histogram_animation.py --N=500 --n_nests=5 --connectivity=3 --alpha```

Parameters: 

- N: number of ants
- n_nests: number of nests
- num_nodes: number of nodes in the graph
- connectivity: connectivity of the graph
- theta: pheromone decaying rate (default=0.1, i.e. at each time step, new pheromone = old pheromone * (1-theta))
- alpha: exploitation rate of ants (the probability that ants proceed following pheromone)
- a0: parameter for congestion function (default = 1)
- b: parameter for congestion function
- a1: parameter for congestion function
- a2: parameter for congestion function
- gamma: parameter for congestion function
- gamma1: parameter for congestion function
- gamma2: parameter for congestion function
- T: total number of time steps in the animation




