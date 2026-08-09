"""
data_generation.py

Builds the synthetic employee population.

I did not want to just scatter random lat/lon points inside a bounding box
around Hamburg, because that produces employees in the middle of lakes,
industrial zones, or the Elbe not a plausible residential distribution.
Instead I anchor sampling around a set of real residential areas/towns
(config.RESIDENTIAL_AREAS) with rough population-based weights, and then
add a small random jitter around each area's centre to spread employees out
within that area without leaving it.

None of this represents actual J&J employees. It's a plausible hypothetical
population for scenario analysis, built and validated the way I'd want a
reviewer to be able to check.
"""

import numpy as np
import pandas as pd

from config import RESIDENTIAL_AREAS, N_EMPLOYEES, RANDOM_SEED


def _sample_area_jitter(rng, area, n, spread_km=2.5):
    """
    Sample n points around an area's centre with gaussian jitter.
    spread_km controls how tightly points cluster around the area centre --
    2.5km is roughly the radius of a small-to-medium Hamburg district, which
    felt like a reasonable order of magnitude rather than a precise figure.
    """
    # convert km jitter to approximate degrees (rough, fine at this latitude)
    km_per_deg_lat = 111.0
    km_per_deg_lon = 111.0 * np.cos(np.radians(area["lat"]))
    lat_jitter = rng.normal(0, spread_km / km_per_deg_lat, n)
    lon_jitter = rng.normal(0, spread_km / km_per_deg_lon, n)
    return area["lat"] + lat_jitter, area["lon"] + lon_jitter


def generate_synthetic_employees(n_employees=N_EMPLOYEES, seed=RANDOM_SEED):
    rng = np.random.default_rng(seed)

    areas = RESIDENTIAL_AREAS
    weights = np.array([a["weight"] for a in areas])
    area_assignment = rng.choice(len(areas), size=n_employees, p=weights)

    home_lat = np.empty(n_employees)
    home_lon = np.empty(n_employees)
    home_area = np.empty(n_employees, dtype=object)

    for area_idx in range(len(areas)):
        mask = area_assignment == area_idx
        n_in_area = mask.sum()
        if n_in_area == 0:
            continue
        lat, lon = _sample_area_jitter(rng, areas[area_idx], n_in_area)
        home_lat[mask] = lat
        home_lon[mask] = lon
        home_area[mask] = areas[area_idx]["name"]

    employee_id = [f"EMP{str(i).zfill(4)}" for i in range(1, n_employees + 1)]

    # --- Demographic / commuting attributes -----------------------------
    # age_group: I used a distribution weighted toward the working-age
    # bands one would typically see in a company workforce, skewed toward
    # 25-44, with smaller shares at the younger and older ends. This is an
    # assumption, not a measured HR statistic -- documented in
    # docs/assumptions.md.
    age_group = rng.choice(
        ["18-24", "25-34", "35-44", "45-54", "55-64"],
        size=n_employees,
        p=[0.08, 0.32, 0.28, 0.20, 0.12],
    )

    household_type = rng.choice(
        ["single", "couple_no_children", "family_with_children"],
        size=n_employees,
        p=[0.32, 0.30, 0.38],
    )

    work_days_per_week = rng.choice([2, 3, 4, 5], size=n_employees, p=[0.05, 0.15, 0.30, 0.50])

    # driving_license: assumed high given German adult population norms
    driving_license = rng.choice([True, False], size=n_employees, p=[0.85, 0.15])

    # car_access conditioned on driving_license and household_type: a
    # single person without children is somewhat less likely to have a
    # car readily available than someone in a family household, all else
    # equal. This is a reasonable qualitative assumption, not a fitted model.
    car_access = np.zeros(n_employees, dtype=bool)
    for i in range(n_employees):
        if not driving_license[i]:
            car_access[i] = False
            continue
        base_p = 0.55 if household_type[i] == "single" else 0.75
        car_access[i] = rng.random() < base_p

    current_transport_mode = []
    for i in range(n_employees):
        if car_access[i]:
            probs = {"car": 0.65, "public_transport": 0.20, "bike": 0.10, "mixed": 0.05}
        else:
            probs = {"car": 0.05, "public_transport": 0.55, "bike": 0.20, "mixed": 0.20}
        modes, p = zip(*probs.items())
        current_transport_mode.append(rng.choice(modes, p=p))

    df = pd.DataFrame({
        "employee_id": employee_id,
        "home_area": home_area,
        "home_lat": home_lat,
        "home_lon": home_lon,
        "age_group": age_group,
        "household_type": household_type,
        "work_days_per_week": work_days_per_week,
        "driving_license": driving_license,
        "car_access": car_access,
        "current_transport_mode": current_transport_mode,
    })
    return df


if __name__ == "__main__":
    df = generate_synthetic_employees()
    print(df.head())
    print(df.shape)
