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

def gen_options(vals):
    """
    generate options via not the black-scholes equation
    """
    return [{"label": v, "value": v} for v in vals]

def get_filter(trips):
    df = trips.get_trips()    

    # Gen vessel options
    vessel_types = list(df['VesselType'].unique())
    vessel_options = gen_options(vessel_types)

    # Gen zones options
    zone_types = AVAILABLE_ZONES
    zone_options = gen_options(zone_types)

    return html.Div(
        [
        html.P(
            "Filter by cluster size",
            className="control_label",
            ),
        dcc.Slider(
            id="cluster_slider",
            min=1,
            max=30,
            value=5,
            step=None,
            className="dcc_control",
            marks={1: "1", 5:"5", 30:"30"}
            ),
        html.P("Filter by AIS zones:", className="control_label"),
        dcc.Dropdown(
                id="zone_types",
                options=zone_options,
                multi=True,
                value=zone_types,
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
