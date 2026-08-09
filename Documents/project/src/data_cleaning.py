"""
data_cleaning.py

Data-quality and sanity checks run on both the raw synthetic population and
the enriched (post-commute-time, post-scoring) dataset. I kept these as
plain functions that return a small report dict rather than silently
"fixing" anything any issue found is printed/logged in the notebook so
the fix is visible.
"""

import numpy as np
import pandas as pd


def check_missing_and_duplicates(df, id_col="employee_id"):
    report = {}
    report["missing_values"] = df.isna().sum().to_dict()
    report["duplicate_ids"] = int(df[id_col].duplicated().sum())
    report["duplicate_rows"] = int(df.duplicated().sum())
    return report


def check_coordinate_validity(df, lat_col="home_lat", lon_col="home_lon"):
    """
    Hamburg/Schleswig-Holstein region: sanity-check coordinates fall in a
    plausible bounding box (roughly 53.3-54.0 lat, 9.5-10.3 lon). This is a
    generous box around the real study area, not a tight one it's meant
    to catch generation bugs (e.g. swapped lat/lon), not to be a precise
    boundary.
    """
    lat_ok = df[lat_col].between(53.3, 54.0)
    lon_ok = df[lon_col].between(9.3, 10.5)
    invalid = df[~(lat_ok & lon_ok)]
    return {
        "n_invalid_coordinates": int(len(invalid)),
        "invalid_employee_ids": invalid["employee_id"].tolist() if len(invalid) else [],
    }


def check_commute_time_sanity(df, time_col="door_to_door_time_min"):
    negative = df[df[time_col] < 0]
    impossible_low = df[df[time_col] < 5]     # nobody should have a <5 min door-to-door PT commute here
    impossible_high = df[df[time_col] > 150]  # >2.5h one-way would be an extreme outlier worth flagging
    return {
        "n_negative": int(len(negative)),
        "n_implausibly_low_(<5min)": int(len(impossible_low)),
        "n_implausibly_high_(>150min)": int(len(impossible_high)),
        "min": float(df[time_col].min()),
        "max": float(df[time_col].max()),
        "mean": float(df[time_col].mean()),
        "median": float(df[time_col].median()),
    }


def check_distance_sanity(df, dist_col="distance_to_station_km"):
    return {
        "n_negative": int((df[dist_col] < 0).sum()),
        "n_over_10km": int((df[dist_col] > 10).sum()),
        "min": float(df[dist_col].min()),
        "max": float(df[dist_col].max()),
    }


def check_categorical_consistency(df):
    issues = {}
    if "current_transport_mode" in df.columns:
        issues["transport_mode_values"] = sorted(df["current_transport_mode"].unique().tolist())
    if "adoption_potential_group" in df.columns:
        issues["adoption_group_values"] = sorted(df["adoption_potential_group"].unique().tolist())
        # check score/group alignment on a sample basis
    return issues


def run_full_quality_report(df, stage_name=""):
    print(f"--- Data quality report: {stage_name} ---")
    report = {}
    report["missing_duplicates"] = check_missing_and_duplicates(df)
    if "home_lat" in df.columns:
        report["coordinates"] = check_coordinate_validity(df)
    if "door_to_door_time_min" in df.columns:
        report["commute_time"] = check_commute_time_sanity(df)
    if "distance_to_station_km" in df.columns:
        report["distance"] = check_distance_sanity(df)
    report["categorical"] = check_categorical_consistency(df)
    for section, content in report.items():
        print(f"\n[{section}]")
        for k, v in content.items():
            print(f"  {k}: {v}")
    return report
