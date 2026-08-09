"""
geospatial.py

Small set of geospatial helper functions. 
haversine distance for straight-line distance, plus a nearest-station lookup.
environment -- see docs/limitations.md. Straight-line distance is scaled by
a documented "network distance factor" in transport.py instead.
"""

import numpy as np
import pandas as pd


def haversine_km(lat1, lon1, lat2, lon2):
    """
    Great-circle distance between two points in kilometres.
    Vectorised so it works on scalars or numpy arrays/pandas Series.
    """
    R = 6371.0088  # mean Earth radius, km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c


def nearest_station(lat, lon, stations_df):
    """
    Given a single (lat, lon) and a DataFrame of stations with lat/lon/name/line
    columns, return the nearest station's name, line, and distance in km.

    I loop over the (small) station list per employee rather than building a
    spatial index (e.g. BallTree) because we only have ~10 reference stations.
    For a larger station set this would not scale and a KD-tree/BallTree
    would be the right choice.
    """
    dists = haversine_km(lat, lon, stations_df["lat"].values, stations_df["lon"].values)
    idx = np.argmin(dists)
    row = stations_df.iloc[idx]
    return row["name"], row["line"], float(dists[idx])


def attach_nearest_station(df, stations_df, lat_col="home_lat", lon_col="home_lon"):
    """
    Vectorised-ish version of nearest_station applied to a whole employee
    DataFrame. Returns three new columns: nearest_station, station_line,
    distance_to_station_km.
    """
    names, lines, dists = [], [], []
    for lat, lon in zip(df[lat_col], df[lon_col]):
        n, l, d = nearest_station(lat, lon, stations_df)
        names.append(n)
        lines.append(l)
        dists.append(d)
    out = df.copy()
    out["nearest_station"] = names
    out["station_line"] = lines
    out["distance_to_station_km"] = dists
    return out
