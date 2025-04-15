# Additional Imports for Dash
import argparse
import os
import random

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash import Dash
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

from functions import *
from graph import *

# from dash.dependencies import Input, Output

random.seed(2022)

# ... (keep your existing imports and other code)

# Remove the argparse section since we're using Dash for input
# Also remove the fig.show() since we'll display the figure in Dash

# Initialize the Dash app
app = Dash(__name__)

# Define the app layout
app.layout = html.Div(
    [
        html.H1("Ant Flow Visualization"),
        html.Div(
            [
                html.Label("Node Number:"),
                dcc.Input(id="input-node-number", type="number", value=20),
                html.Label("Number of Nests:"),
                dcc.Input(id="input-n-nests", type="number", value=5),
                html.Label("Connectivity:"),
                dcc.Input(id="input-connectivity", type="number", value=4),
                html.Label("Number of Ants:"),
                dcc.Input(id="input-N", type="number", value=500),
                html.Label("Pheromone Decaying Rate (Theta):"),
                dcc.Input(id="input-theta", type="number", value=0.1),
                html.Label("Exploitation Probability (Alpha):"),
                dcc.Input(id="input-alpha", type="number", value=0.85),
                html.Label("value of a0:"),
                dcc.Input(id="input-a0", type="number", value=1),
                html.Label("value of b"),
                dcc.Input(id="input-b", type="number", value=23),
                html.Label("value of gamma"),
                dcc.Input(id="input-gamma", type="number", value=1),
                html.Label("total time steps"),
                dcc.Input(id="input-T", type="number", value=500),
                html.Button("Submit", id="submit-button"),
            ]
        ),
        dcc.Graph(id="animated-graph"),
    ]
)


@app.callback(
    Output("animated-graph", "figure"),
    [
        Input("submit-button", "n_clicks"),
        Input("input-node-number", "value"),
        Input("input-n-nests", "value"),
        Input("input-connectivity", "value"),
        Input("input-N", "value"),
        Input("input-theta", "value"),
        Input("input-alpha", "value"),
        Input("input-a0", "value"),
        Input("input-b", "value"),
        Input("input-gamma", "value"),
        Input("input-T", "value"),
    ],
)
def update_graph(
    n_clicks, node_number, n_nests, connectivity, N, theta, alpha, a0, b, gamma, T
):
    # The previously provided code for generating the figure goes here.
    # Make sure to return the fig at the end.
    # if n_clicks == 0:
    #     return dash.no_update  # Do nothing if button wasn't clicked yet
    fig = generate_animation(
        node_number, n_nests, connectivity, N, theta, alpha, a0, b, gamma, T
    )
    return fig


