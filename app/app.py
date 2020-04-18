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
    autosize=False,
    automargin=False,
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
                    [dcc.Graph(id="teu_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="original_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="individual_graph", config={'displayModeBar': False})],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        
        ),
       # dcc scatter mapbox
       html.Div(
            [
                html.Div(
                    [dcc.Graph(id="mapbox_graph")],
                    className="pretty_container twelve columns",
                )
            ],
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
    [
        Input("zone_types", "value"),
        Input("vessel_types", "value"),
        Input("cluster_slider", "value"),
        Input("hub_efficiency", "value"),
    ],
)
def update_metrics(zone_types, vessel_types, cluster_slider, hub_efficiency):
    def agg_metrics(df_full_trips):
        df = df_full_trips 
        data = {
            'number_of_trips': len(df_full_trips),
            'number_of_hubs': len(set(df_full_trips['StartHUBPORT_PortID'].unique()).union(
                                set(df_full_trips['ENDHUBPORT_PortID'].unique()))),
            'actual_co2_emission': df_full_trips['Individual_TEU'].sum(),
            'optimized_co2_emission': df_full_trips['Hub_TEU'].sum()
        }

        return data
    df_full_trips = trips.get_trips(cluster_size=cluster_slider,
                                    hub_efficiency=None,
                                    zone_types=None,
                                    vessel_types=vessel_types)
    metrics = agg_metrics(df_full_trips)
    metrics['actual_co2_emission'] /= 1000000
    metrics['actual_co2_emission'] = metrics['actual_co2_emission'].round(1)
    metrics['actual_co2_emission'] = f"{metrics['actual_co2_emission']} M TEU"
    metrics['optimized_co2_emission'] /= 1000000
    metrics['optimized_co2_emission'] = metrics['optimized_co2_emission'].round(1)
    metrics['optimized_co2_emission'] = f"{metrics['optimized_co2_emission']} M TEU"
    return metrics['number_of_trips'], metrics['number_of_hubs'], metrics['actual_co2_emission'], metrics['optimized_co2_emission']


# Selectors -> main graph
@app.callback(
    Output("main_graph", "figure"),
    [
        Input("zone_types", "value"),
        Input("vessel_types", "value"),
        Input("cluster_slider", "value"),
        Input("hub_efficiency", "value"),
    ],
    [State("main_graph", "relayoutData")],
)
def make_main_figure(
    zone_types, vessel_types, cluster_slider, hub_efficiency, main_graph_layout
):
    df_full_trips = trips.get_trips(cluster_size=cluster_slider,
                                    hub_efficiency=hub_efficiency,
                                    zone_types=zone_types,
                                    vessel_types=vessel_types)
    figure = map_view.gen_map(df_full_trips)
    return figure

"""
## Mapbox graph plotting start port by port ID assigned
"""
@app.callback(
    Output("mapbox_graph", "figure"),
    [
        Input("zone_types", "value"),
        Input("vessel_types", "value"),
        Input("cluster_slider", "value"),
        Input("hub_efficiency", "value"),
    ],
    [State("mapbox_graph", "relayoutData")],
)
def make_mapbox_figure(
    zone_types, vessel_types, cluster_slider, hub_efficiency, main_graph_layout
):
    df_full_trips = trips.get_trips(cluster_size=0.001,
                                    hub_efficiency=None,
                                    zone_types=zone_types,
                                    vessel_types=vessel_types)                       
    figure = {
            'data': [{
                'lat': df_full_trips['LAT_SPOKEStartPort'],
                'lon': df_full_trips['LON_SPOKEStartPort'],
                'marker':{
                    'color': df_full_trips['StartHUBPORT_PortID'],
                    'size': 10,
                    'opacity': 1,
                    'colorscale':'Jet'
                },
                'customdata': df_full_trips['StartHUBPORT_PortID'],
                'type':'scattermapbox' ## Different types of mapbox is available
            }],
            'layout':{
                'mapbox':{
                    'accesstoken':'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3MDBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw',
                    'center': dict(lon= -75.629536, lat= 24.619554)
                }, ##Access token is taken from https://github.com/plotly/dash-recipes/blob/master/walmart-hover.py
                'hovermode': 'closest',
                'margin':{'l':30, 'r':30, 'b':30, 't':30},
            },
        }
    map_view.gen_map(df_full_trips, lines=False)
    return figure

"""
"""
@app.callback(
    Output("original_graph", "figure"),
    [
        Input("zone_types", "value"),
        Input("vessel_types", "value"),
        Input("cluster_slider", "value"),
        Input("hub_efficiency", "value"),
    ],
    [State("original_graph", "relayoutData")],
)
def make_original_figure(
    zone_types, vessel_types, cluster_slider, hub_efficiency, main_graph_layout
):
    df_full_trips = trips.get_trips(cluster_size=cluster_slider,
                                    hub_efficiency=0.01,
                                    zone_types=zone_types,
                                    vessel_types=vessel_types)
    print(len(df_full_trips))
    figure = map_view.gen_map(df_full_trips, lines=False)
    return figure

# Main graph -> individual graph
@app.callback(Output("individual_graph", "figure"), 
                [
                    Input("zone_types", "value"),
                    Input("vessel_types", "value"),
                    Input("cluster_slider", "value"),
                    Input("hub_efficiency", "value"),
                ]
             )
def make_scatter_figure(zone_types, vessel_types, cluster_slider, hub_efficiency):
    layout_individual = copy.deepcopy(layout)
    df_full_trips = trips.get_trips(cluster_size=cluster_slider,
                                    vessel_types=vessel_types)
    figure = co2_scatter.get_co2_scatter(df_full_trips)
    return figure

# Main graph -> individual graph
@app.callback(Output('teu_graph', 'figure'),
              [Input('main_graph', 'hoverData')])
def make_teu_figure(main_graph_hover):

    layout_individual = copy.deepcopy(layout)
    df = trips.df_clusters

    if main_graph_hover:
        points_data = main_graph_hover['points'][0]
        df = df[(df['LON_SPOKEStartPort'] == points_data['lon']) |
                (df['StartHUBPORT_LON'] == points_data['lon']) |
                (df['LON_SPOKEEndPort'] == points_data['lon']) |
                (df['ENDHUBPORT_LON'] == points_data['lon'])]
        df = df.drop_duplicates(subset=['cluster_size'])
        df = df.sort_values(by=['cluster_size'], ascending=True)

        data = [
            dict(
                type='scatter',
                mode='lines+markers',
                name='Epsilon vs TEU',
                x=df['cluster_size'],
                y=df['Hub_TEU'],
                xaxis_title="Cluster Size (Epsilon)",
                yaxis_title="CO2 Efficiency (TEU)",
                line=dict(
                    shape="spline",
                    smoothing=2,
                    width=1,
                    color='#92d8d8'
                ),
                marker=dict(symbol='diamond-open')
            )
        ]
    else:
        data = []
    layout_individual["title"] = "Cluster Size vs TEU"
    layout_individual["xaxis_title"] = "Cluster Size (Epsilon)"
    layout_individual["yaxis_title"] = "CO2 Efficiency (TEU)"
    figure = dict(data=data, layout=layout_individual)
    return figure

# Main
if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_props_check=False)
