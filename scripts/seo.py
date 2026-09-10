"""Deterministic discovery metadata. Describes the project, never implies research results."""
import html
import json
from urllib.parse import urljoin

SITE = 'https://stewalexander-com.github.io/energy-density-challenge/'
REPO = 'https://github.com/StewAlexander-com/energy-density-challenge'
NAME = 'Energy Density Challenge'
IMAGE = 'assets/social-preview.jpg'
IMAGE_ALT = 'Energy Density Challenge. Is energy density the right problem? Open research. Start with the question.'
PAGES = {
    'license.html': ('MIT license', 'Read the Energy Density Challenge MIT license: permission to use, modify and share original project materials, with copyright and permission notices preserved.'),
    'index.html': ('Is energy density the right problem?', 'An open research challenge: test whether energy density is the right problem. Compare alternatives, inspect assumptions and contribute a better question.'),
    'explore.html': ('Explore the assumptions', 'Explore a proposed energy systems model, compare efficiency and demand, and inspect the unresolved hypothesis and proposed first study.'),
    'guide.html': ('Research guide', 'Review the Energy Density Challenge methodology, proposed first study, evidence rules, source limits, safety boundaries and contribution process.'),
    'contribute.html': ('Contribute a question', 'Draft a bounded research question with a baseline, feasible alternative, evidence status and an observation that would change your mind.'),
    'review.html': ('Ten cumulative reviews', 'Read the ten-step review of the founding brief: why the first assignment is to test the energy density framing before choosing a solution.'),
    'ux-review.html': ('Twenty-step UX review', 'Follow twenty cumulative reviews of the Energy Density Challenge interface, navigation, grammar, spacing and readability.'),
    'resources.html': ('Share and reuse', 'Share the Energy Density Challenge, find its reviews, download AI-readable research records and learn how to cite and reuse the project.'),
}

def canonical(path):
    return SITE if path == 'index.html' else urljoin(SITE, path)

def head(path):
    title, description = PAGES[path]
    url = canonical(path)
    esc = lambda value: html.escape(str(value), quote=True)
    tags = [f'<title>{esc(title)} — {NAME}</title>',
            f'<link rel="canonical" href="{url}">',
            '<link rel="sitemap" type="application/xml" href="sitemap.xml">',
            '<link rel="describedby" type="text/plain" href="llms.txt" title="AI reading index">',
            '<link rel="license" href="LICENSE">']
    meta = {'description': description, 'robots': 'index, follow, max-image-preview:large',
            'theme-color': '#214f60', 'twitter:card': 'summary_large_image',
            'twitter:title': title, 'twitter:description': description,
            'twitter:image': SITE + IMAGE, 'twitter:image:alt': IMAGE_ALT}
    og = {'og:type': 'website', 'og:site_name': NAME, 'og:locale': 'en_US',
          'og:title': title, 'og:description': description, 'og:url': url,
          'og:image': SITE + IMAGE, 'og:image:secure_url': SITE + IMAGE,
          'og:image:type': 'image/jpeg', 'og:image:width': '1200', 'og:image:height': '628',
          'og:image:alt': IMAGE_ALT}
    for attr, values in [('name', meta), ('property', og)]:
        tags.extend(f'<meta {attr}="{key}" content="{esc(value)}">' for key, value in values.items())
    graph = [
        {'@type': 'WebSite', '@id': SITE + '#website', 'name': NAME, 'url': SITE,
         'description': PAGES['index.html'][1], 'inLanguage': 'en', 'sameAs': REPO},
        {'@type': 'WebPage', '@id': url + '#webpage', 'name': title, 'description': description,
         'url': url, 'inLanguage': 'en', 'isPartOf': {'@id': SITE + '#website'},
         'primaryImageOfPage': {'@type': 'ImageObject', 'url': SITE + IMAGE, 'width': 1200, 'height': 628},
         'license': SITE + 'LICENSE'},
    ]
    if path != 'index.html':
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': NAME, 'item': SITE},
            {'@type': 'ListItem', 'position': 2, 'name': title, 'item': url}]})
    if path == 'resources.html':
        graph.append({'@type': 'SoftwareSourceCode', '@id': REPO + '#source', 'name': NAME,
                      'codeRepository': REPO, 'url': REPO, 'license': SITE + 'LICENSE',
                      'description': 'Source code and documentation for a static research commons. The model is proposed and uncalibrated; no project result is recorded.',
                      'programmingLanguage': ['Python', 'JavaScript', 'HTML', 'CSS'],
                      'runtimePlatform': 'Static website; no backend required'})
    payload = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('<', '\\u003c')
    tags.append('<script type="application/ld+json">' + payload + '</script>')
    return '\n'.join(tags)

def sitemap():
    urls = ''.join(f'  <url><loc>{canonical(path)}</loc></url>\n' for path in PAGES)
    # Omit optional lastmod: rebuild time is not a content modification date.
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n'
