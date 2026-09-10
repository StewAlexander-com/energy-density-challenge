# Research templates

Templates are unregistered drafts. Maintainers allocate permanent identifiers before merge.

## Hypothesis

Title; service and beneficiary; functional unit; place and time; installed-system boundary; baseline and feasible alternatives; statement and mechanism; assumptions; predicted measurement; minimum improvement and hard constraints; uncertainty; source evidence and scope; falsifier; signal/noise/bias/unknowns; possible omitted boundaries; safety scope; dated status rationale. Use `schemas/hypothesis.schema.json` and the initial hypothesis as a structural example, not as measured evidence.

## Experiment

1. Hypothesis and permanent hypothesis ID.
2. Physical mechanism.
3. Required assumptions.
4. Predicted measurable result.
5. Cheapest discriminating test.
6. Required equipment.
7. Expected uncertainty and analysis method.
8. Safety review and approved scope where applicable.
9. Result that would falsify the registered claim.
10. Replication procedure, data and source snapshots.

Before setting status to registered, fill the preregistration date, service, functional unit, boundary, baseline and thresholds. See `schemas/experiment.schema.json`.

## Result

Permanent result and experiment IDs; evidence kind (desk analysis, simulation, observation or experimental result); date; methods; licensed data; observed outcome and uncertainty; exclusions/deviations; limitations; authors and provenance; replication group; safety scope; conclusion within tested conditions. Do not count a simulation or repeated model answer as an independent physical replication. See `schemas/result.schema.json`.

## Dataset

Title; origin URL and location; author; collection method and dates; units; functional unit and boundary; geography; license and redistribution rights; file checksum; missing-value meaning; known bias and uncertainty; transformations and reproducible code; personal-data restrictions.

## Red-team note

Claim ID; strongest counterexample; unsupported assumption; affected metric or boundary; prior art or negative evidence; possible harm transfer; cheapest discriminating test; what would change the critique; source access status; reviewer exposure to earlier conclusions.
