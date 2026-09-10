# GitHub Pages deployment

This project is a static website designed for a repository subpath such as `https://OWNER.github.io/energy-density-challenge/`. Asset and data links are relative. No custom domain, backend, API key, JavaScript build framework or distributed job runner is needed.

## Publish this repository

1. Create a public GitHub repository and push the files to its `main` branch.
2. In repository Settings → Pages → Build and deployment, choose GitHub Actions as the source.
3. The included Pages workflow validates schemas, permanent references, regression cases, local links, JavaScript syntax and generated-page freshness. It stages only the public site and research documents.
4. The deploy job publishes that validated artifact through the `github-pages` environment. Open the URL shown by the deployment once the workflow succeeds.

Pull requests run validation without a deployment permission or publishing job. Only a successful main-branch build can feed the deployment. Manually rerun from the Actions page if Pages was enabled after the first push.

## Content changes

Edit the source documents, JSON records or `templates/`, then run `python3 scripts/build.py`. Commit both sources and generated HTML. The workflow rejects stale generated pages. `scripts/stage.py` recreates `_site/` from an explicit allowlist and includes `.nojekyll`.

For a fork, update repository links in `scripts/build.py`, `assets/site.js` and the README to the chosen owner and repository, then rebuild. The website has no automatic submission API; draft links only open the issue editor.

## Rollback and failure

If validation fails, the current published site stays in place. Correct the failing source and rerun checks. To roll back, revert the relevant content change through Git and publish the passing revision. Deployment success must be checked in Actions; pushing a commit alone does not confirm publication.

Reference: [GitHub's custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
