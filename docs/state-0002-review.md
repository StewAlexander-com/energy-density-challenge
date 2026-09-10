# Ten cumulative reviews: what should we learn next?

September 10, 2026. One AI-assisted review developed in ten successive passes. These passes are not ten independent reviewers, a completed experiment or a systematic literature review. Each pass carries a correction into the next. The attached directive is preserved verbatim in [the source directive](state-0002-directive.txt).

## 01 — Preserve the actual starting point

**Question:** What are we being asked to preserve, and does it exist?

**Finding:** State 0001 questioned energy density as the objective and proposed service-specific comparison. Its model, hypothesis and first desk audit remain untested. The directive assumes an existing Merkle-backed research DAG; the implementation has Git history and linked JSON records, not that application-level graph. It also calls the first state independent, but independent review was never established.

**Revision carried forward:** Preserve the complete tracked repository at commit `3b55fbab2ea9b94e0f78e9d458d5f6144cbed026` as ASTRA-STATE-0001. Add explicit SHA-256 manifests and parent links now, with their creation provenance. Hashes detect changes relative to a trusted reference; they do not prove correctness, completeness, independence or permanent availability. No missing reasoning is reconstructed as historical fact.

## 02 — Separate two claims that could fail differently

**Learning from 01:** Preserving the baseline does not validate its method.

**Challenge:** “Directing intelligence at energy problems” could describe almost any research institution. It does not yet identify a measurable treatment. “Intelligence” also invites a vague latent score.

**Revision carried forward:** Use a narrower working object: a protocol for choosing the next research action under stated resource limits. Program A tests interventions for a defined energy service. Program B tests whether this decision protocol improves choices against credible alternatives. Neither has produced a completed project study. An interesting idea in A is not evidence of an advantage in B.

## 03 — Check the claimed novelty before inventing terminology

**Learning from 02:** A measurable process must specify what differs from established practice.

