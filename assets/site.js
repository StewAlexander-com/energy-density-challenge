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
    transport:{title:'Move the same load, over the same route.',density:'Installed storage mass or volume limits payload or range.',alternative:'Route and vehicle efficiency, charging access, and the best feasible existing vehicle.',boundary:'Payload, route, duty cycle, service reliability, lifetime and the complete vehicle energy system.'},
    heat:{title:'Keep the same space at a specified temperature.',density:'The space available for required thermal storage is the limiting factor.',alternative:'Insulation, heat pumps, controls, maintenance and the best feasible existing heating system.',boundary:'Indoor temperature, climate, occupancy, reliability, equipment lifetime and energy supply.'},
    compute:{title:'Complete the same task, at the same quality.',density:'On-device storage mass or volume limits useful operation; this must be established.',alternative:'Better algorithms, efficient hardware, cooling, scheduling and reliable power delivery.',boundary:'Task quality, latency, workload, hardware lifetime, cooling and the complete energy supply.'}
  };
  document.querySelectorAll('[data-scenario]').forEach(button => button.addEventListener('click', () => {
    const scenario = scenarios[button.dataset.scenario];
    document.querySelectorAll('[data-scenario]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    for (const name of ['title','density','alternative','boundary']) document.getElementById('scenario-'+name).textContent = scenario[name];
  }));
  const model = JSON.parse(document.getElementById('model-data').textContent);
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
      const article=textElement('article','','model-edge');
      article.append(textElement('p',edge.id+' · UNTESTED HYPOTHESIS','edge-meta'),textElement('h4',labels[edge.source]+' → '+labels[edge.target]));
      for(const [title,value] of [['Condition: ',edge.assumption],['Test: ',edge.discriminating_test]]) {
        const p=document.createElement('p');p.append(textElement('strong',title),document.createTextNode(value));article.append(p);
      }
      edgeList.append(article);
    }
  }));
  const saving=document.getElementById('saving'), growth=document.getElementById('growth');
  function updateEnergy() {
    const s=Number(saving.value),g=Number(growth.value),result=calculateEnergy(s,g);
    document.getElementById('saving-value').textContent=s+'%';document.getElementById('growth-value').textContent=g+'%';
    saving.setAttribute('aria-valuetext',s+' percent less energy per task');growth.setAttribute('aria-valuetext',g+' percent more tasks');
    const formatter=new Intl.NumberFormat('en',{maximumFractionDigits:1});
    document.getElementById('energy-result').textContent=formatter.format(100*result.ratio)+'%';
    document.getElementById('energy-message').textContent=Math.abs(result.ratio-1)<1e-9?'The saving is exactly offset by task growth.':result.ratio<1?'Operational energy decreases in this illustration.':'Operational energy increases despite the per-task saving.';
    document.getElementById('energy-formula').textContent=(1-s/100).toFixed(2)+' × '+(1+g/100).toFixed(2)+' = '+result.ratio.toFixed(3);
    document.getElementById('break-even').textContent=s===0?'With no per-task saving, any task growth increases operational energy.':'A '+formatter.format(result.breakEvenGrowth)+'% increase in tasks erases a '+s+'% saving per task.';
  }
  saving.addEventListener('input',updateEnergy);growth.addEventListener('input',updateEnergy);updateEnergy();
  const form=document.getElementById('draft-form'), evidence=document.getElementById('evidence-status'), source=document.getElementById('source'), preview=document.getElementById('draft-preview');
  let currentDraft=null;
  function invalidatePreview(){preview.hidden=true;currentDraft=null;}
  form.addEventListener('input',event=>{if(event.target.setCustomValidity)event.target.setCustomValidity('');invalidatePreview();});
  evidence.addEventListener('change',()=>{const linked=evidence.value==='linked';document.getElementById('source-field').hidden=!linked;source.required=linked;source.setCustomValidity('');invalidatePreview();});
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
    const markdown=formatDraft(currentDraft);document.getElementById('draft-text').textContent=markdown;
    const target=new URL(EDC_REPOSITORY+'/issues/new');target.searchParams.set('title','Framing question: '+currentDraft.service);target.searchParams.set('body',markdown);
    const link=document.getElementById('github-draft');
    if(target.href.length>7000){link.href=EDC_REPOSITORY+'/issues/new';link.textContent='Open GitHub; attach downloaded draft ↗';}
    else {link.href=target.href;link.textContent='Review on GitHub ↗';}
    preview.hidden=false;preview.focus();
  });
  document.getElementById('download-draft').addEventListener('click',()=>{
    if(!currentDraft)return;
    const blob=new Blob([JSON.stringify(currentDraft,null,2)+'\n'],{type:'application/json'}),url=URL.createObjectURL(blob),anchor=document.createElement('a');
    anchor.href=url;anchor.download='energy-challenge-framing-draft.json';document.body.append(anchor);anchor.click();anchor.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
}
