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

def get_header():
    return html.Div(
            [
                html.Div(
                    [
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "CO2 Emissions in Freight Traffic",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "42. Team NYC", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Learn More: DVA", id="learn-more-button"),
                            href="https://docs.google.com/document/d/e/2PACX-1vR5-8SC5dE30GdEohe69d-CA0QA45dPtBI43VYImQsqLKW7PjIVHPCGtA9fFlu98hAw6YWVF9Pyb-4n/pub#h.9rebwbttjkfm",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        )

