# Preserved research states

ASTRA-STATE-0001 is the exact tracked repository at commit `3b55fbab2ea9b94e0f78e9d458d5f6144cbed026`. Its archive includes the original conclusions, criticisms, proposed records, source limits, review documents and implementation. Only recorded material can be preserved; this does not reconstruct unrecorded reasoning or certify independent review.

ASTRA-STATE-0002 is a child containing the new directive, cumulative review, protocol, proposed evaluation, allocation decision, process graph, source ledger and transition record. It is a selected research bundle, not a claim to contain the entire publishing checkout. The publishing Git commit separately preserves the implementation. Follow [the state index](../research/states/index.json) to both manifests and archives.

## How integrity is recorded

Each state directory contains exactly `source.tar` and `manifest.json`. The manifest records the archive SHA-256, a sorted list of regular file paths, byte counts and SHA-256 digests, and a deterministic Merkle root. No symlinks or path traversal entries are allowed. Nothing is extracted during validation.

The scheme identifier is `edc-path-content-v1`:

1. Order paths by Python's Unicode string order. Paths are canonical relative POSIX paths, encoded in UTF-8.
2. Hash each file's exact bytes with SHA-256.
3. A leaf is SHA-256 of byte `0x00`, the path bytes, byte `0x00`, and the raw 32-byte file digest.
4. A parent is SHA-256 of byte `0x01`, its left child digest and its right child digest. Duplicate the last digest at an odd level. A one-file tree uses its leaf. Empty archives are rejected.
5. A child state records the SHA-256 of its parent's exact manifest bytes, including the final newline. The state index records each manifest's exact digest. These are linked research-state records; causal cycles in the energy model are separate.

The new hashes and manifests were added during State 0002. The earlier repository used Git and linked JSON; it did not already implement this application-level state mechanism. W3C PROV is relevant prior art, but this small graph is not claimed to conform to its model.

## Verify a checkout

Run the checks from the repository root:

```sh
python3 scripts/research_states.py
python3 scripts/research_states.py --base <trusted-earlier-commit>
```

The normal validation workflow checks archive bytes, members, roots, parent hashes, index coverage and original scientific files. With a trusted earlier commit, it also rejects edits or removal of any previously published state file. The seal operation refuses to overwrite an existing manifest or archive. Corrections belong in a new child state and an explicit transition; do not edit a published state to clean up its history.

State 0001's original scientific files remain byte-for-byte intact in the live repository. State 0002's selected research files are checked against their snapshot. A later change should add a successor and update verification deliberately, retaining all earlier snapshots and explaining any supersession.

## What these checks cannot prove

A hash is not truth, an independent replication, a timestamp authority, a signature of a human author or a guarantee of permanent storage. A repository owner can change branch history or validation code. This is an append-only project policy with tamper detection against trusted references, not externally enforced write-once storage.

Retain a trusted commit or manifest outside the mutable branch if you need to detect coordinated rewriting of content and its reference digests. Availability and stronger archival custody remain separate concerns. Do not convert successful integrity checks into confidence in a scientific claim.
