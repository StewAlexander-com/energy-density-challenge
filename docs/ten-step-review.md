# Ten cumulative reviews of the founding brief

Date: 2026-09-10 (UTC). Scope: conceptual and implementation review, not an experimental finding or a systematic literature review. Each pass changes the input to the next. This is one AI-assisted review sequence, not ten independent reviewers.

## 01 — Test the choice of problem

**Input:** The brief names an energy-density challenge before establishing the binding problem.

**Finding:** Its strongest feature is permission to be wrong. Its central vulnerability is anchoring: a name can silently become a conclusion. An open-ended statement that an intervention “may” help somewhere is not by itself a discriminating, falsifiable research claim.

**Revision:** First ask: “For a specified useful service, what constraint matters most, and which intervention improves the outcome without unacceptable burdens elsewhere?” Keep the project name provisional and treat density as one candidate.

**Carry forward:** No technology search is prioritized until a service, beneficiary, and decision are specified.

## 02 — Separate the quantities

**Input from 01:** A service is the target; energy density is a possible means.

**Finding:** Stored energy per kilogram, energy per litre, power, useful work per joule, computation per joule, and lifecycle cost are not interchangeable. Fuel-only, cell, pack, and installed-system figures have different boundaries. Quality, duration, duty cycle, and reliability can change the comparison.

**Revision:** Record units and the complete system boundary for each metric. Select the binding constraint per use case. For computation, fix task quality and latency; for heat, specify temperature; for mobility, specify payload, distance, and duty cycle. Never rank a battery cell directly against an entire generating plant.

**Carry forward:** A comparison with mismatched units, services, or boundaries is incomplete, not a winner.

## 03 — Audit the causal story

**Input from 02:** The candidate variable must be specific and comparable.

**Finding:** No original model, methodology, edge list, or source set was supplied. Connectivity does not establish causal leverage, intervention magnitude, feasibility, or tractability. Adding more sectors to a graph does not supply evidence.

**Revision:** At the user's request, create a new, explicitly proposed qualitative model, EDC-M-0001. Every directed edge is an untested conditional hypothesis, with an assumption and a discriminating test. Equal visual weight avoids suggesting measured strength. No centrality ranking or causal effect estimate is reported.

**Carry forward:** The model generates questions. It cannot establish that energy density is the best intervention.

## 04 — Give alternatives a fair test

**Input from 03:** A map can nominate candidates, not select winners.

**Finding:** A search restricted to energy technologies can overlook efficiency, maintenance, infrastructure, access, financing, or changes in demand. “Do nothing” may preserve an unacceptable service deficit; it still needs an explicit description.

**Revision:** Compare the density intervention with the current baseline, best feasible existing alternative, demand/service redesign, and infrastructure or operational improvement. Allow evidence-backed exclusion of an irrelevant category. Match the service, reliability, deployment window, accounting boundary, and resource budget. Report additional service separately from efficiency savings.

**Carry forward:** Density earns priority only in a bounded comparison where it addresses an actual constraint.

## 05 — Follow the displaced burdens

**Input from 04:** Alternatives need an equal accounting basis.

**Finding:** The entropy refrain is memorable, but entropy is not a synonym for toxicity, cost, mineral dependence, or political risk. Local efficiency can coexist with increased aggregate consumption. Demand growth is not automatically evidence of a price-induced rebound effect.

**Revision:** Keep “Where did the entropy go?” and add a precise subtitle: “Where did the burdens go?” Separate energy and exergy accounting from lifecycle and distributional accounting. Track extraction, manufacturing, conversion, storage, delivery, use, maintenance, replacements, and end of life; name omissions. Report totals as well as per-service metrics, geography, timing, affected groups, uncertainty, and demand scenarios. Measure causal rebound separately from unrelated growth.

**Carry forward:** An attractive ratio cannot conceal a larger absolute burden or transfer of harm to another community.

## 06 — Make failure decidable

**Input from 05:** A meaningful claim is bounded and has more than one outcome.

**Finding:** “Substantially improve” and “decrease total costs” lack thresholds, comparators, and decision rules. A universal positive result across every dimension is unlikely; an arbitrary weighted score can hide the tradeoff.

**Revision:** Register scope, baseline, measurable prediction, minimum relevant improvement, uncertainty method, hard constraints, and a falsifier before inspecting results. Stakeholders must set thresholds with a rationale; this launch does not invent universal numbers. Preserve nondominated options and unresolved tradeoffs. With uncertain or missing measurements, say “ordering unresolved.” Record whether the framing should be retained, narrowed, replaced, or left unresolved.

