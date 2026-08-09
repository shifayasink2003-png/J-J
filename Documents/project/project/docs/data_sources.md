# Data Sources

## Real / public sources referenced

### HVV (Hamburger Verkehrsverbund) GTFS feed
- **Name:** hvv Fahrplandaten (GTFS)
- **URL:** https://suche.transparenz.hamburg.de/dataset/hvv-fahrplandaten-gtfs-januar-2025-bis-dezember-2025 (Hamburg Transparency Portal / GovData)
- **Date accessed:** 2026-08-08 
- **License:** Published under Hamburg's open-data transparency portal terms (dl-de/by-2-0 style attribution license, typical for this portal)
- **Purpose:** Used to confirm which real transit lines (U1 U-Bahn, AKN A1 regional line) and stations actually serve the Norderstedt/Hamburg-North corridor, and to source real station names and approximate locations for `src/config.py`.
- **Relevant fields:** stop names, stop locations, route/line identifiers (not accessed directly — see limitation below)

## Synthetic data

The employee-level dataset (locations, demographics, transport mode, commute times, adoption scores) is entirely synthetic, generated in `src/data_generation.py` with a fixed random seed (42) for reproducibility. It does not represent real J&J employees. Full generation logic and assumptions are documented in `assumptions.md`.

