import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('validate',ROOT/'scripts/validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def read(path):return json.loads((ROOT/path).read_text())
class GuardTests(unittest.TestCase):
 def setUp(self):self.h=read('research/hypotheses/EDC-H-0001.json')
 def promotion(self,status):
  h=self.h;h['status']=status;h['confidence_history'][-1]['status']=status
  h['scope']={k:'Registered test conditions' for k in h['scope']};h['baseline']='Baseline';h['prediction']='Prediction';h['thresholds']={'minimum':'Registered'};h['evidence']=['R1'];return h
 def test_launch_record_is_unresolved(self):v.validate_hypothesis(self.h,{}, {})
 def test_status_cannot_silently_change(self):
  self.h['status']='falsified'
  with self.assertRaisesRegex(ValueError,'history'):v.validate_hypothesis(self.h,{}, {})
 def test_confidence_number_needs_calibration(self):
  self.h['confidence']['value']=.99
  with self.assertRaisesRegex(ValueError,'calibration'):v.validate_hypothesis(self.h,{}, {})
 def test_falsification_needs_result(self):
  h=self.promotion('falsified')
  with self.assertRaisesRegex(ValueError,'result record'):v.validate_hypothesis(h,{'R1':{}},{})
 def test_shared_group_is_not_independent_replication(self):
  h=self.promotion('supported_within_tested_conditions');h['result_ids']=['R1','R2'];h['replications']=[{'group':'same','result_id':r} for r in ['R1','R2']]
  with self.assertRaisesRegex(ValueError,'independent'):v.validate_hypothesis(h,{'R1':{},'R2':{}},{})
 def test_simulation_cannot_be_physical_replication(self):
  h=self.promotion('supported_within_tested_conditions');h['result_ids']=['R1','R2'];h['replications']=[{'group':r,'result_id':r} for r in ['R1','R2']]
  with self.assertRaisesRegex(ValueError,'physical replication'):v.validate_hypothesis(h,{r:{'evidence_kind':'simulation'} for r in ['R1','R2']},{})
 def test_unverified_source_cannot_be_evidence(self):
  self.h['evidence']=['S1']
  with self.assertRaisesRegex(ValueError,'Unverified'):v.validate_hypothesis(self.h,{}, {'S1':{'verification':'lead_only_direct_fetch_403'}})
 def test_registration_cannot_omit_boundary(self):
  experiment=read('research/experiments/EDC-E-0001.json');experiment['status']='registered'
  with self.assertRaisesRegex(ValueError,'preregistration'):v.validate_experiment(experiment)
 def test_model_weight_cannot_imply_measurement(self):
  model=read('research/models/EDC-M-0001.json');model['edges'][0]['strength']=.8
  with self.assertRaisesRegex(ValueError,'weights'):v.validate_model(model)
 def test_missing_model_node_rejected(self):
  model=read('research/models/EDC-M-0001.json');model['edges'][0]['target']='imaginary'
  with self.assertRaisesRegex(ValueError,'missing node'):v.validate_model(model)
 def test_index_cannot_drift(self):
  records={k:[read(str(p.relative_to(ROOT))) for p in ROOT.glob(f'research/{k}/EDC-*.json')] for k in ['hypotheses','experiments','results','models']};index=read('research/index.json');index['hypotheses'][0]['status']='falsified'
  with self.assertRaisesRegex(ValueError,'Index status'):v.validate_index(index,records)
if __name__=='__main__':unittest.main()
