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
    df = df_full_trips[['Length', 'Width', 'VesselType']]
    df['CO2 Emitted'] = df['Length'].copy().apply(lambda x: x*np.random.random(1)[0])
    df.head()
    return df

def get_co2_scatter(df_full_trips):
    fig = px.scatter_3d(_generate_scatter_df(df_full_trips), 
                        x='Length', 
                        y='Width', 
                        z='CO2 Emitted',
                        color='VesselType')
                        
    return fig
