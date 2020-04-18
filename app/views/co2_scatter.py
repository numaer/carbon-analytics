"""
co2_scatter.py

Plotly figure for scatter plot for individual trip emissions

TODO:
- Get actual CO2 numbers

"""

import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import plotly.graph_objects as go

def _generate_scatter_df(df_full_trips):
    df = df_full_trips[['Length', 'Width', 'ENDHUBPORT_PortID']]
    df['Hub'] = df['ENDHUBPORT_PortID']
    df['CO2 Efficiency'] = df_full_trips['Individual_TEU']
    df.head()
    return df

def get_co2_scatter(df_full_trips):
    fig = px.scatter_3d(_generate_scatter_df(df_full_trips), 
                        title=dict(
                            text="Vessel Dimensions vs CO2 Efficiency",
                        ),
                        x='Length', 
                        y='Width', 
                        z='CO2 Efficiency',
                        color='Hub')
                        
    return fig
