import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from scripts import research_states as states
from scripts.validate_process import dependency_order

ROOT = Path(__file__).resolve().parents[1]

class StateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(ROOT/'research/states', self.root/'research/states')
        paths = set(states.PRESERVED)
        state2 = json.loads((ROOT/'research/states/ASTRA-STATE-0002/manifest.json').read_text())
        paths.update(f['path'] for f in state2['files'])
        for p in paths:
            target = self.root/p; target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(ROOT/p,target)

    def test_real_archives_and_ancestry_validate(self):
        self.assertEqual(states.validate(self.root),2)

    def test_sealing_cannot_replace_an_existing_state(self):
        with patch.object(states,'ROOT',self.root):
            with self.assertRaisesRegex(ValueError,'Refusing to replace'):
                states.seal('ASTRA-STATE-0001')

    def test_archive_tampering_is_detected(self):
        path = self.root/'research/states/ASTRA-STATE-0001/source.tar'
        path.write_bytes(path.read_bytes()+b'changed')
        with self.assertRaisesRegex(ValueError,'archive digest'): states.validate(self.root)

    def test_original_scientific_record_cannot_silently_change(self):
        path = self.root/'research/hypotheses/EDC-H-0001.json'; path.write_text('{}')
        with self.assertRaisesRegex(ValueError,'scientific content changed'): states.validate(self.root)

    def test_child_research_record_must_match_its_snapshot(self):
        path = self.root/'research/protocols/EDC-P-0001.json'; path.write_text('{}')
        with self.assertRaisesRegex(ValueError,'State 0002 artifact changed'): states.validate(self.root)

    def test_rehashed_child_cannot_claim_a_different_parent(self):
        path = self.root/'research/states/ASTRA-STATE-0002/manifest.json'; state = json.loads(path.read_text())
        state['parents'][0]['manifest_sha256']='0'*64; path.write_bytes(states.encoded(state))
        index_path=self.root/'research/states/index.json'; index=json.loads(index_path.read_text())
        index['states'][1]['sha256']=states.digest(path.read_bytes()); index_path.write_bytes(states.encoded(index))
        with self.assertRaisesRegex(ValueError,'ancestry'): states.validate(self.root)

    def test_merkle_root_binds_paths_as_well_as_contents(self):
        a=[{'path':'a','sha256':states.digest(b'same')}]; b=[{'path':'b','sha256':states.digest(b'same')}]
        self.assertNotEqual(states.merkle_root(a),states.merkle_root(b))

    def test_graph_rejects_cycles_and_missing_dependencies(self):
        graph=json.loads((ROOT/'research/process/graph.json').read_text())
        self.assertEqual(len(dependency_order(graph)),len(graph['nodes']))
        cyclic=copy.deepcopy(graph);cyclic['edges'].append({'from':'process-question','to':'allocation-choice','relation':'depends_on'})
        with self.assertRaisesRegex(ValueError,'Cycle'):dependency_order(cyclic)
        missing=copy.deepcopy(graph);missing['edges'][0]['to']='not-a-node'
        with self.assertRaisesRegex(ValueError,'Unknown'):dependency_order(missing)

    def test_unsafe_archive_paths_are_rejected(self):
        for path in ['../secret','/absolute','a/../b','./a']:
            with self.assertRaises(ValueError):states.safe_path(path)

if __name__ == '__main__': unittest.main()
