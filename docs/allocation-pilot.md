# A cheap test before a larger research system

Status: proposed; not registered, funded or run. Record: [EDC-V-0001](../research/evaluations/EDC-V-0001.json). The following counts describe a design candidate, not a power calculation or a completed study.

## First check whether the task is measurable

Propose three previously resolved energy decision cases with licensed evidence. A curator prepares an information cutoff, feasible actions and an outcome-based reference rubric before participants see the cases. Withhold subsequent observations. Two reviewers independently try to apply the rubric and record disagreements, leakage risk and time needed. A decision that experts cannot score reliably is not rescued by asking an AI to grade it.

This screen asks whether a comparative study is feasible. It cannot demonstrate calibration, superiority or generality. Reject or revise cases with ambiguous ground truth, impossible resource estimates or likely outcome leakage. For public cases that a model may have memorized, record exposure and exclude contaminated cases under rules written in advance. If leakage cannot be controlled, switch to prospective outcomes rather than calling the replay independent.

## A small comparative pilot, if the screen passes

Candidate design: twelve cases spanning two clearly defined energy services. Lock the case selection, allocation of cases to conditions and analysis before producing trial outputs. The same underlying case should be comparable across processes; use independent participants or counterbalanced assignment to reduce carryover. The unit of analysis is the case, with repeats clustered appropriately, not every answer or agent as a new independent sample.

Compare four processes:

- A relevant expert working alone.
- One competent model with a frozen prompt and tool setup, chosen on separate development cases.
- A structured human–AI group using the proposed protocol.
- An unstructured group with the same participant composition, information and tools as the structured group.

The last comparison helps distinguish structure from simply having extra participants. The solo comparisons test whether the group earns its overhead. Additional conventional-team, literature-review, forecasting, optimization or laboratory baselines should be selected for a later domain-specific evaluation, not claimed tested here.

## Fair budgets and independent evaluation

Before the run, specify caps for elapsed time, spend, human attention and compute; use the same information cutoff and permitted access. Record actual resource use separately by unit. Different processes may use different fractions of a cap. Compare decision quality under matched constraints and inspect the quality–cost trade-offs; do not conceal overhead in free expert time. Include protocol setup, curation, review, failed attempts and opportunity costs, amortized only under an explicit scenario.

Outcome assessors should be unaware of process labels and separate from participants. Hide decorative formatting so presentation is not rewarded. Record identities, conflicts, prior case exposure, model versions, prompts, sources and tool access. Keep initial judgments before cross-exposure. Withhold trial outcomes from both participants and whoever selects a model or tunes a prompt.

## Measures that must be fixed before outcomes

Primary candidate: case-specific decision loss relative to prespecified acceptable actions and later observations. “Loss” must correspond to consequences in that service, not a generic prose-quality score. If it cannot be justified, the case is not ready. Register the smallest worthwhile improvement and tolerated harm before comparison.

Secondary diagnostics: identification of the discriminating observation, critical burden detection, elapsed time, actual resource use, inappropriate-action rate and whether a wait or stop decision was justified. Hypothesis counts, citation counts and falsification counts are not targets. Calibration needs enough independently resolved probabilistic predictions and a prechosen scoring method; a three-case screen or twelve-case pilot is not adequate grounds for a broad calibration claim. Exploratory metrics must be labeled and their multiplicity acknowledged.

Report uncertainty, case-level outcomes, clustering, exclusions, deviations, null results and negative cases. Do not average incompatible service losses without justified normalization. A win in one domain cannot stand in for another. Do not tune the protocol on the same cases used to claim its advantage.

## Gates and possible conclusions

Registration remains blocked until the case list and rights, participant availability, budget caps, primary rubric, assessor arrangements, minimum effect, harm tolerance, sample rationale, leakage handling, allocation design and stopping rule are specified and reviewed. The page does not recruit participants or authorize spending.

- **Revise the measurement task:** reviewers cannot apply a defensible rubric, or leakage invalidates the comparison.
- **Narrow or reject this implementation:** within the tested conditions, a credible comparator achieves meaningfully better choices or comparable choices at lower relevant cost, under the registered rule.
- **Leave unresolved:** uncertainty is too large to distinguish a useful gain from no useful gain. A nonsignificant result alone is not equivalence.
- **Earn a larger test:** the prespecified benefit and harm criteria are met within resource caps. Seek prospective, independent replication before broader claims.

The three-case screen is the cheapest proposed next evaluation because it can expose an unusable scoring task before buying multi-agent runs. Its actual cost is unknown until a curator, reviewers, cases and caps are available. The current allocation decision is to prepare this design for review, not to declare it ready or run it.
