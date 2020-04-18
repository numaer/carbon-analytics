"""
trips.py

Trips ORM model.

TODO:
    - Data should ideally be queried from Postgres here as needed. 
    - For computationally expensive parameters, the results should be cached
"""

# Import required libraries
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
from util.helpers import *
from util import map_helpers

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

class Trips():
    def __init__(self, data_path):
        self.data_path = data_path
        self.df_clusters = []
        for c in CLUSTERS:
            c = np.format_float_positional(c)
            df = pd.read_csv(self.data_path.joinpath(f"clusteredDF_{(c)}.csv"), low_memory=False)
            df['cluster_size'] = (c)
            df['co2_total'] = df[['CO2_SpokeStart', 'CO2_SpokeEnd', 'CO2_Hub_Hub']].sum(axis=1)
            self.df_clusters.append(df)
        self.df_clusters = pd.concat(self.df_clusters)

    def get_trips(self, cluster_size=1, hub_efficiency=None, zone_types="All", vessel_types=None):
        cluster_size = np.format_float_positional(cluster_size)
        df = self.df_clusters[self.df_clusters['cluster_size'] == cluster_size]
        if zone_types != "All":
            df = df[(df['StartHUBPORT_PortID'] == zone_types) | (df['ENDHUBPORT_PortID'] == zone_types)]
        if vessel_types:
            df = df[df['VesselType'].isin(vessel_types)]

        return df
