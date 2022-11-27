import numpy as np
# import networkx as nx
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
import plotly.graph_objects as go

from graph_plot import make_annotations
from parameters import *
from ant_trace_simulation import *


# make figure
fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=True,
            showticklabels=False
            )

#fill in layout
fig_dict["layout"]["xaxis"] = axis
fig_dict["layout"]["yaxis"] = axis
fig_dict["layout"]['showlegend']=False 
fig_dict["layout"]["margin"]=dict(l=40, r=40, b=85, t=100)
fig_dict["layout"]["plot_bgcolor"]='rgb(248,248,248)'
fig_dict["layout"]["font_size"]=12
fig_dict["layout"]["annotations"]=make_annotations(new_position, labels,labels,M)
fig_dict["layout"]["hovermode"] = "closest"
fig_dict['layout']["title"] = "Ant trace of {} Ants on {} Tree Nodes".format(N, node_num)
fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
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


#make data
data_dict = {
        "x": Xe,
        "y": Ye,
        "mode": "lines",
        "line": dict(color='rgb(210,210,210)', width=1),
        "hoverinfo":'none'
    }

fig_dict["data"].append(data_dict)

fig_dict["data"].append(go.Scatter(x=Xn,
                  y=Yn,
                  mode='markers',
                  marker=dict(symbol='circle-dot',
                                size=18,
                                color='#6175c1',    # purple
                                line=dict(color='rgb(50,50,50)', width=1)
                                ),
                  text=labels,
                  hoverinfo='text',
                  opacity=0.5
                  ))

ant_node_index = [int(e) for e in ant_trace[0]]
#remain_index = [e for e in range(N_node) if e not in ant_node_index]

fig_dict["data"].append(go.Scatter(x=[Xn[e] for e in ant_node_index],
                  y=[Yn[e] for e in ant_node_index],
                  mode='markers',
                  marker=dict(symbol='circle-dot',
                                size=18,
                                color='#FF5733',    # purple
                                line=dict(color='rgb(50,50,50)', width=1)
                                ),
                  text=labels,
                  hoverinfo='text',
                  opacity=0.5
                  ))


#make frames
for i in range(T):
    frame = {"data": [], "name": str(i)}
    ant_node_index = [int(e) for e in ant_trace[i]] 
    remain_index = [e for e in range(node_num) if e not in ant_node_index]
    
    #plot branches
    data_dict_line = {
        "x": Xe,
        "y": Ye,
        "mode": "lines",
        "line": dict(color='rgb(210,210,210)', width=1),
        "hoverinfo":'none'
    }
    frame["data"].append(data_dict_line)
    
    #plot all the nodes
    data_dict_origin = {
            "x": Xn,
            "y": Yn,
            "mode": 'markers',
            "text": labels,
            "marker": dict(symbol='circle-dot',
                                size=18,
                                color='#6175c1',    #'#DB4551',
                                line=dict(color='rgb(50,50,50)', width=1)
                        ),
            "name": 'bla',
            "hoverinfo":'text',
            "opacity":0.8
        }
    frame["data"].append(data_dict_origin)
    

    #plot the nodes on which ants stay at each time step
    data_dict_ant = dict(x=[Xn[e] for e in ant_node_index],
                  y=[Yn[e] for e in ant_node_index],
                  mode='markers',
                  marker=dict(symbol='circle-dot',
                                size=20,
                                color='#FF5733',    #red
                                line=dict(color='rgb(50,50,50)', width=1)
                                ),
                  text=labels,
                  hoverinfo='text',
                  opacity=0.8
                  )
    frame["data"].append(data_dict_ant)



    fig_dict['frames'].append(frame)
    
    slider_step = {"args": [
        [i],
        {"frame": {"duration": 1, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": i,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)

fig_dict["layout"]["sliders"] = [sliders_dict]







fig = go.Figure(fig_dict)
fig.show()