**Carry forward:** No evidence status is upgraded because an AI sounds confident, a vote agrees, or a form is complete.

## 07 — Start with the cheapest useful test

**Input from 06:** A decision requires a test capable of changing it.

**Finding:** The first needed experiment is a framing audit, not a new battery, reactor, or autonomous laboratory. A literature/model comparison is useful but is not experimental replication.

**Revision:** Propose EDC-E-0001: select one bounded service with a relevant practitioner; preregister comparison rules; collect provenance-bearing data; compare density with non-density interventions; vary uncertain assumptions; publish the decision and missing data. Equipment is a computer and source access. The protocol stays proposed until its service, thresholds, and dataset are registered. Record a negative result as research output.

**Carry forward:** Use the initial audit to decide whether a physical experiment is justified, not to claim the umbrella hypothesis is validated.

## 08 — Separate independent work from consensus

**Input from 07:** The audit needs criticism that could change the result.

**Finding:** Different role prompts are not independent evidence. Models may share training data, sources, and failure modes. A public static repository cannot enforce blind work, run agents, or safely dispatch compute.

**Revision:** Specify independent initial evidence summaries using the same frozen question. Record model/provider or human expertise, source overlap, conflicts, and exposure to others' conclusions. Participants voluntarily withhold initial drafts until a release point; publish timestamped summaries or precommitted digests and reveal the matching content. This supplies an audit trail, not proof of independence. Compare claim-level disagreements and propose discriminating tests. “Converge” means decide the next action; unresolved dissent is a valid output.

**Carry forward:** The repository documents this protocol. It does not claim that a multi-AI system or blind review service is running.

## 09 — Make the memory difficult to misuse

**Input from 08:** Scientific memory must preserve disagreement, provenance, and limits.

**Finding:** Moving failed hypotheses can break permanent links. Status labels alone can blur a proposed test, simulation, observation, and independent replication. JSON can be machine-readable while remaining semantically misleading.

**Revision:** Keep canonical records at permanent paths; use falsified/unresolved indexes that refer to them. Validate required fields, IDs, reference targets, unknown values, and the evidence requirements for status changes. Keep a dated confidence history with reasons and conditions; no fabricated probability. Add versioning, licensing, contribution review, corrections, data provenance, and the explicit human safety boundary. Failed and superseded records remain retrievable.

**Carry forward:** Unknown is stored as null with a reason, never zero. An accepted contribution is not an accepted scientific claim.

## 10 — Turn the corrected question into a usable interface

**Input from 09:** The site can make the research process visible and difficult to misread.

**Finding:** The original long homepage risks hiding the first task under ambition, role lists, and diagrams. A network or confidence meter can imply evidence that does not exist.

**Revision:** Lead with “First, test the question.” Show the framing verdict and evidence gap immediately. Provide three clear routes: inspect the ten-step review, explore the proposed model, and contribute a bounded question. Use short labels, native disclosure controls, keyboard access, strong contrast, mobile layouts, and plain-language explanations. Mark illustrative arithmetic, proposed models, and proposed experiments beside the content itself. Validate contribution drafts, preview before export, and never transmit them automatically. Provide static-readable content and machine-readable files from the same records.

**Carry forward / launch decision:** Proceed as a problem-framing research commons. Do not proceed as a campaign asserting that energy density is humanity's principal bottleneck. The first open task is a bounded framing audit; the first model is proposed and uncalibrated. Revisit the project name if evidence favors a different intervention.

## What would change this decision?

An auditable model with causal identification and sensitivity analysis could strengthen the leverage case. A preregistered application-level comparison could justify prioritizing density within that application. Better performance by an alternative could narrow or replace that framing. None of these results would automatically establish a global ranking of humanity's problems.

## Sources and limits

The supplied brief is the design input. This review is an analysis of that input, not an exhaustive survey. [DOE's hydrogen-storage explanation](https://www.energy.gov/cmei/fuels/hydrogen-storage) illustrates why mass, volume, application, and storage-system constraints differ. [MIT's thermodynamics notes](https://web.mit.edu/16.unified/www/FALL/thermodynamics/notes/node49.html) distinguish available work and entropy generation. These sources support definitions, not this project's leverage hypothesis.

IPCC AR6 Working Group III chapters 5 and 6 are recorded as literature leads. Direct retrieval returned HTTP 403 during this review; their contents were not fully verified and are not used to claim a project finding. See the source ledger for access status and scope.
