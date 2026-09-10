/* A local planning checklist. It never authorizes or executes research. */
'use strict';
function nextResearchStep(values) {
  for (const key of ['decision','discriminator','feasible','resources','stalled']) {
    if (!['yes','no','unknown'].includes(values[key])) throw new Error('Answer every question, or choose “Not sure”.');
  }
  const result = (title, reason, requires) => ({title, reason, requires, status:'planning_only', execution_authorized:false});
  if (values.decision !== 'yes') return result('Define the decision first.', 'More reasoning is hard to value until you know what choice could change.', 'Name the useful service, beneficiary, boundary, alternatives and consequences of error with a relevant practitioner.');
  if (values.discriminator !== 'yes') return result(values.stalled === 'yes' ? 'Pause and reframe—or wait.' : 'Find an observation that could change the choice.', 'An action is not useful just because it produces more information.', 'State the competing predictions. Seek a different perspective or missing evidence; if no feasible discriminator exists, preserve disagreement and record a revisit trigger.');
  if (values.feasible !== 'yes') return result('Resolve feasibility and authority first.', 'A potentially informative test is not yet a permissible or practical action.', 'Get the relevant human review, identify the missing capability and consider a safe feasible alternative or waiting.');
  if (values.resources !== 'yes') return result(values.resources === 'no' ? 'Stop at the resource limit.' : 'Estimate the costs before committing.', 'Unknown or excessive costs cannot be treated as free resources.', 'Record time, human attention, compute, energy, money, displaced work and relevant burdens. Obtain caps or choose a smaller action; do not spend from this checklist.');
  if (values.stalled === 'unknown') return result('Check what changed in the recent rounds.', 'You cannot judge diminishing returns without a short record of decision-relevant changes.', 'Compare predictions, choices, boundaries and proposed tests across recent rounds before buying more reasoning.');
  return result(values.stalled === 'yes' ? 'Prepare the discriminating observation for review.' : 'Compare this action with feasible alternatives.', values.stalled === 'yes' ? 'Another similar discussion has no demonstrated advantage over obtaining the missing observation.' : 'The stated prerequisites are present, but this checklist does not establish which action has the best value.', 'Write how each possible outcome would change the decision, compare reliability and costs with waiting, and prerecord the chosen plan. Only the responsible person can authorize execution.');
}
if (typeof module !== 'undefined' && module.exports) module.exports = {nextResearchStep};
if (typeof document !== 'undefined') {
  const form = document.getElementById('allocation-form');
  if (form) {
    form.hidden = false;
    const output = document.getElementById('allocation-result');
    form.addEventListener('change', () => { output.hidden = true; });
    form.addEventListener('submit', event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const result = nextResearchStep(Object.fromEntries(new FormData(form)));
      document.getElementById('allocation-result-title').textContent = result.title;
      document.getElementById('allocation-result-reason').textContent = result.reason;
      document.getElementById('allocation-result-requires').textContent = result.requires;
      output.hidden = false; output.focus();
    });
  }
}
