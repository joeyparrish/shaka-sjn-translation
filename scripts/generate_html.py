#!/usr/bin/env python3
import datetime
import json
import os
import yaml
from jinja2 import Environment, FileSystemLoader

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source_path = os.path.join(base_path, "sjn-translations.yaml")
template_dir = os.path.join(base_path, "site")
output_path = os.path.join(base_path, "site", "index.html")

with open(source_path) as f:
    source = yaml.safe_load(f)

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
)

with open(output_path, "w") as f:
    f.write(html)
