# J&J
# Deutschlandticket Commuting Analysis — J&J Medical GmbH, Norderstedt

## Business problem

Would promoting the Deutschlandticket actually make commuting easier, cheaper, and more sustainable for employees at Johnson & Johnson Medical GmbH's Norderstedt site? Real employee addresses can't be used for this, so the approach here is a scenario analysis: build a plausible synthetic employee population, estimate their door-to-door public transport commute, and turn that into a transparent Deutschlandticket adoption-potential score.

## Objective

1. Estimate what share of a synthetic employee population would have a public-transport commute within 30 / 45 / 60 minutes.
2. Build an interpretable Deutschlandticket adoption-potential score and segment employees by it.
3. Identify which residential areas have strong vs weak public transport connectivity to the site.
4. Turn all of the above into a targeted business recommendation, not a blanket one.

## Methodology (short version — full detail in `docs/methodology.md`)

Synthetic population (anchored on real Hamburg/Norderstedt residential areas) → nearest real HVV/AKN reference station → estimated door-to-door commute time (documented formula, not live-routed — see limitations) → commute-time grouping → adoption-potential scoring (interpretable, weighted, not a trained ML model) → area-level aggregation → recommendations.

## Data sources

Real HVV/AKN station geography (cross-referenced against Hamburg's official open-data GTFS feed) plus a fully synthetic, documented employee population. Full sourcing detail is in `docs/data_sources.md`.

## Key results

See `docs/executive_summary.md` for the full write-up. Headline: roughly 40% of this synthetic population sits within a 60-minute estimated commute, concentrated in Norderstedt and the U1 corridor; adoption potential follows a similar geographic pattern.

## Repository structure

```
project/
├── README.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   └── deutschlandticket_commuting_analysis.ipynb
├── src/
│   ├── config.py            # all assumptions, station/area reference data, weights
│   ├── data_generation.py   # synthetic employee population
│   ├── geospatial.py        # distance + nearest-station helpers
│   ├── transport.py         # door-to-door commute time estimation
│   ├── scoring.py           # Deutschlandticket adoption-potential score
│   ├── data_cleaning.py     # data-quality checks
│   └── visualization.py     # charts + interactive Folium map
├── data/S
│   ├── processed/           # final employee-level analysis dataset
│   └── synthetic/           # raw synthetic population before enrichment
├── outputs/
│   ├── figures/              # all notebook charts, saved as PNG
│   ├── tables/                # area_level_summary.csv
│   └── maps/                  # commute_map.html (interactive)
└── docs/
    ├── data_sources.md
    ├── assumptions.md
    ├── methodology.md
    ├── limitations.md
    ├── executive_summary.md
    └── assessment_checklist.md
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## How to run

```bash
jupyter notebook notebooks/deutschlandticket_commuting_analysis.ipynb
```

Run all cells top to bottom. The random seed is fixed (42), so re-running reproduces identical results. To regenerate the notebook itself from scratch (e.g. after editing `build_notebook.py`), run:

```bash
python build_notebook.py
jupyter nbconvert --to notebook --execute --inplace notebooks/deutschlandticket_commuting_analysis.ipynb
```

## Limitations (short version — full detail in `docs/limitations.md`)

- Commute times are **estimated**, not routed against a live HVV timetable.
- Only 16 reference stations were used, a simplification of HVV's real, denser network.
- There is no observed Deutschlandticket adoption data anywhere — the adoption score is a transparent heuristic for segmentation, not a validated prediction.
- The synthetic population does not represent real J&J employees.

## Future improvements

- Swap the estimated commute-time formula for real HVV routing (or an OSM-based routing engine) if network access allows.
- Use a denser, more complete HVV/AKN station list, ideally pulled directly from the official GTFS feed.
- Validate the adoption-score weights against real survey or pilot data if J&J ever ran an actual employee survey on this topic.


