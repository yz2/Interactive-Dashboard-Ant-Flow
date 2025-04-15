Interactive Dashboard for ant flow visualization: simulating large population of ant trails.

## Getting Started

### 1. Install dependencies

Make sure you have Python 3.8+ and pip installed. Then, in your project directory, run:

```bash
pip install streamlit plotly networkx igraph pandas
```

### 2. Launch the Streamlit app

From your project directory, run:

```bash
streamlit run app.py
```

### 3. Open the app in your browser

After running the above command, Streamlit will display a local URL in the terminal, typically:

```
Local URL: http://localhost:8501
```

Open that address in your browser to use the interactive ant flow visualization dashboard.

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




