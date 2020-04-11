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
from util.helpers import *
from util import map_helpers

# Multi-dropdown options
from controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS

# Custom imports
from views import filter, header, metrics
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

# Create global chart template
mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Vessel Tracker",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
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
                 filter.get_filter()],
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
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("count_graph", "figure")],
)

# Radio -> multi
@app.callback(
    Output("well_statuses", "value"), [Input("well_status_selector", "value")]
)
def display_status(selector):
    if selector == "all":
        return list(WELL_STATUSES.keys())
    elif selector == "active":
        return ["AC"]
    return []


# Radio -> multi
@app.callback(Output("well_types", "value"), [Input("well_type_selector", "value")])
def display_type(selector):
    if selector == "all":
        return list(WELL_TYPES.keys())
    elif selector == "productive":
        return ["GD", "GE", "GW", "IG", "IW", "OD", "OE", "OW"]
    return []

# Slider -> count graph
@app.callback(Output("year_slider", "value"), [Input("count_graph", "selectedData")])
def update_year_slider(count_graph_selected):

    if count_graph_selected is None:
        return [1990, 2010]

    nums = [int(point["pointNumber"]) for point in count_graph_selected["points"]]
    return [min(nums) + 1960, max(nums) + 1961]

@app.callback(
    [
        Output("well_text", "children"),
        Output("gasText", "children"),
        Output("oilText", "children"),
        Output("waterText", "children"),
    ],
    [Input("aggregate_data", "data")],
)
def update_metrics(data):
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
    full_trips_df = trips.get_trips()
    metrics = agg_metrics(full_trips_df)
    return metrics['number_of_trips'], metrics['number_of_hubs'], metrics['actual_co2_emission'], metrics['optimized_co2_emission']


# Selectors -> main graph
@app.callback(
    Output("main_graph", "figure"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
    ],
    [State("main_graph", "relayoutData")],
)
def make_main_figure(
    well_statuses, well_types, year_slider, main_graph_layout
):
    full_trips_df = trips.get_trips()
    figure = map_view.gen_map(full_trips_df)
    return figure


# Main graph -> individual graph
@app.callback(Output("individual_graph", "figure"), 
              [])
def make_individual_figure():

    layout_individual = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {
            "points": [
                {"curveNumber": 4, "pointNumber": 569, "customdata": 31101173130000}
            ]
        }

    chosen = [point["customdata"] for point in main_graph_hover["points"]]
    index, gas, oil, water = produce_individual(chosen[0])

    if index is None:
        annotation = dict(
            text="No data available",
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_individual["annotations"] = [annotation]
        data = []
    else:
        data = [
            dict(
                type="scatter",
                mode="lines+markers",
                name="Gas Produced (mcf)",
                x=index,
                y=gas,
                line=dict(shape="spline", smoothing=2, width=1, color="#fac1b7"),
                marker=dict(symbol="diamond-open"),
            ),
            dict(
                type="scatter",
                mode="lines+markers",
                name="Oil Produced (bbl)",
                x=index,
                y=oil,
                line=dict(shape="spline", smoothing=2, width=1, color="#a9bb95"),
                marker=dict(symbol="diamond-open"),
            ),
            dict(
                type="scatter",
                mode="lines+markers",
                name="Water Produced (bbl)",
                x=index,
                y=water,
                line=dict(shape="spline", smoothing=2, width=1, color="#92d8d8"),
                marker=dict(symbol="diamond-open"),
            ),
        ]
        layout_individual["title"] = dataset[chosen[0]]["Well_Name"]

    figure = dict(data=data, layout=layout_individual)
    return figure

# Selectors -> count graph
@app.callback(
    Output("count_graph", "figure"),
    [
        #Input("well_statuses", "value"),
        #Input("well_types", "value"),
        #Input("year_slider", "value"),
    ],
)
def make_count_figure():#well_statuses, well_types, year_slider):
    layout_count = copy.deepcopy(layout)

    #dff = filter_dataframe(df, well_statuses, well_types, [1960, 2017])
    dff = df
    g = dff[["API_WellNo", "Date_Well_Completed"]]
    g.index = g["Date_Well_Completed"]
    g = g.resample("A").count()

    colors = []
    for i in range(1960, 2018):
        if i >= int(year_slider[0]) and i < int(year_slider[1]):
            colors.append("rgb(123, 199, 255)")
        else:
            colors.append("rgba(123, 199, 255, 0.2)")

    data = [
        dict(
            type="scatter",
            mode="markers",
            x=g.index,
            y=g["API_WellNo"] / 2,
            name="All Wells",
            opacity=0,
            hoverinfo="skip",
        ),
        dict(
            type="bar",
            x=g.index,
            y=g["API_WellNo"],
            name="All Wells",
            marker=dict(color=colors),
        ),
    ]

    layout_count["title"] = "Optimized CO2 vs Actual CO2"
    layout_count["dragmode"] = "select"
    layout_count["showlegend"] = False
    layout_count["autosize"] = True

    figure = dict(data=data, 
                  layout=layout_count)
    return figure

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
