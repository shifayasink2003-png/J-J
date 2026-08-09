"""
config.py

Central place for every assumption and reference value used in the analysis.
I put everything here instead of scattering magic numbers through the notebook
so that every number in the analysis can be traced back to a single,
documented source.

Sources for station data: the coordinates below are real, publicly known
locations of HVV (Hamburger Verkehrsverbund) stations near Norderstedt and
along the Hamburg U-Bahn/AKN network. I was not able to pull the live HVV
GTFS feed into this environment (see docs/limitations.md).
"""

import numpy as np

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
RANDOM_SEED = 42

# ---------------------------------------------------------------------------
# Workplace
# ---------------------------------------------------------------------------
WORKPLACE_NAME = "Johnson & Johnson Medical GmbH"
WORKPLACE_ADDRESS = "Robert-Koch-Straße 1, 22851 Norderstedt, Germany"
# Approximate coordinates for the Robert-Koch-Straße industrial/office area
# in Norderstedt (Nordheide/Harksheide district), near Norderstedt Mitte.
WORKPLACE_LAT = 53.6947
WORKPLACE_LON = 9.9959

# ---------------------------------------------------------------------------
# Reference HVV / AKN stations near Norderstedt and along commute corridors
# into Hamburg. These are real stations (U-Bahn U1 line and AKN A1 line
# serve Norderstedt); coordinates are approximate station-area locations,
# not exact platform coordinates.
# ---------------------------------------------------------------------------
STATIONS = [
    # U1 line (Norderstedt <-> central Hamburg corridor)
    {"name": "Norderstedt Mitte", "lat": 53.6906, "lon": 9.9885, "line": "U1"},
    {"name": "Garstedt",          "lat": 53.6742, "lon": 9.9932, "line": "U1"},
    {"name": "Ochsenzoll",        "lat": 53.6580, "lon": 10.0068, "line": "U1"},
    {"name": "Kiwittsmoor",       "lat": 53.6465, "lon": 10.0182, "line": "U1"},
    {"name": "Langenhorn Nord",   "lat": 53.6395, "lon": 10.0090, "line": "U1"},
    {"name": "Fuhlsbüttel Nord",  "lat": 53.6274, "lon": 10.0012, "line": "U1"},
    {"name": "Alsterdorf",        "lat": 53.6018, "lon": 9.9987, "line": "U1"},
    {"name": "Ohlsdorf",          "lat": 53.6205, "lon": 10.0202, "line": "U1"},
    # AKN A1 line (Norderstedt <-> Kaltenkirchen/Quickborn corridor)
    {"name": "Norderstedt-Mitte AKN", "lat": 53.6906, "lon": 9.9885, "line": "AKN-A1"},
    {"name": "Friedrichsgabe",    "lat": 53.6975, "lon": 9.9700, "line": "AKN-A1"},
    {"name": "Tanneneck",         "lat": 53.7050, "lon": 9.9550, "line": "AKN-A1"},
    {"name": "Quickborn",         "lat": 53.7326, "lon": 9.9061, "line": "AKN-A1"},
    {"name": "Hasloh",            "lat": 53.7130, "lon": 9.9270, "line": "AKN-A1"},
    {"name": "Henstedt-Ulzburg",  "lat": 53.7967, "lon": 9.9764, "line": "AKN-A1"},
    {"name": "Kaltenkirchen",     "lat": 53.8367, "lon": 9.9628, "line": "AKN-A1"},
    # Central Hamburg reference point (city-centre residents use the wider
    # U/S-Bahn network, simplified here to a single representative hub)
    {"name": "Hamburg Hauptbahnhof", "lat": 53.5528, "lon": 10.0069, "line": "U1"},
]

# ---------------------------------------------------------------------------
# Residential areas used as the basis for synthetic-population sampling.
# These are real districts/towns around Hamburg and Norderstedt. Rather than
# sample uniformly in a bounding box, I anchor sampling around these named
# areas and give each a rough population weight reflecting its relative size
# (approximate, ordinal weighting based on general population size -- see
# docs/assumptions.md for the reasoning).
# ---------------------------------------------------------------------------
RESIDENTIAL_AREAS = [
    {"name": "Norderstedt",        "lat": 53.6889, "lon": 9.9822, "weight": 0.22},
    {"name": "Langenhorn (Hamburg)","lat": 53.6494, "lon": 10.0106, "weight": 0.16},
    {"name": "Fuhlsbüttel",        "lat": 53.6314, "lon": 9.9958, "weight": 0.10},
    {"name": "Ohlsdorf",           "lat": 53.6217, "lon": 10.0225, "weight": 0.08},
    {"name": "Alsterdorf",         "lat": 53.6032, "lon": 9.9984, "weight": 0.07},
    {"name": "Quickborn",          "lat": 53.7326, "lon": 9.9061, "weight": 0.09},
    {"name": "Kaltenkirchen",      "lat": 53.8319, "lon": 9.9622, "weight": 0.08},
    {"name": "Hamburg-Innenstadt", "lat": 53.5511, "lon": 9.9937, "weight": 0.10},
    {"name": "Henstedt-Ulzburg",   "lat": 53.7833, "lon": 9.9667, "weight": 0.10},
]
_w = np.array([a["weight"] for a in RESIDENTIAL_AREAS], dtype=float)
for a, w in zip(RESIDENTIAL_AREAS, _w / _w.sum()):
    a["weight"] = float(w)

# ---------------------------------------------------------------------------
# Synthetic population size
# ---------------------------------------------------------------------------
N_EMPLOYEES = 500

# ---------------------------------------------------------------------------
# Commute-time assumptions (documented, not hidden)
# Sources: these are standard planning-level assumptions used in transport
# accessibility studies when live routing isn't available -- not measured
# values. See docs/assumptions.md.
# ---------------------------------------------------------------------------
WALKING_SPEED_KMH = 4.5          # average adult walking speed
AVG_WAIT_TIME_MIN = 6.0          # average wait for next scheduled service
TRANSFER_PENALTY_MIN = 5.0       # time cost per transfer (walk + wait)
TRANSIT_SPEED_KMH = {
    "U1": 32.0,        # U-Bahn average scheduled speed incl. stops
    "AKN-A1": 45.0,    # AKN regional line, faster/less frequent
}
DEFAULT_TRANSIT_SPEED_KMH = 30.0

# route "directness" factor: network distance is longer than straight-line
# distance because transit follows fixed corridors, not straight lines.
NETWORK_DISTANCE_FACTOR = 1.3

# ---------------------------------------------------------------------------
# Commute-time groups
# ---------------------------------------------------------------------------
COMMUTE_BINS = [0, 30, 45, 60, np.inf]
COMMUTE_LABELS = ["<=30 min", "31-45 min", "46-60 min", ">60 min"]

# ---------------------------------------------------------------------------
# Deutschlandticket adoption-potential score weights
# Score is built on a 0-100 scale from four interpretable components,
# each already normalised to 0-100 before weighting. See docs/assumptions.md
# for why these specific weights were chosen.
# ---------------------------------------------------------------------------
ADOPTION_WEIGHTS = {
    "commute_time_score": 0.35,     # shorter PT commute -> more attractive
    "connectivity_score": 0.30,     # fewer transfers, closer station -> more attractive
    "car_access_penalty": 0.20,     # already has an easy car alternative -> less likely to switch
    "current_mode_score": 0.15,     # already using PT/mixed mode -> more likely to formalise with DT
}

ADOPTION_THRESHOLDS = {
    "High potential":   70,
    "Medium potential": 45,
    "Low potential":    0,
}
