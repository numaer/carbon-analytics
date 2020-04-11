"""
map_helpers.py

Contains helper functions to process post-processed trips dataframe.
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

# Multi-dropdown options
from controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS


import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from time import process_time
from sklearn.cluster import DBSCAN
import plotly.graph_objects as go
import plotly.express as px

"""
HELPERS
"""

def get_lat_lon_range(df):
    """Return the range of lat and lon in the data."""
    return [df['lat'].min(), df['lat'].max()], [df['lon'].min(), df['lon'].max()]

def get_scope(lat_range, lon_range):
    """Assign the proper scope based on range of data's lat/lon."""
    us_lat_rng = [24, 55]
    us_lon_rng = [-127, -50]
    na_lat_rng = [15, 85]
    na_lon_rng = [-170, -50]
    eu_lat_rng = [30, 80]
    eu_lon_rng = [-20, 70]
    sa_lat_rng = [-60, 12]
    sa_lon_rng = [-81, -34]

    if (lat_range[0] >= us_lat_rng[0] and lat_range[1] <= us_lat_rng[1]
            and lon_range[0] >= us_lon_rng[0] and lon_range[1] <= us_lon_rng[1]):
        scope = 'usa'
    elif (lat_range[0] >= na_lat_rng[0] and lat_range[1] <= na_lat_rng[1]
            and lon_range[0] >= na_lon_rng[0] and lon_range[1] <= na_lon_rng[1]):
        scope = 'north america'
    elif (lat_range[0] >= eu_lat_rng[0] and lat_range[1] <= eu_lat_rng[1]
          and lon_range[0] >= eu_lon_rng[0] and lon_range[1] <= eu_lon_rng[1]):
        scope = 'europe'
    elif (lat_range[0] >= sa_lat_rng[0] and lat_range[1] <= sa_lat_rng[1]
          and lon_range[0] >= sa_lon_rng[0] and lon_range[1] <= sa_lon_rng[1]):
        scope = 'south america'
    else:  # can add asia and africa
        scope = 'world'  # default
    return scope


"""
Generates the data needed to funnel trip data into a plotly geoscatter map
"""

def gen_df_spokes_start(df_full_trips):
    df = df_full_trips[['MMSI',
                                 'BaseDateTime_Start',
                                 'LAT_SPOKEStartPort', 
                                 'LON_SPOKEStartPort']].copy()
    df['color'] = 'green'
    df.columns = ['mmsi', 'time', 'lat', 'lon', 'color']
    df['size'] = 8
    df['text'] = (df['mmsi'].apply(lambda x: "MMSI: %s" % x))
    df['name'] = 'Spoke Start'
    df.head()
    return df

def gen_df_hub_start(df_full_trips):
    df = df_full_trips[['MMSI', 
                            'StartHUBPORT_PortID', 
                            'StartHUBPORT_LON',
                             'StartHUBPORT_LAT']].copy()

    df['count'] = df['StartHUBPORT_PortID']
    df = df.groupby(['StartHUBPORT_PortID', 
                        'StartHUBPORT_LON',
                       'StartHUBPORT_LAT'], as_index=False).agg({'count': 'count'})
    df.sort_values(by='count', ascending=False)
    df.columns = ['port_id', 'lon', 'lat', 'count']
    df['color'] = 'orange'
    df['text'] = df['port_id'].apply(lambda x: """Port ID: %s""" % x)
    df['name'] = 'Hub Start'
    df['size'] = 8 + df['count']
    df.head()
    return df

def gen_df_hub_end(df_full_trips):
    df = df_full_trips[['MMSI', 
                                  'ENDHUBPORT_PortID', 
                                  'ENDHUBPORT_LON',
                                  'ENDHUBPORT_LAT']].copy()


    df['count'] = df['ENDHUBPORT_PortID']
    df = df.groupby(['ENDHUBPORT_PortID', 
                        'ENDHUBPORT_LON',
                       'ENDHUBPORT_LAT'], as_index=False).agg({'count': 'count'})
    df.sort_values(by='count', ascending=False)
    df['color'] = 'blue'
    df.columns = ['port_id', 'lon', 'lat', 'count', 'color']
    df['text'] = df['port_id'].apply(lambda x: """Port ID: %s""" % x)
    df['name'] = 'Hub End'
    df['size'] = 8 + df['count']
    df.head()
    return df

def gen_df_spoke_end(df_full_trips):
    df = df_full_trips[['MMSI', 
                                  'LAT_SPOKEEndPort',
                                  'LON_SPOKEEndPort',
                                 'BaseDateTime_TripEnd']].copy()
    df.columns = ['mmsi', 'lat', 'lon', 'time']
    df['color'] = 'red'
    df['size'] = 8
    df['text'] = (df['mmsi'].apply(lambda x: "MMSI: %s" % x))
    df['name'] = 'Spoke End'
    df.head()
    return df


