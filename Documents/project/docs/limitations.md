# Limitations

## Synthetic population
- This population does not represent real J&J employees. Any resemblance in home-area distribution, demographics, or commuting patterns to J&J's actual workforce is coincidental — no real employee data was used or seen.
- Population weights across residential areas are ordinal assumptions about relative area size, not census or company HR data.
- The demographic generation logic (car access, transport mode) was deliberately designed so that later validation checks would show sensible patterns (e.g. car-access employees skew toward driving). That means those checks validate the *generation logic*, not any real-world finding.

## Public transport data
- **No live routing was performed.** I don't have network access to the HVV routing engine, a downloaded GTFS feed, or the OpenStreetMap Overpass API inside this environment. Commute times are estimated from a documented formula (walking speed, average wait, line speed, network-distance factor, transfer penalty) rather than observed or routed.
- **Only 16 reference stations were used**, a small subset of HVV's actual, much denser station network. This likely overstates walking distances and commute times for residential areas that, in reality, have closer stations I didn't include (e.g. within central Hamburg, where the real network is far denser than my Norderstedt/AKN-corridor-focused reference set).
- Schedule frequency, real-time delays, and seasonal timetable variation are not modelled — the "average wait time" is a single fixed planning assumption, not derived from actual headways.
- The transfer rule ("AKN A1 always requires one transfer, U1 never does") is a simplification; in reality this would depend on the specific station pair and time of day.

## Adoption-potential scoring
- **No observed adoption outcomes exist** in this dataset, or realistically anywhere accessible for this exercise. The adoption-potential score is a transparent, interpretable heuristic — useful for segmentation and prioritisation — not a validated prediction of actual purchase behaviour.
- Component weights (35/30/20/15%) are reasoned assumptions tied to the assessment's own framing of what drives adoption, not fitted to any data.
- The score does not account for price sensitivity, employer subsidy availability, or individual willingness to pay — none of which exist in this dataset.

## Geographic sampling bias
- The 9 residential areas were chosen because they're real, named places along or near the Norderstedt/Hamburg-North corridor — not because they're an exhaustive or unbiased sample of where J&J employees plausibly live. A real address dataset (which the assessment explicitly prohibits using) would very likely show a different area mix.

## Difference between "adoption potential" and "actual adoption"
Everywhere this notebook refers to adoption potential, it means: *given this synthetic scenario's assumptions, this employee profile has characteristics associated with higher or lower likely interest in a Deutschlandticket.* It is not a claim about how many employees would actually buy one.
