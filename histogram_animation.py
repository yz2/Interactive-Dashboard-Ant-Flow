import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import plotly.express as px
#import igraph
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from graph_histogram_plot import *
from graph_generator import *
from parameters import *
from ant_trace_simulation import *
import pandas as pd
from histogram_data import *


fig = make_subplots(rows=1, cols=2, subplot_titles = ('Population Distribution','Barplot of Population'))

axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=True,
            showticklabels=False
            )

axis2 = dict(showline=True, # hide axis line, grid, ticklabels and  title
            zeroline=True,
            showgrid=True,
            showticklabels=True
            )

#fill in layout
fig.update_layout(xaxis1= axis,
                  yaxis1=axis,
                  xaxis2=axis2,
                  yaxis2=axis2,
                  showlegend = False,
                  margin = dict(l=40, r=40, b=85, t=100),
                  plot_bgcolor = 'rgb(248,248,248)',
                  font_size = 12,
                  annotations = make_annotations(new_position,labels,labels,M),
                  hovermode = "closest",
                  title = "{} Ants, {} Tree Nodes, Nests: {}".format(N, node_num, nests)
                  )
                

#add initial traces to subplot of population
fig.add_trace(go.Scatter(x=Xe,
         y=Ye,
         mode = "lines",
         line = dict(color='rgb(210,210,210)', width=1),
         hoverinfo = 'none'), row=1, col=1)

fig.add_trace(go.Scatter(x=Xn,
                  y=Yn,
                  mode='markers',
                  marker={
                    "sizemode": "area",
                    "sizeref": 1e-4,
                    "size": eta_seq[0],
                    "color":eta_seq[0]
                  },
                  text=labels,
                  hoverinfo='text',
                  opacity=0.5,
                  ), row=1, col=1)



#add initial trace to the histogram plot
### histogram of initial population distribution
eta_df = pd.DataFrame(eta_seq[0])
eta_df['node']=eta_df.index
eta_df = eta_df.rename({0:'pop'},axis=1)

fig.add_trace(go.Bar(x=eta_df['node'], 
                    y=eta_df['pop'], name='Population Density', 
                    marker_color = eta_df['pop']),row=1, col=2)


sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Time:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

#make frames
frames = []
for i in range(T):
    frame = {"data": [], "name": str(i), "traces": [0,1,2]}
    ant_node_index = [int(e) for e in ant_trace[i]] 
    remain_index = [e for e in range(node_num) if e not in ant_node_index]
    
    #plot branches
    data_dict_tree = {
        "x": Xe,
        "y": Ye,
        "mode": "lines",
        "line": dict(color='rgb(210,210,210)', width=1),
        "hoverinfo":'none'
    }
    
    
    #plot all the nodes "proportional" to the population level
    data_dict_pop = dict(x=Xn,
                  y=Yn,
                  mode='markers',
                  marker={
                    "sizemode": "area",
                    "sizeref": 1e-4,
                    "size": eta_seq[i],
                    "color":eta_seq[i]
                  },
                  text=labels,
                  hoverinfo='text',
                  opacity=0.8
                  )

    #frame for population on the graph
    # frame["data"].append(data_dict_tree)
    frame["data"].append(go.Scatter(x=Xe,
         y=Ye,
         mode = "lines",
         line = dict(color='rgb(210,210,210)', width=1),
         hoverinfo = 'none'))

    # frame["data"].append(data_dict_pop)
    frame["data"].append(go.Scatter(x=Xn,
                  y=Yn,
                  mode='markers',
                  marker={
                    "sizemode": "area",
                    "sizeref": 1e-4,
                    "size": eta_seq[i],
                    "color": eta_seq[i]
                  },
                  text=labels,
                  hoverinfo='text',
                  opacity=0.8))

    #eta (population) for time step i              
    eta_df_temp = pd.DataFrame(eta_seq[i])
    eta_df_temp['node']=eta_df_temp.index
    eta_df_temp = eta_df_temp.rename({0:'pop'},axis=1)
    
    frame["data"].append(go.Bar(x=eta_df_temp['node'], 
                    y=eta_df_temp['pop'], name='Population Density', 
                    marker_color = eta_df_temp['pop'], opacity=0.8))

    
    
    frames.append(frame)
   
    
    slider_step = {"args": [
        [i],
        {"frame": {"duration": 20, "redraw": True},
         "mode": "immediate",
         "transition": {"duration": 500}}
    ],
        "label": i,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)

# fig_dict["layout"]["sliders"] = [sliders_dict]

updatemenus  = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 300, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }
]

sliders = [sliders_dict]

fig.update(frames=frames),
fig.update_layout(updatemenus=updatemenus,
                  bargap=0.2,
                  sliders=sliders)
fig.show() 


# fig = go.Figure(fig_dict)
# fig.show()

