#!/usr/bin/env python3
"""Generate static, no-JavaScript-readable pages from the canonical research records."""
from pathlib import Path
import argparse, html, json, re
ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/StewAlexander-com/energy-density-challenge'
def read(path): return (ROOT/path).read_text()
def data(path): return json.loads(read(path))
def e(value): return html.escape(str(value), quote=True)
DOCS = [('methodology','METHODOLOGY.md'),('contributing','CONTRIBUTING.md'),('model-methodology','docs/model-methodology.md'),('research-protocol','docs/research-protocol.md'),('safety','SAFETY.md'),('governance','docs/governance.md'),('donate-intelligence','docs/donate-intelligence.md'),('deployment','docs/deployment.md')]
LINKS = {p: 'guide.html#'+slug for slug,p in DOCS} | {'docs/ten-step-review.md':'review.html','README.md':REPO}
def resolve_link(url, origin):
 if re.match(r'^(https?://|#)',url): return url
 resolved = (ROOT/origin).parent.joinpath(url).resolve()
 try: path = resolved.relative_to(ROOT).as_posix()
 except ValueError: raise ValueError(f'Link escapes repository: {url}')
 return LINKS.get(path,path)
def inline(text,origin):
 safe=e(text)
 safe=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:f'<a href="{e(resolve_link(html.unescape(m[2]),origin))}">{m[1]}</a>',safe)
 safe=re.sub(r'`([^`]+)`',r'<code>\1</code>',safe)
 safe=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',safe)
 return safe

def markdown(text,origin,heading_offset=0):
 out=[];para=[];lst=None;code=None
 def flush():
  if para: out.append('<p>'+inline(' '.join(para),origin)+'</p>');para.clear()
 def close_list():
  nonlocal lst
  if lst:out.append(f'</{lst}>');lst=None
 for line in text.splitlines()+['']:
  if line.startswith('```'):
   flush();close_list()
   if code is None:code=[]
   else:out.append('<pre><code>'+e('\n'.join(code))+'</code></pre>');code=None
   continue
  if code is not None:code.append(line);continue
  if not line.strip():flush();close_list();continue
  heading=re.match(r'^(#{1,6}) (.+)',line)
  if heading:
   flush();close_list();level=min(6,len(heading[1])+heading_offset)
   out.append(f'<h{level}>{inline(heading[2],origin)}</h{level}>');continue
  item=re.match(r'^(?:([-*]) |(\d+)\. )(.+)',line)
  if item:
   flush();kind='ul' if item[1] else 'ol'
   if lst!=kind:close_list();lst=kind;out.append(f'<{kind}>')
   out.append('<li>'+inline(item[3],origin)+'</li>');continue
  close_list();para.append(line)
 return '\n'.join(out)

