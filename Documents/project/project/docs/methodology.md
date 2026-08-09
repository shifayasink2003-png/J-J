# Methodology

## Pipeline overview

```
Real HVV/AKN station geography (public knowledge, cross-checked against
the official GTFS feed's existence/licensing)
        │
        ▼
Synthetic employee population (anchored on real residential areas,
documented demographic assumptions) ── src/data_generation.py
        │
        ▼
Nearest-station lookup (haversine distance) ── src/geospatial.py
        │
        ▼
Door-to-door commute time estimate (walk + wait + transit + transfer
+ final walk) ── src/transport.py
        │
        ▼
Commute-time grouping (<=30 / 31-45 / 46-60 / >60 min)
        │
        ▼
Deutschlandticket adoption-potential score (interpretable, weighted,
not a trained model) ── src/scoring.py
        │
        ▼
Geographic aggregation by residential area
        │
        ▼
Business recommendations
```

## Key methodological decisions

**Why straight-line distance + a network factor, instead of real routing?**
This environment cannot reach the HVV routing API or a downloaded GTFS feed (see `docs/data_sources.md`). Rather than fabricate a "routed" time, I built a transparent formula from documented planning-level assumptions and labelled every resulting number as an estimate. This is a limitation I'd remove first if given real API/network access.

**Why 9 residential areas instead of a bounding-box sample?**
A uniform bounding-box sample around Hamburg would place synthetic homes in the Elbe, industrial zones, and other non-residential land. Anchoring on real named areas with population-plausible weights produces a population that at least looks like where people actually live, even though the weights themselves are assumptions rather than census figures.

**Why a scoring framework instead of a supervised ML model for adoption?**
There is no observed Deutschlandticket adoption outcome anywhere in this data — no employee has actually been offered a ticket and either bought or declined it. Training a classifier without a real target would produce a confident-looking number with no ground truth behind it, and risks being read as more rigorous than it is. An interpretable, documented weighted score achieves the assessment's actual goal (identify factors, segment employees, support a business decision) without that risk, and it's something a stakeholder can question and adjust component by component.

**Why not use clustering (e.g. k-means) for commute-time or adoption groups?**
The assessment specifies mutually exclusive commute-time buckets (≤30/31–45/46–60/>60 min) and asks for "High/Medium/Low" adoption categories — both are naturally handled with fixed, explainable thresholds. Unsupervised clustering would add complexity without a clear question it answers better than the threshold-based approach.

## Reproducibility

- Fixed random seed (`RANDOM_SEED = 42` in `src/config.py`) controls all synthetic generation.
- All commute-time and scoring formulas are deterministic given the generated population — re-running the notebook end to end reproduces identical results.
