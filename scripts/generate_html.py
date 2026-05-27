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
