"""
scoring.py

Builds an interpretable "Estimated Deutschlandticket Adoption Potential"
score (0-100), not a predicted probability.

I did not train a supervised model here. There is no observed
adoption outcome in this dataset no employee has actually been offered and either bought or
declined a Deutschlandticket in a way we could learn from.
"""

import numpy as np
import pandas as pd

from config import ADOPTION_WEIGHTS, ADOPTION_THRESHOLDS


def _normalise_inverse(series, cap=None):
    """Lower raw value -> higher score. Scales to 0-100."""
    s = series.copy().astype(float)
    if cap is not None:
        s = s.clip(upper=cap)
    lo, hi = s.min(), s.max()
    if hi == lo:
        return pd.Series(50.0, index=s.index)
    return 100 * (1 - (s - lo) / (hi - lo))


def compute_adoption_score(df):
    out = df.copy()

    # Component 1: commute time -- shorter estimated PT commute is more
    # attractive. Capped at 90 min so a handful of extreme outliers don't
    # compress the scale for everyone else.
    out["commute_time_score"] = _normalise_inverse(out["door_to_door_time_min"], cap=90)

    # Component 2: connectivity -- fewer transfers and a shorter walk to the
    # nearest station both make PT more attractive. I combine them into one
    # sub-score: distance to station (inverse) minus a flat penalty per
    # transfer.
    walk_component = _normalise_inverse(out["distance_to_station_km"], cap=3.0)
    transfer_penalty = out["n_transfers"] * 20  # flat 20-point deduction per transfer
    out["connectivity_score"] = (walk_component - transfer_penalty).clip(lower=0, upper=100)

    # Component 3: car access penalty -- someone with an easy car
    # alternative available has less incentive to switch to PT/DT, all else
    # equal. This is scored as: no car access = 100 (no competing
    # alternative), car access = 30 (still possible, but less likely).
    out["car_access_penalty"] = np.where(out["car_access"], 30.0, 100.0)

    # Component 4: current transport mode -- someone already using public
    # transport or a mixed mode is closer to adopting a Deutschlandticket
    # than someone who exclusively drives.
    mode_scores = {
        "public_transport": 100.0,
        "mixed": 80.0,
        "bike": 50.0,
        "car": 20.0,
    }
    out["current_mode_score"] = out["current_transport_mode"].map(mode_scores)

    out["adoption_potential_score"] = (
        out["commute_time_score"] * ADOPTION_WEIGHTS["commute_time_score"]
        + out["connectivity_score"] * ADOPTION_WEIGHTS["connectivity_score"]
        + out["car_access_penalty"] * ADOPTION_WEIGHTS["car_access_penalty"]
        + out["current_mode_score"] * ADOPTION_WEIGHTS["current_mode_score"]
    ).round(1)

    def _group(score):
        if score >= ADOPTION_THRESHOLDS["High potential"]:
            return "High potential"
        elif score >= ADOPTION_THRESHOLDS["Medium potential"]:
            return "Medium potential"
        else:
            return "Low potential"

    out["adoption_potential_group"] = out["adoption_potential_score"].apply(_group)
    return out
