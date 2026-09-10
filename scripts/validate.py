#!/usr/bin/env python3
"""Structural and semantic guardrails. Passing does not certify scientific truth."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, sys
from jsonschema import Draft202012Validator, FormatChecker
ROOT=Path(__file__).resolve().parents[1]
def require(condition,message):
 if not condition: raise ValueError(message)
def load(path):return json.loads(path.read_text())
def validate_schema(record,schema):
 Draft202012Validator.check_schema(schema)
 Draft202012Validator(schema,format_checker=FormatChecker()).validate(record)
def validate_hypothesis(record,results,sources):
 status=record['status'];history=record['confidence_history']
 require(bool(history),'Confidence history is required.')
 require(history[-1]['status']==status,'Latest confidence history must match hypothesis status.')
 require([x['date'] for x in history]==sorted(x['date'] for x in history),'Confidence history must be chronological.')
 if record['confidence']['value'] is not None:
  require(bool(record['confidence'].get('calibration')),'Numerical confidence needs documented calibration.')
 for ref in record['evidence']:
  require(ref in sources or ref in results,f'Unresolved evidence reference: {ref}')
  if ref in sources:require(sources[ref]['verification']=='full_page_reviewed','Unverified literature leads cannot count as evidence.')
 for rid in record['result_ids']:require(rid in results,f'Missing result: {rid}')
 if status!='unresolved':
  require(all(v is not None for k,v in record['scope'].items() if k!='missing_reason'),'A status beyond unresolved requires a bounded scope.')
  require(bool(record['baseline']) and bool(record['prediction']) and bool(record['thresholds']),'Baseline, prediction and thresholds are required before promotion.')
  require(bool(record['evidence']),'Scientific status promotion needs evidence.')
 if status=='falsified':require(bool(record['result_ids']),'Falsification requires a result record explaining the contradiction.')
 if status=='supported_within_tested_conditions':
  replications=record['replications']
  require(len({r['group'] for r in replications})>=2,'Support requires two documented independent replication groups.')
  require(len({r['result_id'] for r in replications})>=2,'Replications must refer to distinct result records.')
  for rep in replications:
   require(rep['result_id'] in record['result_ids'],'Replication result must be listed on the hypothesis.')
   result=results.get(rep['result_id'])
   require(bool(result) and result['evidence_kind']=='experimental_result','A simulation or desk analysis is not physical replication.')
   require(result['replication_group']==rep['group'],'Replication group disagrees with result record.')

def validate_experiment(record):
 if record['status'] in ['registered','completed']:
  require(all(v is not None for k,v in record['preregistration'].items() if k!='missing_reason'),'Registered experiments require complete preregistration.')
  require(bool(record['predicted_measurable_result']),'Registered experiments require a measurable prediction.')

def validate_model(model):
 ids=[n['id'] for n in model['nodes']]
 require(len(set(ids))==len(ids),'Duplicate model node.')
 edge_ids=[x['id'] for x in model['edges']]
 require(len(set(edge_ids))==len(edge_ids),'Duplicate model edge ID.')
 for edge in model['edges']:
  require(edge['source'] in ids and edge['target'] in ids,'Model edge references a missing node.')
  require(edge['strength'] is None,'Uncalibrated model cannot report measured weights.')

def validate_index(index,records):
 for category in ['hypotheses','experiments','results','models']:
  entries=index[category]
  require(len({r['id'] for r in entries})==len(entries),f'Duplicate {category} index entry.')
  expected={r['id'] for r in records[category]}
  require({r['id'] for r in entries}==expected,f'{category} index omits or invents a record.')
  by_id={r['id']:r for r in records[category]}
  for entry in entries:
   rec=by_id[entry['id']]
   require(entry['path']==f'research/{category}/{entry["id"]}.json','Canonical path must match the permanent ID.')
   if 'status' in rec:require(entry.get('status')==rec['status'],'Index status differs from canonical record.')
 for status in ['falsified','unresolved']:
  expected={r['id'] for r in records['hypotheses'] if r['status']==status}
  require(set(index[status])==expected,f'{status} index disagrees with canonical records.')

class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.references=[];self.controls=[];self.labels=set();self.lang=None;self.main=False;self.headings=[];self.in_heading=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   require(a['id'] not in self.ids,'Duplicate HTML id: '+a['id']);self.ids.add(a['id'])
  if tag in ['h1','h2','h3','h4','h5','h6']:self.headings.append(int(tag[1]));self.in_heading=True
  if tag=='br' and self.in_heading:raise ValueError('Use natural heading wrapping; hidden line breaks can join words.')
  if tag=='html':self.lang=a.get('lang')
  if tag=='main':self.main=True
  if tag=='label' and 'for' in a:self.labels.add(a['for'])
  if tag in ['input','select','textarea'] and a.get('type')!='checkbox':self.controls.append(a.get('id'))
  for key in ['href','src']:
   if key in a:self.references.append(a[key])
 def handle_endtag(self,tag):
  if tag in ['h1','h2','h3','h4','h5','h6']:self.in_heading=False
def validate_links(root):
 pages={}
 for path in root.glob('*.html'):
  page=Page();page.feed(path.read_text());pages[path]=page
  require(page.lang=='en' and page.main,f'{path.name} needs language and main landmark.')
  require(page.headings.count(1)==1,f'{path.name} needs exactly one main heading.')
  require(all(b<=a+1 for a,b in zip(page.headings,page.headings[1:])),f'{path.name} skips a heading level.')
  require(all(c in page.labels for c in page.controls),f'{path.name} has an unlabelled input.')
 for path,page in pages.items():
  for ref in page.references:
   parsed=urlsplit(ref)
   if parsed.scheme or parsed.netloc:continue
   require(not parsed.path.startswith('/'),'Root-absolute links break repository-subpath hosting.')
   target=(path.parent/unquote(parsed.path)).resolve() if parsed.path else path
   require(target==root or root in target.parents,'Link escapes published root.')
   require(target.exists(),f'Broken local link in {path.name}: {ref}')
   if parsed.fragment and target in pages:require(unquote(parsed.fragment) in pages[target].ids,f'Broken anchor: {ref}')
 return len(pages)
def main():
 for path in ROOT.glob('schemas/*.json'):Draft202012Validator.check_schema(load(path))
 count=0
 for path in [ROOT/'challenge.json',*ROOT.glob('research/**/*.json')]:
  record=load(path)
  if '$schema' in record:
   schema=(path.parent/record['$schema']).resolve();require(ROOT in schema.parents,'External schema not allowed.');validate_schema(record,load(schema));count+=1
 records={category:[load(p) for p in ROOT.glob(f'research/{category}/EDC-*.json')] for category in ['hypotheses','experiments','results','models']}
 sources={s['id']:s for s in load(ROOT/'research/literature/sources.json')['sources']}
 results={r['id']:r for r in records['results']};hypotheses={r['id']:r for r in records['hypotheses']};experiments={r['id']:r for r in records['experiments']}
 for r in records['hypotheses']:
  validate_hypothesis(r,results,sources)
  for eid in r['experiment_ids']:require(eid in experiments and experiments[eid]['hypothesis_id']==r['id'],'Hypothesis experiment reference mismatch.')
  for rid in r['result_ids']:require(results[rid]['experiment_id'] in r['experiment_ids'],'Hypothesis result belongs to an unrelated experiment.')
 for r in records['experiments']:
  validate_experiment(r);require(r['hypothesis_id'] in hypotheses,'Experiment has an unknown hypothesis.')
 for r in records['results']:require(r['experiment_id'] in experiments,'Result has an unknown experiment.')
 for r in records['models']:
  validate_model(r)
  for edge in r['edges']:
   for sid in edge['context_sources']:require(sid in sources and sources[sid]['verification']=='full_page_reviewed','Model context needs a verified source.')
 index=load(ROOT/'research/index.json');validate_index(index,records)
 for state in ['falsified','unresolved']:require(set(load(ROOT/f'research/{state}/index.json')['hypothesis_ids'])==set(index[state]),'Status directory index drift.')
 challenge=load(ROOT/'challenge.json')
 require(set(challenge['experiments_needed']).issubset(experiments),'Challenge references an unknown experiment.')
 require(challenge['confidence']['value'] is None or challenge['confidence'].get('calibration'),'Challenge numerical confidence needs calibration.')
 for metric in challenge['metrics']:
  if metric['value'] is None:require(bool(metric['missing_reason']),'Unknown metric requires a reason.')
 require(len({m['id'] for m in challenge['metrics']})==len(challenge['metrics']),'Duplicate metric ID.')
 try:
  from .research_states import validate as validate_states
  from .validate_process import validate as validate_process
 except ImportError:
  from research_states import validate as validate_states
  from validate_process import validate as validate_process
 validate_states(ROOT);validate_process(ROOT)
 pages=validate_links(ROOT)
 print(f'Validated {count} structured records, all schemas and cross-references, and {pages} HTML pages. No scientific validation is implied.')
if __name__=='__main__':
 try:main()
 except (ValueError,Exception) as exc:print(f'VALIDATION FAILED: {exc}',file=sys.stderr);sys.exit(1)
