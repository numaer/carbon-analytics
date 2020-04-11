import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

# Custom Team NYC imports
from util.helpers import *
from util import map_helpers
from views import filter, header, metrics, co2_scatter
from views import map as map_view
from model.trips import Trips

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", 
                          "content": "width=device-width"}]
)
server = app.server

# Load data
trips = Trips(DATA_PATH) 

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Hub and Spoke CO2 Map",
)

# Create app layout
"""
Configuration for entire dashboard layout. Pulls in figures from functions modularized from
the views/ directory.
"""
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        header.get_header(),
        html.Div([metrics.get_metrics(),
                 filter.get_filter(trips)],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="individual_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

# Create callbacks
"""
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("count_graph", "figure")],
)
"""

@app.callback(
    [
        Output("well_text", "children"),
        Output("gasText", "children"),
        Output("oilText", "children"),
        Output("waterText", "children"),
    ],
    [Input("vessel_types", "value")],
)
def update_metrics(vessel_types):
    def agg_metrics(df_full_trips):
        df = df_full_trips 
        data = {
            'number_of_trips': len(df_full_trips),
            'number_of_hubs': len(set(df_full_trips['StartHUBPORT_PortID'].unique()).union(
                                set(df_full_trips['ENDHUBPORT_PortID'].unique()))),
            'actual_co2_emission': 1337,
            'optimized_co2_emission': 337
        }

        return data
    df_full_trips = trips.get_trips()
    df_full_trips = df_full_trips[df_full_trips['VesselType'].isin(vessel_types)]
    metrics = agg_metrics(df_full_trips)
    return metrics['number_of_trips'], metrics['number_of_hubs'], metrics['actual_co2_emission'], metrics['optimized_co2_emission']


# Selectors -> main graph
@app.callback(
    Output("main_graph", "figure"),
    [
        Input("zone_types", "value"),
        Input("vessel_types", "value"),
        Input("cluster_slider", "value"),
    ],
    [State("main_graph", "relayoutData")],
)
def make_main_figure(
    zone_types, vessel_types, cluster_slider, main_graph_layout
):
    df_full_trips = trips.get_trips()
    df_full_trips = df_full_trips[df_full_trips['VesselType'].isin(vessel_types)]
    figure = map_view.gen_map(df_full_trips)
    return figure


# Main graph -> individual graph
@app.callback(Output("individual_graph", "figure"), 
                [
                    Input("zone_types", "value"),
                    Input("vessel_types", "value"),
                    Input("cluster_slider", "value"),
                ],
             )
def make_individual_figure(zone_types, vessel_types, cluster_slider):
    layout_individual = copy.deepcopy(layout)
    df_full_trips = trips.get_trips()
    df_full_trips = df_full_trips[df_full_trips['VesselType'].isin(vessel_types)]
    figure = co2_scatter.get_co2_scatter(df_full_trips)
    return figure

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
