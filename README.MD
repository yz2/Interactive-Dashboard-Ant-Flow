Guidance:

1. Run ```Python3 app.py``` in terminal

2. copy and paste the address after "Running on", for example you may see (where 'x' are numbers)

  ```Running on http://xxx.x.x.x:xxxx```

  then you copy and paste ```http://xxx.x.x.x:xxxx``` in your browser and then you can see the interactive visualization of ant flow. 

Parameters: 

- N: number of ants (default = 500)
- n_nests: number of nests (default = 5)
- num_nodes: number of nodes in the graph (default = 20)
- connectivity: connectivity of the graph (default = 3)
- theta: pheromone decaying rate (default=0.1, i.e. at each time step, new pheromone = old pheromone * (1-theta))
- alpha: exploitation rate of ants (the probability that ants proceed following pheromone)
- a: parameter for congestion function (default = 1)
- b: parameter for congestion function (default = 23)
- gamma: parameter for congestion function (default = 1)
- T: total number of time steps in the animation (default = 500)




