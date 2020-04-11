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
