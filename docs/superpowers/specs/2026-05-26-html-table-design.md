# HTML Translation Table: Design Spec

Date: 2026-05-26

## Overview

Add a GitHub Pages site that renders the contents of `sjn-translations.yaml` as
a clean HTML table, generated automatically on every push to `main`.

## File Layout

```
site/
  TengwarTelcontar.woff2   # committed; moved from repo root (root copy deleted)
  index.html.j2            # Jinja2 template; committed
  index.html               # generated; gitignored
scripts/
  generate_html.py         # new script; reads YAML, renders template
.github/
  workflows/
    pages.yml              # CI/CD workflow
```

`site/index.html` is added to `.gitignore`. All other files under `site/` are
committed. The root-level `TengwarTelcontar.woff2` is deleted as part of the
move. The `site/` directory is the Pages artifact root, so the font and
the generated HTML are served from the same directory without any path
gymnastics.

## HTML Template (`site/index.html.j2`)

A single self-contained page. Key characteristics:

- `@font-face` declaration loads `TengwarTelcontar.woff2` from the same
  directory, aliased as `TengwarTelcontar`.
- Body uses a system sans-serif stack, centered with a modest max-width.
- One `<table>` with `border-collapse: collapse`, taking full width.
- Six columns: Key, English, Literal, Romanized, Tengwar, (more info).
- Header row has a light background and bold text.
- Data rows have a 1px separator and alternating stripe.
- The Tengwar cell applies `font-family: TengwarTelcontar`.
- The last column contains a `<button class="more-info">` element per row;
  it is present and styled but has no behavior yet.

Styling is inline in a `<style>` block in `<head>`. No external CSS framework.

## Generation Script (`scripts/generate_html.py`)

Reads `sjn-translations.yaml` with PyYAML, passes the `translations` list to
Jinja2, and writes the rendered output to `site/index.html`. The template path
is `site/index.html.j2` relative to the repo root. The script requires no
arguments; paths are resolved relative to the script's own location.

Dependencies: `pyyaml` (already used by existing scripts), `jinja2`.

## GitHub Actions Workflow (`.github/workflows/pages.yml`)

Trigger: `push` to `main`.

### Permissions

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

### Jobs

**build**
1. `actions/checkout@v4`
2. `pip install pyyaml jinja2`
3. `python scripts/generate_html.py`
4. `actions/upload-pages-artifact@v3` with `path: site`

**deploy** (depends on build)
1. `actions/deploy-pages@v4`

The Pages source in repository settings is set to "GitHub Actions" (already
configured by the user).

## Out of Scope

- "More info" button behavior (future work).
- Search, filtering, or sorting of the table.
- Dark mode or theming beyond clean minimal polish.
