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
county_options = [
    {"label": str(COUNTIES[county]), "value": str(county)} for county in COUNTIES
]

well_status_options = [
    {"label": str(WELL_STATUSES[well_status]), "value": str(well_status)}
    for well_status in WELL_STATUSES
]

well_type_options = [
    {"label": str(WELL_TYPES[well_type]), "value": str(well_type)}
    for well_type in WELL_TYPES
]

def get_metrics():
    return html.Div(
            [
            html.Div(
                [
                html.Div(
                    [html.H6(id="well_text"), html.P("Total Trips")],
                    id="wells",
                    className="mini_container",
                    ),
                html.Div(
                    [html.H6(id="gasText"), html.P("Total Hubs")],
                    id="gas",
                    className="mini_container",
                    ),
                html.Div(
                    [html.H6(id="oilText"), html.P("CO2 Emitted")],
                    id="oil",
                    className="mini_container",
                    ),
                html.Div(
                    [html.H6(id="waterText"), html.P("CO2 Optimized Emissions")],
                    id="water",
                    className="mini_container",
                    ),
                ],
                id="info-container",
                className="row container-display",
                ),
                html.Div(
                        [dcc.Graph(id="count_graph")],
                        id="countGraphContainer",
                        className="pretty_container",
                        ),
                ],
                id="right-column",
                className="eight columns",
                )

def get_filter():
    return html.Div(
            [
            html.Div(
                [
                html.P(
                    "Filter by cluster size",
                    className="control_label",
                    ),
                dcc.RangeSlider(
                    id="year_slider",
                    min=1,
                    max=30,
                    value=[5],
                    step=5,
                    className="dcc_control",
                    marks={1: "1", 5:"5", 30:"30"}
                    ),
                html.P("Filter by well status:", className="control_label"),
                dcc.RadioItems(
                    id="well_status_selector",
                    options=[
                    {"label": "All ", "value": "all"},
                    {"label": "Active only ", "value": "active"},
                    {"label": "Customize ", "value": "custom"},
                    ],
                    value="active",
                    labelStyle={"display": "inline-block"},
                    className="dcc_control",
                    ),
                dcc.Dropdown(
                        id="well_statuses",
                        options=well_status_options,
                        multi=True,
                        value=list(WELL_STATUSES.keys()),
                        className="dcc_control",
                        ),
                dcc.Checklist(
                        id="lock_selector",
                        options=[{"label": "Lock camera", "value": "locked"}],
                        className="dcc_control",
                        value=[],
                        ),
                html.P("Filter by well type:", className="control_label"),
                dcc.RadioItems(
                        id="well_type_selector",
                        options=[
                        {"label": "All ", "value": "all"},
                        {"label": "Productive only ", "value": "productive"},
                        {"label": "Customize ", "value": "custom"},
                        ],
                        value="productive",
                        labelStyle={"display": "inline-block"},
                        className="dcc_control",
                        ),
                dcc.Dropdown(
                        id="well_types",
                        options=well_type_options,
                        multi=True,
                        value=list(WELL_TYPES.keys()),
                        className="dcc_control",
                        ),
                ],
                className="pretty_container four columns",
                id="cross-filter-options",
                ), get_metrics()
                            ],
                            className="row flex-display",
                            )

