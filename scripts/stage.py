#!/usr/bin/env python3
"""Stage only intentional public files. Never publish Git metadata or local environments."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'_site'
if DEST.exists():shutil.rmtree(DEST)
DEST.mkdir()
for name in ['resources.html','sitemap.xml','llms.txt','llms-full.txt','discovery.json','CITATION.cff','index.html','explore.html','contribute.html','ux-review.html','review.html','guide.html','.nojekyll','README.md','AI_CHALLENGE.md','CONTRIBUTING.md','METHODOLOGY.md','SAFETY.md','LICENSE','challenge.json','assets','research','schemas','docs']:
 src=ROOT/name;dst=DEST/name
 if src.is_dir():shutil.copytree(src,dst,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.DS_Store'))
 else:shutil.copy2(src,dst)
print('Public site staged in _site/.')
