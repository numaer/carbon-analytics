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

def get_metrics():
    return html.Div(
            [
            html.Div(
                [
                html.H3(
                    "CO2 Emissions Optimization in Freight Traffic",
                    style={"margin-bottom": "0px"},
                    ),
                html.H5(
                    "42. Team NYC", style={"margin-top": "0px"}
                    ),
                html.P("This dashboard demonstrates how we can reduce CO2 emissions from maritime freight traffic by leveraging a hub-and-spoke model to aggregate vessel cargo. Toggle the controls on the right and interact with the charts to understand the various scenarios of optimizing freight traffic to reduce emissions.")
                ],
                className="pretty_container"
                ),
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
                    [html.H6(id="oilText"), html.P("CO2 Original Efficiency")],
                    id="oil",
                    className="mini_container",
                    ),
                html.Div(
                    [html.H6(id="waterText"), html.P("CO2 Optimized Efficiency")],
                    id="water",
                    className="mini_container",
                    ),
                ],
                id="info-container",
                className="row container-display",
                ),
                ],
                id="right-column",
                className="eight columns",
                )

"""
If we get the optimized co2 data, put this back in!

html.Div(
[dcc.Graph(id="count_graph")],
id="countGraphContainer",
className="pretty_container",
),
"""