HEADER='''<a class="skip" href="#main">Skip to content</a><header class="site-header wrap"><a class="brand" href="index.html"><span class="mark" aria-hidden="true">E<span>?</span></span><span>ENERGY DENSITY<br>CHALLENGE</span></a><nav aria-label="Main navigation"><a href="review.html">The 10-step review</a><a href="index.html#model">The model</a><a href="guide.html">Research guide</a><a class="nav-action" href="index.html#contribute">Contribute ↗</a></nav></header>'''
def page(title,body):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{e(title)} — The Energy Density Challenge, an open research commons that tests its problem framing first."><title>{e(title)} — Energy Density Challenge</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css"></head><body>{HEADER}<main id="main" class="wrap">{body}</main><footer class="site-footer wrap"><a href="index.html">Energy Density Challenge</a><p>Framing first · No completed project study</p><nav aria-label="Footer"><a href="{REPO}">GitHub</a><a href="AI_CHALLENGE.md">AI entry point</a><a href="challenge.json">Challenge data</a><a href="guide.html#sources">Sources</a></nav></footer></body></html>\n'''
def edge_html(edge,labels):
 return f'<article class="model-edge"><p class="edge-meta">{e(edge["id"])} · UNTESTED HYPOTHESIS</p><h4>{e(labels[edge["source"]])} → {e(labels[edge["target"]])}</h4><p><strong>Condition:</strong> {e(edge["assumption"])}</p><p><strong>Test:</strong> {e(edge["discriminating_test"])}</p></article>'
def render():
 ch=data('challenge.json');model=data('research/models/EDC-M-0001.json');hyp=data('research/hypotheses/EDC-H-0001.json');exp=data('research/experiments/EDC-E-0001.json')
 labels={n['id']:n['label'] for n in model['nodes']}
 positions={'density':(17,14),'efficiency':(50,12),'delivery':(83,14),'cost':(17,48),'service':(50,47),'compute':(83,48),'demand':(28,83),'burdens':(72,83)}
 nodes=''.join(f'<button class="node" type="button" data-node="{n["id"]}" aria-pressed="{str(n["id"]=="density").lower()}" style="left:{positions[n["id"]][0]}%;top:{positions[n["id"]][1]}%">{e(n["label"])}</button>' for n in model['nodes'])
 edges=''
 for edge in model['edges']:
  a,b=positions[edge['source']],positions[edge['target']]
  edges+=f'<path data-source="{edge["source"]}" data-target="{edge["target"]}" class="{"active" if "density" in [edge["source"],edge["target"]] else ""}" d="M {a[0]*6} {a[1]*4.3} L {b[0]*6} {b[1]*4.3}"/>'
 statuses={'unresolved':'UNRESOLVED','plausible_experiment_required':'PLAUSIBLE — EXPERIMENT REQUIRED','falsified':'FALSIFIED','supported_within_tested_conditions':'SUPPORTED WITHIN TESTED CONDITIONS','proposed':'PROPOSED','registered':'REGISTERED','completed':'COMPLETED','withdrawn':'WITHDRAWN'}
 records=''
 for rec,path,description in [(hyp,'research/hypotheses/EDC-H-0001.json','An open framing claim. The service, baseline and decision thresholds must be registered before the comparison.'),(exp,'research/experiments/EDC-E-0001.json','A proposed desk audit. Compare density with feasible alternatives before deciding whether a physical test is warranted.')]:
  records+=f'<article class="record"><span class="record-id">{e(rec["id"])}</span><div><h3>{e(rec["title"])}</h3><p>{description}</p><a href="{path}">Read the full record ↗</a></div><span class="status">{statuses[rec["status"]]}</span></article>'
 vals={'NODES':nodes,'EDGES':edges,'NODE_TITLE':e(model['nodes'][0]['label']),'NODE_QUESTION':e(model['nodes'][0]['question']),'NODE_EDGES':''.join(edge_html(x,labels) for x in model['edges'] if x['source']=='density' or x['target']=='density'),'ALL_EDGES':''.join(edge_html(x,labels) for x in model['edges']),'METRICS':''.join(f'<li><strong>{e(m["label"])}</strong> — {e(m["unit"])}</li>' for m in ch['metrics']),'ROLES':''.join(f'<li><strong>{e(role)}:</strong> {e(task)}</li>' for role,task in data('assets/roles.json')),'RECORDS':records,'DATE':ch['last_updated'],'MODEL_JSON':json.dumps(model,ensure_ascii=False).replace('<','\\u003c')}
 home=read('templates/index.html')
 for key,value in vals.items():home=home.replace('@@'+key+'@@',value)
 if '@@' in home:raise ValueError('Unreplaced template token')
 review=read('docs/ten-step-review.md');parts=re.split(r'^## ',review,flags=re.M)[1:];nav=[];body=[]
 for part in parts:
  title,rest=part.split('\n',1)
  step=re.match(r'(\d{2}) — (.+)',title)
  if step:
   slug='step-'+step[1];nav.append(f'<a href="#{slug}">{e(step[1]+" / "+step[2])}</a>')
   body.append(f'<section id="{slug}" class="review-step"><h2>{e(title)}</h2>{markdown(rest,"docs/ten-step-review.md")}</section>')
  else:body.append(f'<section class="doc-section"><h2>{e(title)}</h2>{markdown(rest,"docs/ten-step-review.md")}</section>')
 review_body='''<div class="article-hero"><p class="eyebrow">The founding brief / cumulative review</p><h1>Ten steps to a better question.</h1><p class="lede">Each pass learns from the last. The result is a research commons that can challenge its own premise.</p><p class="source-note">One AI-assisted review sequence · 2026-09-10 UTC · Not ten independent reviews or an experimental result</p><div class="review-verdict"><p><strong>Launch decision:</strong> proceed with problem-framing research. Energy density remains a candidate, with no validated claim that it is the leading leverage point.</p></div></div>'''+f'<div class="document-layout"><nav class="document-nav" aria-label="Review steps"><span class="small-label">THE TEN PASSES</span>{"".join(nav)}</nav><article class="document-content">{"".join(body)}</article></div>'
 guide_sections=[];guide_nav=[]
 for slug,path in DOCS:
  title,rest=read(path).split('\n',1);title=title.removeprefix('# ')
  guide_nav.append(f'<a href="#{slug}">{e(title)}</a>')
  guide_sections.append(f'<section id="{slug}" class="doc-section"><h2>{e(title)}</h2>{markdown(rest,path,1)}<p class="source-note"><a href="{path}">Read the original Markdown</a></p></section>')
 sources=[]
 for s in data('research/literature/sources.json')['sources']:
  label='BACKGROUND SOURCE · PAGE REVIEWED' if s['verification']=='full_page_reviewed' else 'LITERATURE LEAD · FULL TEXT NOT VERIFIED'
  supports=s['supports'] or 'Direct retrieval returned HTTP 403. Recheck this source before relying on its contents.'
  sources.append(f'<article class="source-entry"><span class="small-label">{label}</span><h3><a href="{e(s["url"])}">{e(s["title"])}</a></h3><p>{e(supports)}</p><p><strong>Limit:</strong> {e(s["does_not_support"])}</p><p class="source-note">{s["id"]} · Access checked {s["accessed"]} UTC</p></article>')
 guide_nav.append('<a href="#sources">Sources & limits</a>')
 guide_sections.append('<section id="sources" class="doc-section"><h2>Sources & limits</h2><p>Background definitions are separate from project evidence. No completed project result is recorded. The ten-step review is conceptual analysis, not a systematic literature review.</p>'+''.join(sources)+'<p><a href="research/literature/sources.json">Machine-readable source ledger</a></p></section>')
 guide_body='<div class="article-hero"><p class="eyebrow">Shared rules / inspectable records</p><h1>A guide to doing useful research.</h1><p class="lede">Define a fair comparison. Make it possible to be wrong. Preserve what you learn.</p></div>'+f'<div class="document-layout"><nav class="document-nav" aria-label="Guide topics"><span class="small-label">IN THIS GUIDE</span>{"".join(guide_nav)}</nav><article class="document-content">{"".join(guide_sections)}</article></div>'
 return {'index.html':home,'review.html':page('Ten cumulative reviews',review_body),'guide.html':page('Research guide',guide_body)}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
 for name,content in render().items():
  if args.check:
   if not (ROOT/name).exists() or read(name)!=content:raise SystemExit(f'{name} is stale. Run python3 scripts/build.py')
  else:(ROOT/name).write_text(content)
 print('Generated pages are current.' if args.check else 'Built index.html, review.html and guide.html.')
if __name__=='__main__':main()
