# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

from controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS

# Create controls
AVAILABLE_ZONES = ["Zone 20"]
CLUSTERS = [
    0.1,
    0.01,
    0.001,
    0.0001,
    0.00001,
    0.2,
    0.02,
    0.3,
    0.03,
    0.4,
    0.04,
    0.5,
    0.05,
    0.005,
    0.6,
    0.06,
    0.7,
    0.07,
    0.8,
    0.08,
    0.9,
    0.09,
    0.15,
    0.25,
    0.35,
    0.45,
    0.95,
    0,
    1.25,
    1
]

CLUSTERS.sort()

def gen_options(vals, b=False):
    """
    generate options via not the black-scholes equation
    """
    if b:
        return [{"label": v, "value": v} for v in vals]
    return [{"label": v, "value": v} for v in vals]
     

def get_filter(trips):
    df = trips.get_trips()    
    max_eff = df['Hub_TEU'].max()
    min_eff = df['Hub_TEU'].min()

    # Gen vessel options
    vessel_types = list(df['VesselType'].unique())
    vessel_options = gen_options(vessel_types)

    # Gen zones options
    zone_types = AVAILABLE_ZONES
    zone_types = list(set(df['StartHUBPORT_PortID'].unique()).union(set(df['ENDHUBPORT_PortID'].unique())))
    zone_options = gen_options(zone_types)

    return html.Div(
        [
        html.P(
            "Filter by cluster size (epsilon):",
            className="control_label",
            ),
        dcc.Slider(
            id="cluster_slider",
            min=0,
            max=1.25,
            value=1,
            step=None,
            className="dcc_control",
            #marks=CLUSTERS
            marks={k:"" for k in CLUSTERS},
            tooltip = { 'always_visible': True }
            ),
        html.P(
            "Percentage of trips to display:",
            className="control_label",
            ),
        dcc.Slider(
            id="hub_efficiency",
            min=0,
            max=1,
            value=0.10,
            step=0.05,
            className="dcc_control",
            marks={0:"0%", .25:"25%", 0.50:"50%", 0.75:"75%", 1:"100%"}
            ),
        html.P("Hubs to display:", className="control_label"),
        dcc.Dropdown(
                id="zone_types",
                options=zone_options,
                multi=True,
                value=zone_types[:5],
                className="dcc_control",
                ),
        html.P("Filter by vessel type:", className="control_label"),
        dcc.Dropdown(
                id="vessel_types",
                options=vessel_options,
                multi=True,
                value=vessel_types,
                className="dcc_control",
                ),
        ],
        className="pretty_container four columns",
        id="cross-filter-options",
        )
