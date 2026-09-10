# Search, sharing and AI discovery

The site exposes its content as static HTML, Markdown and JSON. The discovery layer describes the project as it exists; it does not claim a breakthrough, measured dataset, scientific endorsement or peer-reviewed publication.

## What is published

- Each HTML page has its own title, description, absolute canonical URL, Open Graph tags and X large-image card tags.
- A 1200 × 628 JPEG title card supplies an absolute image URL, MIME type, dimensions and alternative text. It is shared across pages; page titles and descriptions remain specific.
- Schema.org JSON-LD describes the website, individual pages, breadcrumbs and the source repository. It does not mark the untested model as an empirical dataset.
- `sitemap.xml` lists canonical HTML pages. The homepage uses the directory URL, not a second `index.html` entry. Optional change frequency, priority and modification dates are omitted because they would add invented precision.
- `llms.txt` provides a curated AI reading index. `llms-full.txt` combines canonical source documents and records, with source URLs. `discovery.json` lists structured file and schema URLs.
- `CITATION.cff` supports repository citation. Cite an exact commit when reproducibility matters; no DOI, formal release or individual authorship is invented.
- The footer offers a manual link, a copy button and native device sharing where supported. Nothing posts automatically. No social SDK, tracker or third-party script is loaded.

Open Graph is intended for compatible sharing services; X card tags add its large-image format. Other apps may use these tags or their own extraction rules. The native share sheet and copyable link also work for services without a web sharing endpoint. Card appearance and support vary by app. A site cannot force a preview everywhere.

## GitHub Pages and robots.txt

This is a project site at `https://stewalexander-com.github.io/energy-density-challenge/`. Crawlers fetch robots.txt from the host root, `https://stewalexander-com.github.io/robots.txt`. A file under `/energy-density-challenge/` cannot set host crawl rules.

The host-root file returned HTTP 404 when checked on September 10, 2026 UTC. No project-level robots.txt is shipped as a misleading substitute. Pages declare `index, follow, max-image-preview:large`; no login or client-rendering barrier is added. A missing robots.txt normally means no robots-file restrictions, not guaranteed indexing.

If a host-root site is established later, preserve its existing rules and add this sitemap line there:

```text
Sitemap: https://stewalexander-com.github.io/energy-density-challenge/sitemap.xml
```

## Search engine submission

The deployed sitemap is ready for submission. Account ownership verification and sitemap submission have not been performed by this change.

1. In [Google Search Console](https://search.google.com/search-console/), add the exact HTTPS project URL as a URL-prefix property. Complete an offered ownership verification method. If using an HTML verification file, add the exact supplied file to the public staging allowlist; do not invent a token.
2. Submit `sitemap.xml` under that property. Use URL Inspection for the homepage and important review pages.
3. In [Bing Webmaster Tools](https://www.bing.com/webmasters/), verify the same site or use its available import process, then submit the same sitemap.
4. Review crawl and indexing reports after processing. Submission, structured data and llms.txt do not guarantee discovery, ranking or AI citation.

This project’s llms.txt is a convenience format, not an access-control file or proof that every AI provider uses it. Google site-name display is scoped to domains and subdomains; a GitHub project subdirectory should not be promised its own site-name treatment.

## Check sharing previews

Inspect the published HTML and image first. Use [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) and [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/) when signed in to those services. Refresh an old cached preview there when possible. Test the link in the intended app before a campaign; not every app exposes a debugger.

The repository’s own GitHub social preview is a separate repository setting. A website og:image tag does not configure it. This upload remains pending because the available browser is not signed in to GitHub settings. The prepared `assets/social-preview.jpg` can be uploaded in the repository’s Social preview settings.

When replacing the card artwork, give the new file a versioned name and update `scripts/seo.py` with its real dimensions. This makes image-cache changes explicit. Do not load the sharing image above the fold merely to trigger previews; crawlers get it from the head metadata.

## Maintenance and verification

Edit `scripts/seo.py` for page summaries and canonical metadata, `scripts/build.py` for generated reading packs, and `templates/resources.html` for the human directory. Update launch-status prose when canonical research status changes. Regenerate with `python3 scripts/build.py`; `--check` rejects stale generated discovery files as well as stale pages.

The test suite checks sitemap coverage, canonical consistency, metadata uniqueness, structured-data URLs, image dimensions, public discovery references and citation fields. Public staging includes only intended files. CI runs these checks before deployment. The reading pack is generated locally from project records; external source papers are not copied into it.

## Standards and references

- [Open Graph protocol](https://ogp.me/) — metadata and image properties.
- [Schema.org SoftwareSourceCode](https://schema.org/SoftwareSourceCode) — source repository description.
- [Google sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) — canonical URLs and submission.
- [Google robots.txt specification](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec) — host-root scope and error handling.
- [Google site names](https://developers.google.com/search/docs/appearance/site-names) — domain and subdomain scope.
- [llms.txt proposal](https://llmstxt.org/) — structured reading indexes, including subpaths.
- [GitHub citation files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files) — repository citation metadata.

- [GitHub social previews](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview) — repository image upload.
- [X image alternative text](https://blog.x.com/developer/en_us/a/2016/alt-text-support-for-twitter-cards-and-the-rest-api) — accessible card descriptions.
