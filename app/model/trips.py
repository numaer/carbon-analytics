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
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
from util.helpers import *
from util import map_helpers

class Trips():
    def __init__(self, data_path):
        self.data_path = data_path

    def get_trips(self):
        df = pd.read_csv(self.data_path.joinpath("fullTrips.csv"), low_memory=False)
        return df
