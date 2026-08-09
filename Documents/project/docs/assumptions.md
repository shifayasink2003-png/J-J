# Assumptions

Every assumption below lives as a named constant in `src/config.py` — this document explains the reasoning, the config file has the actual values.

## Population size
- **N = 500 synthetic employees.** Large enough to get stable percentage/area-level statistics without being an arbitrary "big round number." No claim is made that this matches J&J's actual site headcount.

## Geographic sampling
- Employees are anchored to **9 real residential areas** around Hamburg and Norderstedt (Norderstedt itself, Langenhorn, Fuhlsbüttel, Ohlsdorf, Alsterdorf, Quickborn, Kaltenkirchen, Hamburg-Innenstadt, Henstedt-Ulzburg) rather than sampled uniformly inside a bounding box, which would put employees in the middle of the Elbe, industrial land, or a lake.
- Each area has a **relative population weight** (roughly ordinal, based on general knowledge of the areas' relative sizes — not a fitted statistic) controlling what share of the 500 employees are anchored there.
- Within an area, home locations are jittered with **Gaussian noise, spread ≈ 2.5 km**, chosen as a rough order-of-magnitude for a small-to-medium district, not a precise value.

## Demographics
- `age_group` distribution skews toward 25–44 (a typical working-age company profile assumption), not based on J&J's actual workforce data.
- `household_type`, `driving_license` (85% assumed licensed), and `car_access` (conditioned on license + household type) are assumption-based, calibrated to plausible German adult population norms, not measured statistics.
- `current_transport_mode` is generated conditionally on `car_access`: employees with car access skew toward driving; employees without skew toward public transport/bike/mixed. This is a designed relationship, meant to make the later adoption-score validation meaningful, not an empirical finding.

## Commute-time formula components
- **Walking speed: 4.5 km/h** — standard adult walking-speed planning assumption.
- **Average wait time: 6 minutes** — a planning-level assumption for reasonably frequent urban/suburban service, not a measured HVV headway.
- **Transfer penalty: 5 minutes** — flat cost per required interchange (walk + wait combined), applied only when the nearest station is on the AKN A1 line, which I assume typically requires an interchange onto U1 (or a bus) to reach the workplace corridor.
- **Network distance factor: 1.3×** straight-line distance — transit lines follow fixed corridors, not straight lines; 1.3× is a common planning-level approximation for urban network circuity, not derived from actual HVV routing.
- **Line speeds:** U1 ≈ 32 km/h, AKN A1 ≈ 45 km/h (average scheduled speed including stops) — approximate, based on general knowledge of U-Bahn vs regional-line operating speeds, not sourced from a timetable.
- **Final walk (station to workplace door): fixed 12 minutes** for all employees, since everyone arrives at effectively the same workplace-side stop near Norderstedt Mitte.

## Deutschlandticket adoption-potential score
- Score = weighted sum of four 0–100 normalised components: commute time (35%), connectivity/transfers (30%), car-access penalty (20%), current transport mode (15%).
- **Weight rationale:** commute time and connectivity together make up 65% of the score. Car access and current mode are included because someone with an easy existing alternative is less likely to switch regardless of how good the PT commute looks on paper.
- **Thresholds:** High potential ≥ 70, Medium potential ≥ 45, Low potential below 45 — round, defensible cut points on the 0–100 scale, not derived from any external benchmark (none exists for this synthetic scenario).
