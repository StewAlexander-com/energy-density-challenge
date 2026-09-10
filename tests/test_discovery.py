"""Check public discovery contracts: URLs, previews and evidence boundaries."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import struct
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://stewalexander-com.github.io/energy-density-challenge/'

class Metadata(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.meta = {}; self.links = {}; self.graphs = []; self.capture = False; self.payload = ''
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta':
            key = a.get('name', a.get('property'))
            if key:
                if key in self.meta: raise ValueError('Duplicate metadata: ' + key)
                self.meta[key] = a.get('content')
        if tag == 'link':
            rel = a.get('rel')
            if rel == 'canonical' and rel in self.links: raise ValueError('Duplicate canonical')
            self.links[rel] = a.get('href')
        if tag == 'script' and a.get('type') == 'application/ld+json': self.capture = True; self.payload = ''
    def handle_data(self, value):
        if self.capture: self.payload += value
    def handle_endtag(self, tag):
        if tag == 'script' and self.capture:
            self.graphs.append(json.loads(self.payload)); self.capture = False

def jpeg_size(path):
    raw = path.read_bytes()
    if raw[:2] != b'\xff\xd8': raise ValueError('Not a JPEG')
    pos = 2
    while pos < len(raw):
        if raw[pos] != 255: raise ValueError('Invalid JPEG segment')
        while raw[pos] == 255: pos += 1
        marker = raw[pos]; pos += 1
        size = int.from_bytes(raw[pos:pos+2], 'big')
        if marker in {0xc0, 0xc1, 0xc2}:
            height, width = struct.unpack('>HH', raw[pos+3:pos+7]); return width, height
        pos += size
    raise ValueError('JPEG has no dimensions')

class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.pages = {p.name: Metadata(p.read_text()) for p in ROOT.glob('*.html')}

    def test_sitemap_exactly_covers_canonical_pages(self):
        tree = ET.parse(ROOT/'sitemap.xml')
        urls = [e.text for e in tree.findall('.//{*}loc')]
        expected = [BASE + ('' if p == 'index.html' else p) for p in self.pages]
        self.assertCountEqual(urls, expected)
        self.assertEqual(len(urls), len(set(urls)))
        self.assertNotIn(BASE+'index.html', urls)

    def test_page_identity_matches_search_social_and_structured_data(self):
        descriptions = set()
        for path, page in self.pages.items():
            url = BASE + ('' if path == 'index.html' else path)
            self.assertEqual(page.links['canonical'], url)
            self.assertEqual(page.meta['og:url'], url)
            self.assertEqual(page.meta['description'], page.meta['og:description'])
            self.assertEqual(page.meta['description'], page.meta['twitter:description'])
            self.assertEqual(page.meta['og:title'], page.meta['twitter:title'])
            descriptions.add(page.meta['description'])
            self.assertIn('index, follow', page.meta['robots'])
            self.assertNotIn('noindex', page.meta['robots'])
            self.assertEqual(len(page.graphs), 1)
            graph = page.graphs[0]
            self.assertEqual(graph['@context'], 'https://schema.org')
            web = next(g for g in graph['@graph'] if g['@type'] == 'WebPage')
            self.assertEqual(web['url'], url)
            self.assertEqual(web['description'], page.meta['description'])
            # No fabricated empirical dataset, rating or scientific publication.
            self.assertTrue(all(g['@type'] in {'WebSite','WebPage','BreadcrumbList','SoftwareSourceCode'} for g in graph['@graph']))
        self.assertEqual(len(descriptions), len(self.pages))

    def test_preview_asset_has_real_dimensions_and_small_payload(self):
        width, height = jpeg_size(ROOT/'assets/social-preview.jpg')
        self.assertGreaterEqual(width, 1200)
        self.assertTrue(1.85 < width/height < 2.05)
        self.assertLess((ROOT/'assets/social-preview.jpg').stat().st_size, 1_000_000)
        for page in self.pages.values():
            self.assertEqual(page.meta['og:image'], BASE+'assets/social-preview.jpg')
            self.assertEqual(page.meta['og:image'], page.meta['twitter:image'])
            self.assertEqual(page.meta['og:image:type'], 'image/jpeg')
            self.assertEqual((int(page.meta['og:image:width']), int(page.meta['og:image:height'])), (width,height))
            self.assertEqual(page.meta['twitter:card'], 'summary_large_image')
            self.assertTrue(page.meta['og:image:alt'])
            self.assertEqual(page.meta['og:image:alt'], page.meta['twitter:image:alt'])

    def test_discovery_urls_resolve_to_public_files(self):
        manifest = json.loads((ROOT/'discovery.json').read_text())
        urls = [x['url'] for group in ['pages','files'] for x in manifest[group]] + manifest['schemas']
        urls += re.findall(r'\]\((https://[^)]+)\)', (ROOT/'llms.txt').read_text())
        for url in urls:
            self.assertTrue(url.startswith(BASE), url)
            suffix = urlsplit(url).path.removeprefix(urlsplit(BASE).path)
            local = ROOT/unquote(suffix or 'index.html')
            self.assertTrue(local.is_file(), url)
        self.assertCountEqual([p['url'] for p in manifest['pages']], [p.links['canonical'] for p in self.pages.values()])
        self.assertEqual(set(manifest['schemas']), {BASE+p.relative_to(ROOT).as_posix() for p in (ROOT/'schemas').glob('*.json')})

    def test_reading_pack_preserves_canonical_research_records(self):
        pack = (ROOT/'llms-full.txt').read_text()
        for path in ['challenge.json','research/index.json','research/models/EDC-M-0001.json','research/hypotheses/EDC-H-0001.json','research/experiments/EDC-E-0001.json','research/literature/sources.json']:
            self.assertIn('Source: '+BASE+path, pack)
            self.assertIn((ROOT/path).read_text().rstrip(), pack)
        self.assertIn('proposed and uncalibrated', (ROOT/'llms.txt').read_text())

    def test_citation_identifies_project_and_repository(self):
        citation = (ROOT/'CITATION.cff').read_text()
        for field in ['cff-version: 1.2.0','title: "Energy Density Challenge"','type: software','authors:','license: MIT','repository-code: "https://github.com/StewAlexander-com/energy-density-challenge"']:
            self.assertIn(field, citation)
        self.assertNotRegex(citation, r'(?m)^doi:')

    def test_duplicate_metadata_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate metadata'):
            Metadata('<meta name="description" content="one"><meta name="description" content="two">')

if __name__ == '__main__': unittest.main()
