"""Keep process proposals, causal claims and historical integrity distinct."""
import json
from pathlib import Path

def dependency_order(graph):
    ids = [node['id'] for node in graph['nodes']]
    if len(ids) != len(set(ids)): raise ValueError('Duplicate process graph node')
    links = {key: [] for key in ids}
    seen = set()
    for edge in graph['edges']:
        pair = (edge['from'], edge['to'])
        if pair in seen or edge['relation'] != 'depends_on': raise ValueError('Duplicate or invalid process dependency')
        seen.add(pair)
        if any(key not in links for key in pair): raise ValueError('Unknown process graph reference')
        links[pair[0]].append(pair[1])
    active = set(); done = set(); order = []
    def visit(node):
        if node in active: raise ValueError('Cycle in process dependency graph')
        if node in done: return
        active.add(node)
        for parent in links[node]: visit(parent)
        active.remove(node); done.add(node); order.append(node)
    for node in ids: visit(node)
    return order

def validate(root):
    def read(path): return json.loads((root/path).read_text())
    protocol = read('research/protocols/EDC-P-0001.json')
    evaluation = read('research/evaluations/EDC-V-0001.json')
    decision = read('research/decisions/EDC-D-0001.json')
    records = [protocol, evaluation, decision]
    if any(r['status'] != 'proposed' or r['result_ids'] or r['research_program'] != 'process_evaluation' for r in records):
        raise ValueError('Process proposals cannot imply evaluated results')
    if protocol['evaluation_id'] != evaluation['id'] or evaluation['protocol_id'] != protocol['id'] or decision['protocol_id'] != protocol['id'] or decision['evaluation_id'] != evaluation['id']:
        raise ValueError('Process record reference mismatch')
    if protocol['claim_status'] != 'unresolved': raise ValueError('Process claim must remain unresolved')
    if any(v is not None for v in evaluation['preregistration'].values()):
        raise ValueError('State 0002 preregistration fields must not be silently filled')
    for estimate in decision['resource_estimates'].values():
        if estimate.get('value') is not None or not estimate.get('unit') or not estimate.get('reason'):
            raise ValueError('Unmeasured resources must remain null with units and a reason')
    if decision['expected_decision_value'] is not None or decision['retrospective_assessment'] is not None:
        raise ValueError('An unperformed allocation cannot have measured value or a retrospective result')
    graph = read('research/process/graph.json'); dependency_order(graph)
    for node in graph['nodes']:
        if node['type'] in {'RESULT','EVIDENCE','REPLICATION'}: raise ValueError('Process graph cannot invent result evidence')
        if node['record'] and node['record'] not in {'research/evaluations/EDC-V-0001.json','research/decisions/EDC-D-0001.json'}:
            raise ValueError('Unexpected process graph record')
    index = read('research/process/index.json')
    for category, expected in [('protocols','research/protocols/EDC-P-0001.json'),('evaluations','research/evaluations/EDC-V-0001.json'),('decisions','research/decisions/EDC-D-0001.json')]:
        if index[category] != [expected]: raise ValueError('Process index mismatch')
    if index['results']: raise ValueError('Process index cannot invent results')
    sources = read('research/process/sources.json')['sources']
    if len({s['id'] for s in sources}) != len(sources): raise ValueError('Duplicate process source')
    for source in sources:
        if source['verification'] not in {'abstract_reviewed','page_reviewed'} or not source['does_not_support']:
            raise ValueError('Process sources need explicit review scope and limits')
    return len(records)