**Prior art:** [NIST's value-of-information overview](https://www.nist.gov/publications/value-information-and-decision-pathways-concepts-and-case-studies) connects information costs to decision benefits. [NIST's experimental-design introduction](https://www.itl.nist.gov/div898/handbook/pri/section1/pri11.htm) describes planning controlled changes and observing responses. [COS preregistration guidance](https://www.cos.io/initiatives/prereg) separates planned tests from exploratory work. [W3C PROV](https://www.w3.org/TR/prov-overview/) provides an existing provenance vocabulary.

**Revision carried forward:** Classify decision analysis, experimental design, preregistration and provenance as established methods. Our synthesis combines bounded action comparison, retained dissent and auditable allocation records. A reusable, experimentally demonstrated improvement across energy cases could be a contribution; it has not been demonstrated or shown novel. A general scientific intelligence system remains speculation. Operations research, active learning, metascience, forecasting, robust optimization and automated laboratories are relevant adjacent fields still needing a deeper review.

## 04 — Optimize decisions, not a convenient information score

**Learning from 03:** Existing value-of-information methods offer a stronger starting point than a new universal “intelligence efficiency” ratio.

**Challenge:** Information gain may resolve an irrelevant parameter. A ratio can favor tiny cheap tasks while missing a decisive costly test. Dollars cannot silently substitute for scarce expert attention, delay, electricity, risk or environmental burden. A predicted information gain is itself uncertain and model-dependent.

**Revision carried forward:** First name the decision, beneficiary, feasible choices, time horizon and consequences of error. Then compare how an observation might change the decision, its reliability, cost ranges, opportunity cost and hard constraints. Retain separate resource measures and sensitivity to boundaries. Use expected net decision value only when probabilities and utilities are defensible; otherwise show conditional scenarios and non-dominated options. “Unknown” is not zero. A cheaper physical test wins only if it is feasible, safe and more useful for this decision; the directive's dollar examples are illustrations, not estimates.

## 05 — Give the process a chance to lose

**Learning from 04:** A process that consumes more resources must earn that expense through decision improvements.

**Prior evidence:** The [Vaccaro, Almaatouq and Malone abstract](https://arxiv.org/abs/2405.06087) reports heterogeneous human–AI effects, including average losses against the better solo participant in the included studies. The [Smit et al. abstract](https://arxiv.org/abs/2311.17371) reports that evaluated debate methods did not reliably beat other prompting strategies, with results sensitive to tuning. These findings motivate strong controls; neither study tests this protocol or establishes its energy-domain performance. The abstracts were read; the full papers were not evaluated in this pass.

**Revision carried forward:** Compare a frozen structured process against an expert, a competent single-model baseline and an unstructured group using the same participant pool as the structured group. Later add conventional teams, literature review and relevant optimization or laboratory workflows where the use case warrants them. Fix selection rules before evaluation; choosing the “best baseline” after seeing test outcomes introduces bias. The protocol earns no credit merely for beating an intentionally weak comparator.

## 06 — Protect independence and expose manipulation

**Learning from 05:** More participants and more confident prose may increase cost without adding independent signal.

**Challenge:** Premature sharing, common source packets, memorized cases, an AI judging its own answers, selective case choice and founder-controlled success criteria can all produce apparent agreement. Humans can omit costly harms; agents can inflate novelty, split one claim into many or repeatedly sample until a score improves.

**Revision carried forward:** Record first responses before sharing; disclose exposure, source overlap, model versions and roles. Different model names alone do not establish independence. Preserve incompatible predictions in separate branches. Use withheld outcomes, independent scoring where feasible, a fixed case list, locked rubrics and full failed-run accounting. Log deviations and conflicts. Seek counterexamples and anomalies, including boundary changes and stakeholder objections. Unknown unknowns cannot be listed in advance; these procedures may expose them but cannot guarantee coverage.

## 07 — Repair the loop and make stopping operational

**Learning from 06:** A well-documented discussion can still become an expensive echo chamber.

**Challenge:** The proposed loop allocates resources after testing, although allocation is needed before every action. It omits an explicit resource and permission gate. Repeating all eight stages for each trivial choice can become overhead.

**Revision carried forward:** Define the decision and limits → propose competing explanations and actions → choose a discriminating next step → check feasibility, permission and cost → prerecord the plan → act only when authorized → assess the observation → update or preserve branches → choose again, wait or stop. These are checks, not a mandatory meeting cycle. After two review rounds with no decision-relevant change, pause and justify the value of another round; this provisional trigger is itself subject to evaluation. Safety, missing authority or an exhausted cap blocks execution. Waiting names a revisit trigger and owner. An infeasible experiment is not the next action merely because it would be informative.

## 08 — Design the least expensive useful evaluation

**Learning from 07:** Before running a comparative trial, discover whether the decision task can even be scored without rewarding style.

**Proposal:** Start with a three-case feasibility screen using existing, licensed evidence and outcomes withheld by a curator. Check whether two reviewers can apply an outcome-anchored decision rubric and whether cases leak their answers. This is a proposed design, not a performed study or proof that three is statistically sufficient.

**Next if feasible:** A proposed twelve-case pilot across two energy services, with four prespecified processes from pass 05. Use the same information cutoff, permitted evidence access and comparable caps; log actual human time, inference, spend and elapsed time separately. Do not equalize human and machine work by inventing a conversion factor. Blind scorers to process labels and control carryover. Preregister cases, budget, sample rationale, primary decision-loss measure, tolerances, stopping rule and analysis before trial outputs. These details remain unfilled. More cases and prospective validation would be needed to estimate calibration or generalize.

**Revision carried forward:** The immediate recommendation is to design and review the feasibility screen. No participant recruitment, spending, research run or physical experiment is authorized by this page. [The pilot specification](allocation-pilot.md) explains what would count against the protocol and what must be registered first.

## 09 — Preserve history without building a shrine to hashes

**Learning from 08:** Evaluation needs auditable choices and outcomes, not an impressive diagram.

**Challenge:** Making every noun a node would create an elaborate ontology before the smallest trial. Rewriting old records to fit it would destroy precisely the history we want to study. A causal feedback loop is not a provenance DAG.

**Revision carried forward:** Add a minimal process graph containing the two competing process hypotheses, a proposed evaluation, an allocation decision, a resource boundary and a stop condition. Its edges describe dependencies, not measured causes. Keep the existing energy model and all original scientific records byte-for-byte intact. Create State 0002 as a child of State 0001 using parent manifest hashes. Store exact source bundles, file digests and deterministic Merkle roots, plus a human change record. Repository policy rejects edits to published states; a trusted prior copy or commit is still needed to detect coordinated rewriting of the archive and its reference hashes.

## 10 — Make the addition understandable and hard to misuse

**Learning from 09:** The smallest useful interface explains a decision before showing its archival machinery.

**Decision:** Retain the homepage's service-first question, examples, model explorer, calculator and contribution draft. Add one short entry to “What should we learn next?” The new page separates energy outcomes from process performance, exposes a bounded next-step checklist, and labels every recommendation as a planning aid. It does not rank research actions automatically, run agents, spend money or certify readiness.

**Guardrails:** Blank answers cannot produce a recommendation. Unknown feasibility or resources cannot yield a test recommendation. A stalled discussion can lead to waiting or reframing. Edits invalidate the previous suggestion. Technical history, the ten passes and source limits stay in expandable sections or linked documents. Keep normal spacing, readable type, keyboard controls and existing sharing, AI files and MIT notices.

**State 0002 verdict:** Proceed only with designing a cheap test of this narrower protocol. Reject claims that the abstraction is established, the synthesis is novel, multiple intelligences must win or a hash proves truth. The new abstraction is more testable; its practical benefit remains uncertain. This is a conceptual design decision, not an experimental finding.
