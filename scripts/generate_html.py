#!/usr/bin/env python3
import datetime
import json
import os
import sys
import yaml
from jinja2 import Environment, FileSystemLoader

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stats as stats_module
source_path = os.path.join(base_path, "sjn-translations.yaml")
source_json_path = os.path.join(base_path, "source.json")
meta_path = os.path.join(base_path, "source-meta.json")
template_dir = os.path.join(base_path, "site")
output_path = os.path.join(base_path, "site", "index.html")

with open(source_path) as f:
    source = yaml.safe_load(f)

with open(source_json_path, encoding="utf-8") as f:
    source_json = json.load(f)

source_meta = None
if os.path.exists(meta_path):
    with open(meta_path, encoding="utf-8") as f:
        source_meta = json.load(f)

translation_stats = stats_module.compute(source, source_json)

def _serialize(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    raise TypeError(f"{type(obj)} is not JSON serializable")

# Embed full data for the modal JS; escape </ to prevent script tag injection.
translations_json = json.dumps(source["translations"], default=_serialize)
translations_json = translations_json.replace("</", "<\\/")

env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("index.html.j2")

html = template.render(
    translations=source["translations"],
    translations_json=translations_json,
    source_meta=source_meta,
    translation_stats=translation_stats,
)

with open(output_path, "w") as f:
    f.write(html)
