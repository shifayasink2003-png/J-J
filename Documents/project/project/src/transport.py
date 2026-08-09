"""
transport.py

Estimates public transport connectivity and door-to-door commute time.

These are ESTIMATED commute times built from a transparent formula, not
observed or routed times.

Door-to-door time = walk to station + wait + transit ride (with a transfer
penalty when the nearest station doesn't sit on a line that plausibly runs
close to the workplace) + walk from arrival point to workplace.
"""

import numpy as np
import pandas as pd

from config import (
    WALKING_SPEED_KMH, AVG_WAIT_TIME_MIN, TRANSFER_PENALTY_MIN,
    TRANSIT_SPEED_KMH, DEFAULT_TRANSIT_SPEED_KMH, NETWORK_DISTANCE_FACTOR,
    WORKPLACE_LAT, WORKPLACE_LON,
)
from geospatial import haversine_km


def walking_time_minutes(distance_km, speed_kmh=WALKING_SPEED_KMH):
    return (distance_km / speed_kmh) * 60.0


def estimate_transit_leg(distance_km, line):
    """
    Estimate in-vehicle time for a given straight-line distance and transit
    line, applying the network-distance factor (transit doesn't travel in a
    straight line) and the line's average scheduled speed.
    """
    speed = TRANSIT_SPEED_KMH.get(line, DEFAULT_TRANSIT_SPEED_KMH)
    network_km = distance_km * NETWORK_DISTANCE_FACTOR
    return (network_km / speed) * 60.0


def requires_transfer(line):
    """
    Simplification: the U1 line runs close to Norderstedt/Langenhorn and
    within reasonable reach of the workplace corridor; the AKN-A1 line
    terminates further out and, in practice, usually requires an interchange
    onto U1 or a bus to reach the Robert-Koch-Straße area. I encode that as
    a fixed rule rather than a probability, and flag it as a simplification.
    """
    return line == "AKN-A1"


def compute_door_to_door(df):
    """
    Adds the following columns to df (which must already have
    nearest_station, station_line, distance_to_station_km from
    geospatial.attach_nearest_station):

    walking_time_min, waiting_time_min, transit_time_min, transfer_time_min,
    final_walk_time_min, door_to_door_time_min, n_transfers
    """
    out = df.copy()

    out["walking_time_min"] = walking_time_minutes(out["distance_to_station_km"])
    out["waiting_time_min"] = AVG_WAIT_TIME_MIN

    transit_km = haversine_km(
        out["home_lat"].values, out["home_lon"].values,
        # transit "as the crow flies" is measured station-to-workplace,
        # since we don't have a routed network -- this is the distance the
        # in-vehicle leg has to cover
        WORKPLACE_LAT, WORKPLACE_LON,
    )
    out["transit_time_min"] = [
        estimate_transit_leg(d, line) for d, line in zip(transit_km, out["station_line"])
    ]

    out["n_transfers"] = out["station_line"].apply(lambda l: 1 if requires_transfer(l) else 0)
    out["transfer_time_min"] = out["n_transfers"] * TRANSFER_PENALTY_MIN

    # final walk from arrival station/stop to the workplace door. Robert-
    # Koch-Straße is roughly a 10-15 min walk or short bus hop from
    # Norderstedt Mitte; I use a fixed planning-level assumption here
    # rather than a per-employee calculation since every employee arrives
    # at (effectively) the same workplace-side stop.
    out["final_walk_time_min"] = 12.0

    out["door_to_door_time_min"] = (
        out["walking_time_min"] + out["waiting_time_min"] + out["transit_time_min"]
        + out["transfer_time_min"] + out["final_walk_time_min"]
    )
    return out
