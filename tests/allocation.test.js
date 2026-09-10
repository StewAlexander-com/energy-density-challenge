const test = require('node:test');
const assert = require('node:assert/strict');
const {nextResearchStep} = require('../assets/allocation.js');
const ready = {decision:'yes',discriminator:'yes',feasible:'yes',resources:'yes',stalled:'no'};
test('missing or invented answers cannot produce a suggestion', () => {
  for (const invalid of ['', undefined, 'probably']) assert.throws(() => nextResearchStep({...ready,resources:invalid}));
});
test('a decision must be defined before optimizing another action', () => {
  assert.match(nextResearchStep({...ready,decision:'no'}).title,/Define the decision/);
});
test('unknown discrimination does not become permission to test', () => {
  assert.match(nextResearchStep({...ready,discriminator:'unknown'}).title,/Find an observation/);
});
test('stalled and indistinguishable branches can be retained without consensus', () => {
  const result=nextResearchStep({...ready,discriminator:'no',stalled:'yes'});
  assert.match(result.title,/Pause and reframe/); assert.match(result.requires,/preserve disagreement/);
});
test('unknown feasibility blocks proceeding even when costs look acceptable', () => {
  assert.match(nextResearchStep({...ready,feasible:'unknown'}).title,/feasibility and authority/);
});
test('unknown cost is not zero and a breached cap stops the suggestion', () => {
  assert.match(nextResearchStep({...ready,resources:'unknown'}).title,/Estimate the costs/);
  assert.match(nextResearchStep({...ready,resources:'no'}).title,/Stop at the resource limit/);
});
test('a stalled discussion with a discriminator points to a plan for review', () => {
  const result=nextResearchStep({...ready,stalled:'yes'});
  assert.match(result.title,/Prepare the discriminating observation/);
  assert.match(result.requires,/Only the responsible person/);
});
test('no combination of answers authorizes execution or creates a scientific result', () => {
  const values=['yes','no','unknown'];
  for (const decision of values) for (const discriminator of values) for (const feasible of values) for (const resources of values) for (const stalled of values) {
    const result=nextResearchStep({decision,discriminator,feasible,resources,stalled});
    assert.equal(result.execution_authorized,false); assert.equal(result.status,'planning_only');
  }
});
