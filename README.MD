Run ```python3 histogram_animation.py --N=500 --n_nests=5 --connectivity=3 --alpha=0.85 --theta=0.1```

Parameters: 

- N: number of ants (default = 500)
- n_nests: number of nests (default = 5)
- num_nodes: number of nodes in the graph (default = 20)
- connectivity: connectivity of the graph (default = 3)
- theta: pheromone decaying rate (default=0.1, i.e. at each time step, new pheromone = old pheromone * (1-theta))
- alpha: exploitation rate of ants (the probability that ants proceed following pheromone)
- a0: parameter for congestion function (default = 1)
- b: parameter for congestion function (default = 23)
- gamma: parameter for congestion function (default = 1)
- T: total number of time steps in the animation (default = 500)




