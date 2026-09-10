/* Progressive enhancement only. No requests, automatic submission, agents or device access. */
'use strict';
const EDC_REPOSITORY = 'https://github.com/StewAlexander-com/energy-density-challenge';
function calculateEnergy(savingPercent, growthPercent) {
  if (!Number.isFinite(savingPercent) || !Number.isFinite(growthPercent) || savingPercent < 0 || savingPercent > 90 || growthPercent < 0 || growthPercent > 200) throw new RangeError('Use a saving from 0–90% and growth from 0–200%.');
  const ratio = (1 - savingPercent / 100) * (1 + growthPercent / 100);
  return { ratio, breakEvenGrowth: 100 * (1 / (1 - savingPercent / 100) - 1) };
}
function makeDraft(values, now = new Date()) {
  const draft = {schema_version:'1.0.0',kind:'framing_draft',status:'unreviewed'};
  for (const key of ['service','context','constraint','baseline','alternative','falsifier']) {
    if (typeof values[key] !== 'string' || !values[key].trim()) throw new Error('Complete the question fields, including the observation that would change your mind.');
    draft[key] = values[key].trim();
  }
  if (!['linked','not_yet_available'].includes(values.evidence_status)) throw new Error('Declare whether evidence is available.');
  draft.evidence_status = values.evidence_status;
  draft.source = '';
  if (draft.evidence_status === 'linked') {
    let url; try {url = new URL(String(values.source).trim());} catch {throw new Error('Provide an http or https source URL.');}
    if (!['https:','http:'].includes(url.protocol) || url.username || url.password) throw new Error('Provide an http or https source URL without credentials.');
    draft.source = url.href;
  }
  if (values.safety_acknowledged !== true) throw new Error('Acknowledge the review and safety boundary.');
  draft.safety_acknowledged = true;
  draft.created_at = now.toISOString();
  return draft;
}
function formatDraft(draft) {
  return `# Framing question: ${draft.service}\n\nStatus: unreviewed draft. No scientific validation or permanent ID.\n\nService: ${draft.service}\n\nPeople, place and time: ${draft.context}\n\nSuspected constraint: ${draft.constraint}\n\nCurrent baseline: ${draft.baseline}\n\nFeasible alternative: ${draft.alternative}\n\nEvidence: ${draft.evidence_status === 'linked' ? draft.source + ' (not verified by this form)' : 'Not yet available; this is a question, not a finding.'}\n\nWhat would change my mind: ${draft.falsifier}\n\nSafety: Question for review only. No authorization for hazardous physical work.\n\nNext review: define functional unit, quality, boundary, lifetime, thresholds, uncertainty and displaced burdens before registering a study.\n\nCreated: ${draft.created_at}`;
}
// Export the accounting and draft guards for regression checks without a browser dependency.
if (typeof module !== 'undefined' && module.exports) module.exports = {calculateEnergy,makeDraft,formatDraft};
if (typeof document !== 'undefined') {
  const scenarios = {
    transport:{title:'Move the same load over the same route.',density:'The weight or size of the complete storage system limits the load or range.',alternative:'A more efficient vehicle, a better route or better charging access.',boundary:'The load, route, reliability and lifetime. Include the full vehicle and energy system.'},
    heat:{title:'Keep the same space at the same temperature.',density:'There is too little space for the heat storage that is needed.',alternative:'Better insulation, a heat pump or better heating controls.',boundary:'Indoor temperature, weather, occupancy and reliability. Include the equipment’s lifetime and energy supply.'},
    compute:{title:'Complete the same task to the same standard.',density:'Battery weight or size limits the device’s operation. This would need to be established.',alternative:'More efficient software or hardware, better cooling or reliable power.',boundary:'Accuracy, speed, workload and hardware lifetime. Include cooling and the energy supply.'}
  };
  document.querySelectorAll('[data-scenario]').forEach(button => button.addEventListener('click', () => {
    const scenario = scenarios[button.dataset.scenario];
    document.querySelectorAll('[data-scenario]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    for (const name of ['title','density','alternative','boundary']) document.getElementById('scenario-'+name).textContent = scenario[name];
  }));
  const modelData = document.getElementById('model-data');
  if (modelData) {
  const model = JSON.parse(modelData.textContent);
  const labels = Object.fromEntries(model.nodes.map(n => [n.id,n.label]));
  function textElement(tag,text,className) {const element=document.createElement(tag);element.textContent=text;if(className)element.className=className;return element;}
  document.querySelectorAll('[data-node]').forEach(button => button.addEventListener('click', () => {
    const selected = model.nodes.find(n => n.id === button.dataset.node);
    document.querySelectorAll('[data-node]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    document.querySelectorAll('.network-lines path').forEach(path => path.classList.toggle('active',path.dataset.source===selected.id || path.dataset.target===selected.id));
    document.getElementById('node-title').textContent = selected.label;
    document.getElementById('node-question').textContent = selected.question;
    const edgeList=document.getElementById('node-edges');edgeList.replaceChildren();
    for(const edge of model.edges.filter(item => item.source===selected.id || item.target===selected.id)) {
      const article=textElement('details','','model-edge');
      article.open = edgeList.childElementCount === 0;
      article.append(textElement('summary',labels[edge.source]+' → '+labels[edge.target]));
      for(const [title,value] of [['Assumption: ',edge.assumption],['How to test it: ',edge.discriminating_test]]) {
        const p=document.createElement('p');p.append(textElement('strong',title),document.createTextNode(value));article.append(p);
      }
      article.append(textElement('p',edge.id+' · Untested connection','edge-meta'));
      edgeList.append(article);
    }
  }));
  }
  const saving=document.getElementById('saving'), growth=document.getElementById('growth');
  if (saving && growth) {
  function updateEnergy() {
    const s=Number(saving.value),g=Number(growth.value),result=calculateEnergy(s,g);
    document.getElementById('saving-value').textContent=s+'%';document.getElementById('growth-value').textContent=g+'%';
    saving.setAttribute('aria-valuetext',s+' percent less energy per task');growth.setAttribute('aria-valuetext',g+' percent more tasks');
    const formatter=new Intl.NumberFormat('en',{maximumFractionDigits:1});
    document.getElementById('energy-result').textContent=formatter.format(100*result.ratio)+'%';
    document.getElementById('energy-message').textContent=Math.abs(result.ratio-1)<1e-9?(s===0?'Operational energy is unchanged in this illustration.':'The saving is exactly offset by task growth.'):result.ratio<1?'Operational energy decreases in this illustration.':s===0?'Operational energy increases with task growth.':'Operational energy increases despite the per-task saving.';
    document.getElementById('energy-formula').textContent=(1-s/100).toFixed(2)+' × '+(1+g/100).toFixed(2)+' = '+result.ratio.toFixed(3);
    document.getElementById('break-even').textContent=s===0?'With no per-task saving, any task growth increases operational energy.':'A '+formatter.format(result.breakEvenGrowth)+'% increase in tasks erases a '+s+'% saving per task.';
  }
  saving.addEventListener('input',updateEnergy);growth.addEventListener('input',updateEnergy);updateEnergy();
  }
  const form=document.getElementById('draft-form'), evidence=document.getElementById('evidence-status'), source=document.getElementById('source'), preview=document.getElementById('draft-preview');
  if (form) {
  let currentDraft=null;
  function invalidatePreview(){preview.hidden=true;currentDraft=null;}
  form.addEventListener('input',event=>{if(event.target.setCustomValidity)event.target.setCustomValidity('');invalidatePreview();});
  evidence.addEventListener('change',()=>{const linked=evidence.value==='linked';document.getElementById('source-field').hidden=!linked;source.required=linked;source.disabled=!linked;source.setCustomValidity('');invalidatePreview();});
  form.addEventListener('submit',event=>{
    event.preventDefault();
    for(const input of form.querySelectorAll('input[required]:not([type=checkbox]), textarea[required]')) {
      input.setCustomValidity(input.value.trim()?'':'Please enter a value; spaces alone do not define a question.');
    }
    if(evidence.value==='linked') {
      let valid=false;try{const u=new URL(source.value);valid=['http:','https:'].includes(u.protocol)&&!u.username&&!u.password;}catch{}
      source.setCustomValidity(valid?'':'Use an http or https URL without credentials.');
    }
    if(!form.reportValidity())return;
    const values=Object.fromEntries(new FormData(form));values.safety_acknowledged=form.elements.safety_acknowledged.checked;
    currentDraft=makeDraft(values);
    const markdown=formatDraft(currentDraft);
    const summary=document.getElementById('draft-text');summary.replaceChildren();
    for (const [label,value] of [['What should improve',currentDraft.service],['For whom, where, and when',currentDraft.context],['Possible limit',currentDraft.constraint],['What happens today',currentDraft.baseline],['An alternative',currentDraft.alternative],['Evidence',currentDraft.evidence_status==='linked'?currentDraft.source:'Not yet available'],['What would change my mind',currentDraft.falsifier]]) {
      const term=document.createElement('dt'),detail=document.createElement('dd');term.textContent=label;detail.textContent=value;summary.append(term,detail);
    }
    const target=new URL(EDC_REPOSITORY+'/issues/new');target.searchParams.set('title','Framing question: '+currentDraft.service);target.searchParams.set('body',markdown);
    const link=document.getElementById('github-draft');
    if(target.href.length>7000){link.href=EDC_REPOSITORY+'/issues/new';link.textContent='Open GitHub; attach downloaded draft ↗';}
    else {link.href=target.href;link.textContent='Review on GitHub ↗';}
    preview.hidden=false;preview.focus();
  });
  function downloadDraft(format) {
    if (!currentDraft) return;
    const json=format==='json';
    const content=json?JSON.stringify(currentDraft,null,2)+'\n':formatDraft(currentDraft)+'\n';
    const blob=new Blob([content],{type:json?'application/json':'text/plain;charset=utf-8'});
    const url=URL.createObjectURL(blob),anchor=document.createElement('a');
    anchor.href=url;anchor.download='energy-challenge-framing-draft.'+(json?'json':'txt');
    document.body.append(anchor);anchor.click();anchor.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  document.getElementById('download-draft').addEventListener('click',()=>downloadDraft('text'));
  document.getElementById('download-json').addEventListener('click',()=>downloadDraft('json'));
  }
}
