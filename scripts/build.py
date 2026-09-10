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

HEADER = """<a class="skip" href="#main">Skip to content</a><header class="site-header wrap"><a class="brand" href="index.html" aria-label="Energy Density Challenge home">Energy Density Challenge</a><nav aria-label="Main navigation"><a href="index.html">Question</a><a href="explore.html">Explore</a><a href="guide.html">Research guide</a><a href="contribute.html">Contribute</a></nav></header>"""
def page(title,body,current=''):
 header=HEADER.replace(f'href="{current}"',f'href="{current}" aria-current="page"') if current else HEADER
 return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{e(title)} — The Energy Density Challenge. Investigate the problem before choosing a solution."><title>{e(title)} — Energy Density Challenge</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css"><script src="assets/site.js" defer></script></head><body>{header}<main id="main" class="wrap">{body}</main><footer class="site-footer wrap"><p>Energy Density Challenge · Open research</p><nav aria-label="Footer"><a href="review.html">Framing review</a><a href="guide.html#sources">Sources</a><a href="guide.html#safety">Safety</a><a href="{REPO}">GitHub</a><a href="AI_CHALLENGE.md">AI instructions (Markdown)</a></nav></footer></body></html>\n'''
def edge_html(edge,labels,opened=False):
 return f'<details class="model-edge"{" open" if opened else ""}><summary>{e(labels[edge["source"]])} → {e(labels[edge["target"]])}</summary><p><strong>Assumption:</strong> {e(edge["assumption"])}</p><p><strong>How to test it:</strong> {e(edge["discriminating_test"])}</p><p class="edge-meta">{e(edge["id"])} · Untested connection</p></details>'
def render():
 ch=data('challenge.json');model=data('research/models/EDC-M-0001.json');hyp=data('research/hypotheses/EDC-H-0001.json');exp=data('research/experiments/EDC-E-0001.json')
 labels={n['id']:n['label'] for n in model['nodes']}
 positions={'density':(17,14),'efficiency':(50,12),'delivery':(83,14),'cost':(17,48),'service':(50,47),'compute':(83,48),'demand':(28,83),'burdens':(72,83)}
 nodes=''.join(f'<button class="node" type="button" data-node="{n["id"]}" aria-pressed="{str(n["id"]=="density").lower()}" style="left:{positions[n["id"]][0]}%;top:{positions[n["id"]][1]}%">{e(n["label"])}</button>' for n in model['nodes'])
 edges=''
 for edge in model['edges']:
  a,b=positions[edge['source']],positions[edge['target']]
  # Route these connections through the gap between labels, never through a third factor.
  routes={
   'EDC-L-0003':'M 102 60.2 Q 185 140 250 145 L 405 145 L 405 275 L 432 356.9',
   'EDC-L-0005':'M 300 51.6 L 405 145 L 405 275 L 432 356.9',
   'EDC-L-0007':'M 498 60.2 L 405 145 L 405 275 L 432 356.9',
   'EDC-L-0010':'M 102 206.4 L 200 275 L 405 275 L 498 206.4',
  }
  route=routes.get(edge['id'],f'M {a[0]*6} {a[1]*4.3} L {b[0]*6} {b[1]*4.3}')
  edges+=f'<path data-source="{edge["source"]}" data-target="{edge["target"]}" class="{"active" if "density" in [edge["source"],edge["target"]] else ""}" d="{route}"/>'
 statuses={'unresolved':'UNRESOLVED','plausible_experiment_required':'PLAUSIBLE — EXPERIMENT REQUIRED','falsified':'FALSIFIED','supported_within_tested_conditions':'SUPPORTED WITHIN TESTED CONDITIONS','proposed':'PROPOSED','registered':'REGISTERED','completed':'COMPLETED','withdrawn':'WITHDRAWN'}
 records=''
 for rec,path,description in [(hyp,'research/hypotheses/EDC-H-0001.json','An open framing claim. The service, baseline and decision thresholds must be registered before the comparison.'),(exp,'research/experiments/EDC-E-0001.json','A proposed desk audit. Compare density with feasible alternatives before deciding whether a physical test is warranted.')]:
  records+=f'<article class="record"><span class="record-id">{e(rec["id"])}</span><div><h3>{e(rec["title"])}</h3><p>{description}</p><a href="{path}">Research record (JSON)</a></div><span class="status">{statuses[rec["status"]]}</span></article>'
 vals={'NODES':nodes,'EDGES':edges,'NODE_TITLE':e(model['nodes'][0]['label']),'NODE_QUESTION':e(model['nodes'][0]['question']),'NODE_EDGES':''.join(edge_html(x,labels,i==0) for i,x in enumerate([x for x in model['edges'] if x['source']=='density' or x['target']=='density'])),'ALL_EDGES':''.join(edge_html(x,labels) for x in model['edges']),'METRICS':''.join(f'<li><strong>{e(m["label"])}</strong> — {e(m["unit"])}</li>' for m in ch['metrics']),'ROLES':''.join(f'<li><strong>{e(role)}:</strong> {e(task)}</li>' for role,task in data('assets/roles.json')),'RECORDS':records,'DATE':ch['last_updated'],'MODEL_JSON':json.dumps(model,ensure_ascii=False).replace('<','\\u003c')}
 product={}
 for name,title in [('index','Is energy density the right problem?'),('explore','Explore the assumptions'),('contribute','Contribute a question')]:
  content=read('templates/'+name+'.html')
  for key,value in vals.items():content=content.replace('@@'+key+'@@',value)
  if '@@' in content:raise ValueError('Unreplaced template token')
  product[name+'.html']=page(title,content,name+'.html')
 review=read('docs/ten-step-review.md');parts=re.split(r'^## ',review,flags=re.M)[1:];nav=[];body=[]
 for part in parts:
  title,rest=part.split('\n',1)
  step=re.match(r'(\d{2}) — (.+)',title)
  if step:
   slug='step-'+step[1];nav.append(f'<a href="#{slug}">{e(step[1]+" / "+step[2])}</a>')
   body.append(f'<section id="{slug}" class="review-step"><h2>{e(title)}</h2>{markdown(rest,"docs/ten-step-review.md")}</section>')
  else:body.append(f'<section class="doc-section"><h2>{e(title)}</h2>{markdown(rest,"docs/ten-step-review.md")}</section>')
 review_body='''<div class="article-hero"><p class="eyebrow">Review of the founding brief</p><h1>Ten steps to a better question.</h1><p class="lede">Each pass builds on the last to make the research question clearer and more testable.</p><p class="source-note">One AI-assisted review, revised in ten steps · September 10, 2026</p><div class="review-verdict"><p><strong>Launch decision:</strong> proceed with problem-framing research. Energy density remains a candidate, with no validated claim that it is the leading leverage point.</p></div></div>'''+f'<div class="document-layout"><nav class="document-nav" aria-label="Review steps"><span class="small-label">THE TEN PASSES</span>{"".join(nav)}</nav><article class="document-content">{"".join(body)}</article></div>'
 guide_sections=[];guide_nav=['<a href="#first-study">The first study</a>']
 guide_sections.append('<section id="first-study" class="doc-section"><h2>The first study</h2><p><strong>Status: proposed.</strong> No use case or success threshold has been selected yet.</p><ol><li>Choose one useful outcome with someone who understands the setting.</li><li>Record what happens today, the alternatives, the full system boundary, and the criteria for success before comparing results.</li><li>Gather traceable evidence. Report missing information and uncertainty.</li><li>Compare better storage with efficiency, infrastructure and other practical options.</li><li>Ask a separate reviewer to check the analysis. Decide whether to keep, narrow or replace the question, or leave it unresolved.</li></ol><p>This starts as desk research. It does not authorize a physical experiment.</p><details class="wide-detail"><summary>Research records and data</summary><p><a href="research/hypotheses/EDC-H-0001.json">Framing hypothesis (JSON)</a> · <a href="research/experiments/EDC-E-0001.json">Study protocol (JSON)</a> · <a href="research/index.json">Research index (JSON)</a></p><p>No completed study, independent replication or falsified hypothesis has been recorded.</p></details></section>')
 for slug,path in DOCS:
  title,rest=read(path).split('\n',1);title=title.removeprefix('# ')
  guide_labels={'methodology':'Comparison method','contributing':'Contributions','model-methodology':'Proposed model','research-protocol':'Research process','safety':'Safety','governance':'Review and records','donate-intelligence':'Future contributions','deployment':'Publishing'}
  guide_nav.append(f'<a href="#{slug}">{e(guide_labels[slug])}</a>')
  guide_sections.append(f'<section id="{slug}" class="doc-section"><h2>{e(title)}</h2>{markdown(rest,path,1)}<p class="source-note"><a href="{path}">Source document (Markdown)</a></p></section>')
 sources=[]
 for s in data('research/literature/sources.json')['sources']:
  label='Background source · Page reviewed' if s['verification']=='full_page_reviewed' else 'Literature lead · Full text not verified'
  supports=s['supports'] or 'Direct retrieval returned HTTP 403. Recheck this source before relying on its contents.'
  sources.append(f'<article class="source-entry"><span class="small-label">{label}</span><h3><a href="{e(s["url"])}">{e(s["title"])}</a></h3><p>{e(supports)}</p><p><strong>Limit:</strong> {e(s["does_not_support"])}</p><p class="source-note">{s["id"]} · Access checked {s["accessed"]} UTC</p></article>')
 guide_nav.append('<a href="#sources">Sources and limits</a>')
 guide_sections.append('<section id="sources" class="doc-section"><h2>Sources and limits</h2><p>Background definitions are separate from project evidence. No completed project result is recorded. The ten-step review is conceptual analysis, not a systematic literature review.</p>'+''.join(sources)+'<p><a href="research/literature/sources.json">Machine-readable source ledger</a></p></section>')
 guide_body='<div class="article-hero"><p class="eyebrow">Research guide</p><h1>How to investigate the question.</h1><p class="lede">Start with the first study or choose a topic below. Detailed protocols and source records are here when you need them.</p></div>'+f'<div class="document-layout"><nav class="document-nav" aria-label="Guide topics"><span class="small-label">IN THIS GUIDE</span>{"".join(guide_nav)}</nav><article class="document-content">{"".join(guide_sections)}</article></div>'
 ux_parts=re.split(r'^## ',read('docs/ux-review.md'),flags=re.M)[1:]
 ux_sections=[]
 for part in ux_parts:
  title,rest=part.split('\n',1)
  ux_sections.append(f'<section class="review-step"><h2>{e(title)}</h2>{markdown(rest,"docs/ux-review.md")}</section>')
 ux_body='<div class="article-hero"><p class="eyebrow">Readability and interface review</p><h1>Twenty passes to a clearer site.</h1><p class="lede">A cumulative rubber-duck review of the question, navigation, wording, spacing and controls.</p><p class="source-note">September 10, 2026 · <a href="docs/ux-review.md">Review source (Markdown)</a></p></div><article class="document-content">'+''.join(ux_sections)+'</article>'
 return {**product,'review.html':page('Ten cumulative reviews',review_body),'guide.html':page('Research guide',guide_body,'guide.html'),'ux-review.html':page('Twenty-step UX review',ux_body)}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
 for name,content in render().items():
  if args.check:
   if not (ROOT/name).exists() or read(name)!=content:raise SystemExit(f'{name} is stale. Run python3 scripts/build.py')
  else:(ROOT/name).write_text(content)
 print('Generated pages are current.' if args.check else 'Built all public HTML pages.')
if __name__=='__main__':main()
