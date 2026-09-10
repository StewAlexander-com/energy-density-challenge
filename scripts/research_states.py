#!/usr/bin/env python3
"""Content-addressed research snapshots. Integrity is not scientific validation."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import re
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '3b55fbab2ea9b94e0f78e9d458d5f6144cbed026'
PRESERVED = ['challenge.json', 'research/models/EDC-M-0001.json',
             'research/hypotheses/EDC-H-0001.json', 'research/experiments/EDC-E-0001.json',
             'research/literature/sources.json', 'docs/ten-step-review.md', 'METHODOLOGY.md', 'SAFETY.md']

def digest(data):
    return hashlib.sha256(data).hexdigest()

def encoded(record):
    return (json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()

def safe_path(name):
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or not p.parts or str(p) != name:
        raise ValueError('Unsafe or noncanonical archive path: ' + name)
    return p

def archive_files(path):
    files = {}
    with tarfile.open(path, 'r:') as archive:
        for item in archive:
            if item.isdir():
                safe_path(item.name.rstrip('/')); continue
            safe_path(item.name)
            if not item.isfile() or item.name in files:
                raise ValueError('Archive must contain unique regular files: ' + item.name)
            files[item.name] = archive.extractfile(item).read()
    if not files: raise ValueError('Empty state archive')
    return files

def merkle_root(entries):
    if not entries or [e['path'] for e in entries] != sorted({e['path'] for e in entries}):
        raise ValueError('Manifest paths must be unique, nonempty and sorted')
    level = [hashlib.sha256(b'\x00' + e['path'].encode('utf-8') + b'\x00' + bytes.fromhex(e['sha256'])).digest() for e in entries]
    while len(level) > 1:
        if len(level) % 2: level.append(level[-1])
        level = [hashlib.sha256(b'\x01' + level[i] + level[i+1]).digest() for i in range(0, len(level), 2)]
    return level[0].hex()

def seal(state_id, parent=None, files=None):
    if not re.fullmatch(r'ASTRA-STATE-\d{4}', state_id): raise ValueError('Invalid state ID')
    directory = ROOT/'research/states'/state_id
    if (directory/'manifest.json').exists(): raise ValueError('Refusing to replace a sealed state')
    directory.mkdir(parents=True, exist_ok=True)
    archive = directory/'source.tar'
    if files is not None:
        if archive.exists(): raise ValueError('Refusing to replace a state archive')
        # Fixed metadata makes the bundle reproducible for exactly these bytes.
        import io
        with tarfile.open(archive, 'w', format=tarfile.PAX_FORMAT) as output:
            for name in sorted(set(files)):
                safe_path(name); data = (ROOT/name).read_bytes()
                info = tarfile.TarInfo(name); info.size = len(data); info.mode = 0o644; info.mtime = 0
                output.addfile(info, io.BytesIO(data))
    contents = archive_files(archive)
    entries = [{'path': p, 'bytes': len(b), 'sha256': digest(b)} for p,b in sorted(contents.items())]
    parents = []
    if parent:
        parent_path = ROOT/'research/states'/parent/'manifest.json'
        parents = [{'id': parent, 'manifest_sha256': digest(parent_path.read_bytes())}]
    record = {'id': state_id, 'parents': parents, 'sealed_on': '2026-09-10',
              'kind': 'historical_snapshot' if not parent else 'conceptual_extension',
              'baseline_commit': BASELINE if not parent else None,
              'scope': 'All tracked baseline files' if not parent else 'Selected State 0002 research documents and records; the publishing commit retains the full implementation',
              'archive': 'source.tar', 'archive_sha256': digest(archive.read_bytes()),
              'hash_algorithm': 'sha256', 'merkle_scheme': 'edc-path-content-v1',
              'merkle_root': merkle_root(entries), 'files': entries,
              'scientific_validation': False,
              'limits': 'Tamper-evident against a trusted prior manifest or commit; not externally immutable, independently reviewed, or proof of truth.'}
    (directory/'manifest.json').write_bytes(encoded(record))
    index_path = ROOT/'research/states/index.json'
    index = json.loads(index_path.read_text()) if index_path.exists() else {'states': []}
    if any(s['id'] == state_id for s in index['states']): raise ValueError('Duplicate state ID')
    index['states'].append({'id': state_id, 'manifest': (directory/'manifest.json').relative_to(ROOT).as_posix(), 'sha256': digest(encoded(record))})
    index_path.write_bytes(encoded(index))
    return record

def validate(root=ROOT):
    index = json.loads((root/'research/states/index.json').read_text())
    known = {}; snapshots = {}
    for entry in index['states']:
        state_id = entry['id']
        if state_id in known or not re.fullmatch(r'ASTRA-STATE-\d{4}', state_id): raise ValueError('Duplicate or invalid state ID')
        expected = f'research/states/{state_id}/manifest.json'
        if entry['manifest'] != expected: raise ValueError('State path disagrees with ID')
        path = root/expected; raw = path.read_bytes(); state = json.loads(raw)
        if digest(raw) != entry['sha256'] or state['id'] != state_id: raise ValueError('State manifest digest mismatch')
        if state['archive'] != 'source.tar' or state['hash_algorithm'] != 'sha256' or state['merkle_scheme'] != 'edc-path-content-v1': raise ValueError('Unknown archive or hash scheme')
        if state['scientific_validation'] is not False: raise ValueError('Integrity cannot imply scientific validation')
        if set(p.name for p in path.parent.iterdir()) != {'source.tar','manifest.json'}: raise ValueError('Unexpected file in sealed state')
        archive = path.parent/state['archive']
        if digest(archive.read_bytes()) != state['archive_sha256']: raise ValueError('State archive digest mismatch')
        contents = archive_files(archive)
        entries = [{'path': p, 'bytes': len(b), 'sha256': digest(b)} for p,b in sorted(contents.items())]
        if entries != state['files'] or merkle_root(entries) != state['merkle_root']: raise ValueError('State file or Merkle root mismatch')
        for parent in state['parents']:
            if parent['id'] not in known or known[parent['id']] != parent['manifest_sha256']:
                raise ValueError('Missing, cyclic or altered state ancestry')
        if state_id == 'ASTRA-STATE-0001':
            if state['parents'] or state['baseline_commit'] != BASELINE: raise ValueError('Baseline ancestry changed')
            for name in PRESERVED:
                if contents[name] != (root/name).read_bytes(): raise ValueError('State 0001 scientific content changed: ' + name)
        elif not state['parents']: raise ValueError('Child state must identify a parent')
        known[state_id] = entry['sha256']; snapshots[state_id] = contents
    expected_dirs = {p.name for p in (root/'research/states').glob('ASTRA-STATE-*') if p.is_dir()}
    if set(known) != expected_dirs or 'ASTRA-STATE-0001' not in known: raise ValueError('State index is incomplete')
    for name, data in snapshots.get('ASTRA-STATE-0002', {}).items():
        if (root/name).read_bytes() != data: raise ValueError('State 0002 artifact changed; add a successor state: ' + name)
    return len(known)

def unchanged_since(base):
    if not base or set(base) == {'0'}: return
    # Compare committed bytes to the trusted preceding revision, not mtimes or labels.
    paths = subprocess.check_output(['git','ls-tree','-r','--name-only',base,'--','research/states']).decode().splitlines()
    for path in paths:
        if re.match(r'research/states/ASTRA-STATE-\d{4}/', path):
            old = subprocess.check_output(['git','show',f'{base}:{path}'])
            if not (ROOT/path).is_file() or (ROOT/path).read_bytes() != old:
                raise ValueError('Published state is append-only: ' + path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--base'); args = parser.parse_args()
    if args.base: unchanged_since(args.base)
    print(f'Verified {validate()} state snapshots and ancestry. Integrity is not truth.')