def generate_animation(
    node_number, n_nests, connectivity, N, theta, alpha, a0, b, gamma, T
):
    # ... (your code for generating the figure using the provided values)
    G, neighbor, nests, node_num = graph_generator(
        N_node=node_number, n_nests=n_nests, connectivity=connectivity
    )

    Xe, Ye, Xn, Yn, labels, M, new_position = graph_structure(node_num, G)

    v_seq, eta_seq, ant_trace = simulation(
        node_num, nests, alpha, a0, b, gamma, T, N, neighbor, theta
    )

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Population Distribution",
            "Barplot of Population",
            "Pheromone Distribution",
            "Barplot of Pheromone",
        ),
    )

    axis = dict(
        showline=False,  # hide axis line, grid, ticklabels and  title
        zeroline=False,
        showgrid=True,
        showticklabels=False,
    )

    axis2 = dict(
        showline=True,  # hide axis line, grid, ticklabels and  title
        zeroline=True,
        showgrid=True,
        showticklabels=True,
    )
    # fill in layout
    fig.update_layout(
        xaxis1=axis,
        yaxis1=axis,
        xaxis2=axis2,
        yaxis2=axis2,
        xaxis3=axis,
        yaxis3=axis,
        xaxis4=axis2,
        yaxis4=axis2,
        showlegend=False,
        margin=dict(l=40, r=40, b=85, t=100),
        plot_bgcolor="rgb(248,248,248)",
        font_size=12,
        annotations=make_annotations(new_position, labels, labels, M, nests),
        hovermode="closest",
        title="{} Ants, {} Tree Nodes, Nests: {}, connectivity: {}".format(
            N, node_num, nests, connectivity
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=Xe,
            y=Ye,
            mode="lines",
            line=dict(color="rgb(210,210,210)", width=1),
            hoverinfo="none",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=Xn,
            y=Yn,
            mode="markers",
            marker={
                "sizemode": "area",
                "sizeref": 1e-4,
                "size": eta_seq[0],
                "color": eta_seq[0],
            },
            text=labels,
            hoverinfo="text",
            opacity=0.5,
        ),
        row=1,
        col=1,
    )

    # add initial trace to the histogram plot
    ### histogram of initial population distribution
    eta_df = pd.DataFrame(eta_seq[0])
    eta_df["node"] = eta_df.index
    eta_df = eta_df.rename({0: "pop"}, axis=1)

    fig.add_trace(
        go.Bar(
            x=eta_df["node"],
            y=eta_df["pop"],
            name="Population Density",
            marker_color=eta_df["pop"],
        ),
        row=1,
        col=2,
    )

    # add initial traces to subplot of pheromone
    fig.add_trace(
        go.Scatter(
            x=Xe,
            y=Ye,
            mode="lines",
            line=dict(color="rgb(210,210,210)", width=1),
            hoverinfo="none",
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=Xn,
            y=Yn,
            mode="markers",
            marker={
                "sizemode": "area",
                "sizeref": 1e-3,
                "size": v_seq[0],
                "color": v_seq[0],
            },
            text=labels,
            hoverinfo="text",
            opacity=0.5,
        ),
        row=2,
        col=1,
    )

    # add initial trace to the histogram plot
    ### histogram of initial population distribution
    v_df = pd.DataFrame(v_seq[0])
    v_df["node"] = v_df.index
    v_df = v_df.rename({0: "pop"}, axis=1)

    fig.add_trace(
        go.Bar(
            x=v_df["node"],
            y=v_df["pop"],
            name="Pheromone Density",
            marker_color=v_df["pop"],
        ),
        row=2,
        col=2,
    )

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Time:",
            "visible": True,
            "xanchor": "right",
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": [],
    }

    # make frames
    frames = []
    for i in range(T):
        frame = {"data": [], "name": str(i), "traces": [0, 1, 2, 3, 4, 5, 6, 7]}
        ant_node_index = [int(e) for e in ant_trace[i]]
        remain_index = [e for e in range(node_num) if e not in ant_node_index]

        # frame for population on the graph
        # frame["data"].append(data_dict_tree)
        frame["data"].append(
            go.Scatter(
                x=Xe,
                y=Ye,
                mode="lines",
                line=dict(color="rgb(210,210,210)", width=1),
                hoverinfo="none",
            )
        )

        frame["data"].append(
            go.Scatter(
                x=Xn,
                y=Yn,
                mode="markers",
                marker={
                    "sizemode": "area",
                    "sizeref": 1e-4,
                    "size": eta_seq[i],
                    "color": eta_seq[i],
                },
                text=labels,
                hoverinfo="text",
                opacity=0.8,
            )
        )

        # eta (population) for time step i
        eta_df_temp = pd.DataFrame(eta_seq[i])
        eta_df_temp["node"] = eta_df_temp.index
        eta_df_temp = eta_df_temp.rename({0: "pop"}, axis=1)

        frame["data"].append(
            go.Bar(
                x=eta_df_temp["node"],
                y=eta_df_temp["pop"],
                name="Population Density",
                marker_color=eta_df_temp["pop"],
                opacity=0.8,
            )
        )

        # frame for population on the graph
        # frame["data"].append(data_dict_tree)
        frame["data"].append(
            go.Scatter(
                x=Xe,
                y=Ye,
                mode="lines",
                line=dict(color="rgb(210,210,210)", width=1),
                hoverinfo="none",
            )
        )

        frame["data"].append(
            go.Scatter(
                x=Xn,
                y=Yn,
                mode="markers",
                marker={
                    "sizemode": "area",
                    "sizeref": 1e-3,
                    "size": v_seq[i],
                    "color": v_seq[i],
                },
                text=labels,
                hoverinfo="text",
                opacity=0.8,
            )
        )

        # eta (population) for time step i
        v_df_temp = pd.DataFrame(v_seq[i])
        v_df_temp["node"] = v_df_temp.index
        v_df_temp = v_df_temp.rename({0: "pop"}, axis=1)

        frame["data"].append(
            go.Bar(
                x=v_df_temp["node"],
                y=v_df_temp["pop"],
                name="Pheromone Level",
                marker_color=v_df_temp["pop"],
                opacity=0.8,
            )
        )

        frames.append(frame)

        slider_step = {
            "args": [
                [i],
                {
                    "frame": {"duration": 20, "redraw": True},
                    "mode": "immediate",
                    "transition": {"duration": 500},
                },
            ],
            "label": i,
            "method": "animate",
        }
        sliders_dict["steps"].append(slider_step)

    updatemenus = [
        {
            "buttons": [
                {
                    "args": [
                        None,
                        {
                            "frame": {"duration": 300, "redraw": False},
                            "fromcurrent": True,
                            "transition": {
                                "duration": 300,
                                "easing": "quadratic-in-out",
                            },
                        },
                    ],
                    "label": "Play",
                    "method": "animate",
                },
                {
                    "args": [
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0},
                        },
                    ],
                    "label": "Pause",
                    "method": "animate",
                },
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top",
        }
    ]

    sliders = [sliders_dict]

    fig.update(frames=frames),
    fig.update_layout(updatemenus=updatemenus, bargap=0.2, sliders=sliders)

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)
