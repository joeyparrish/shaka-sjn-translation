# HTML Translation Table Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate a GitHub Pages HTML table from `sjn-translations.yaml` on every push to `main`, displaying key, English, literal, romanized, and Tengwar columns with a placeholder "More info" button.

**Architecture:** A Python/Jinja2 generation script reads the YAML and renders `site/index.html` from `site/index.html.j2`. A GitHub Actions workflow runs the script on push and deploys the `site/` directory via the official Pages deployment actions.

**Tech Stack:** Python 3, PyYAML, Jinja2, GitHub Actions (`actions/checkout@v6`, `actions/upload-pages-artifact@v5`, `actions/deploy-pages@v5`)

---

### Task 1: Prepare the site directory

**Files:**
- Create: `site/` (directory)
- Move: `TengwarTelcontar.woff2` → `site/TengwarTelcontar.woff2`
- Modify: `.gitignore`

- [ ] **Step 1: Create the site directory and move the font**

```bash
mkdir site
git mv TengwarTelcontar.woff2 site/TengwarTelcontar.woff2
```

- [ ] **Step 2: Add the generated file to .gitignore**

Append to `.gitignore`:

```
site/index.html
```

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "Move font into site/ and gitignore generated index.html"
```

Expected: commit succeeds, `git status` clean.

---

### Task 2: Create the Jinja2 template

**Files:**
- Create: `site/index.html.j2`

- [ ] **Step 1: Write the template**

Create `site/index.html.j2` with this exact content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Shaka Player Sindarin Translations</title>
  <style>
    @font-face {
      font-family: TengwarTelcontar;
      src: url('TengwarTelcontar.woff2') format('woff2');
    }

    body {
      font-family: system-ui, sans-serif;
      max-width: 1400px;
      margin: 2rem auto;
      padding: 0 1.5rem;
      color: #222;
    }

    h1 {
      margin-bottom: 1.5rem;
      font-size: 1.5rem;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
    }

    th, td {
      text-align: left;
      padding: 0.5rem 0.75rem;
      border-bottom: 1px solid #ddd;
      vertical-align: top;
    }

    th {
      background: #f0f0f0;
      font-weight: 600;
      position: sticky;
      top: 0;
    }

    tr:nth-child(even) td {
      background: #fafafa;
    }

    .col-tengwar {
      font-family: TengwarTelcontar;
      font-size: 1.2em;
    }

    .more-info {
      font-size: 0.8rem;
      padding: 0.25rem 0.6rem;
      cursor: pointer;
      border: 1px solid #bbb;
      border-radius: 3px;
      background: #fff;
      white-space: nowrap;
    }

    .more-info:hover {
      background: #f0f0f0;
    }
  </style>
</head>
<body>
  <h1>Shaka Player Sindarin Translations</h1>
  <table>
    <thead>
      <tr>
        <th>Key</th>
        <th>English</th>
        <th>Literal</th>
        <th>Romanized</th>
        <th>Tengwar</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      {% for item in translations %}
      <tr>
        <td>{{ item.key }}</td>
        <td>{{ item.english }}</td>
        <td>{{ item.sjn.literal }}</td>
        <td>{{ item.sjn.roman }}</td>
        <td class="col-tengwar">{{ item.sjn.tengwar }}</td>
        <td><button class="more-info" data-key="{{ item.key }}">More info</button></td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add site/index.html.j2
git commit -m "Add Jinja2 HTML template for translation table"
```

Expected: commit succeeds.

---

### Task 3: Write the generation script (TDD)

**Files:**
- Create: `tests/test_generate_html.py`
- Create: `scripts/generate_html.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_generate_html.py`:

```python
import os
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_generate_html():
    result = subprocess.run(
        ["python", "scripts/generate_html.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

    output_path = os.path.join(REPO_ROOT, "site", "index.html")
    with open(output_path) as f:
        html = f.read()

    assert "@font-face" in html
    assert "TengwarTelcontar" in html
    assert "<table" in html
    assert "AD_DURATION" in html
    assert "More info" in html
```

- [ ] **Step 2: Install test dependencies and run to verify failure**

```bash
pip install pyyaml jinja2 pytest
pytest tests/test_generate_html.py -v
```

Expected output contains: `FAILED` or `ERROR` — the script doesn't exist yet.

- [ ] **Step 3: Write the generation script**

Create `scripts/generate_html.py`:

```python
#!/usr/bin/env python3
import os
import yaml
from jinja2 import Environment, FileSystemLoader

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source_path = os.path.join(base_path, "sjn-translations.yaml")
template_dir = os.path.join(base_path, "site")
output_path = os.path.join(base_path, "site", "index.html")

with open(source_path) as f:
    source = yaml.safe_load(f)

env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("index.html.j2")

html = template.render(translations=source["translations"])

with open(output_path, "w") as f:
    f.write(html)
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
pytest tests/test_generate_html.py -v
```

Expected output: `PASSED` for `test_generate_html`.

- [ ] **Step 5: Spot-check the generated file**

```bash
grep -c "<tr>" site/index.html
```

Expected: a number greater than 1 (one header row plus one per translation entry; the YAML has ~70 entries so expect ~71).

- [ ] **Step 6: Commit**

```bash
git add scripts/generate_html.py tests/test_generate_html.py
git commit -m "Add HTML generation script and integration test"
```

Expected: commit succeeds.

---

### Task 4: Write the GitHub Actions workflow

**Files:**
- Create: `.github/workflows/pages.yml`

- [ ] **Step 1: Create the workflow directory**

```bash
mkdir -p .github/workflows
```

- [ ] **Step 2: Write the workflow file**

Create `.github/workflows/pages.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - name: Install dependencies
        run: pip install pyyaml jinja2

      - name: Generate HTML
        run: python scripts/generate_html.py

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v5
        with:
          path: site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v5
```

- [ ] **Step 3: Commit and push**

```bash
git add .github/workflows/pages.yml
git commit -m "Add GitHub Actions workflow to build and deploy Pages"
git push
```

Expected: push succeeds; navigate to the repo's Actions tab to watch the workflow run. Both the `build` and `deploy` jobs should turn green.
