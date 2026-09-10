# The Energy Density Challenge

A standing challenge to human and artificial intelligence.

**First assignment: determine whether energy density is the right problem framing.** The name is provisional. No leverage ranking, completed experiment, or breakthrough is claimed.

[Open the website](https://StewAlexander-com.github.io/energy-density-challenge/) · [Ten cumulative reviews](docs/ten-step-review.md) · [AI entry point](AI_CHALLENGE.md) · [Contribute](CONTRIBUTING.md)

## Start here

For a specified useful service, what constraint matters most, and which intervention improves the outcome without unacceptable burdens elsewhere?

Energy density is one candidate. It must be compared with efficiency, service redesign, infrastructure, operations and the best feasible existing option. A result can retain, narrow, replace or leave the framing unresolved.

[Twenty-step UX review](docs/ux-review.md) documents the readability and interface revision.

## What exists

- One proposed, uncalibrated [systems model](research/models/EDC-M-0001.json), created because the original model was not supplied. Every edge is an untested conditional hypothesis.
- One unresolved [framing hypothesis](research/hypotheses/EDC-H-0001.json) and one proposed [desk audit](research/experiments/EDC-E-0001.json).
- An accessible static website, a cumulative ten-step review, source ledger, research protocol, schemas, contribution forms and validation workflow.
- No project results, independent replications, validated leverage ranking, running AI research system or distributed-compute service.

## Read and reuse

`challenge.json` is the machine entry point. `research/index.json` lists permanent records. Sources support only the statements described in `research/literature/sources.json`. Unknown values are null with a reason. Missing evidence never becomes zero or a positive finding.

[Methodology](METHODOLOGY.md) · [Safety](SAFETY.md) · [Governance](docs/governance.md) · [Proposed model](docs/model-methodology.md) · [AI roles](docs/research-protocol.md) · [Future compute contributions](docs/donate-intelligence.md)

## Local preview and validation

The public site uses only HTML, CSS and JavaScript. It needs no backend, API key, runtime package download, or tracking service.

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173/. JavaScript enhances the model explorer, calculator and draft builder; the question, review, protocol and records remain readable without it.

To edit and check generated pages:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
python3 scripts/build.py
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests
python3 scripts/build.py --check
node --check assets/site.js
```

Edit `templates/`, the Markdown documents and the JSON research records; regenerate the HTML pages. CI rejects stale generated pages, invalid records and broken local references before publishing.

See [deployment instructions](docs/deployment.md). Original project content is MIT licensed; third-party sources and contributed data retain their own licenses. Attribution and provenance are required regardless of license.
