#!/usr/bin/env python3
# Shaka Player Sindarin (Elvish) Translations
# Copyright 2026 Joey Parrish
# SPDX-License-Identifier: Apache-2.0

"""Export sjn translations from sjn-translations.yaml to sjn.json.

sjn-translations.yaml is the working file: it tracks the English source, the
literal back-translation, the romanized Sindarin, the Tengwar-encoded form,
and (per the schema in elvish-translation-tools) per-element provenance.
This script reads it and writes the locale file shaka-player consumes.

The Tengwar field uses CSUR Private Use Area codepoints (U+E000-U+E0AE).
We emit them as \\uXXXX escape sequences in the JSON output (json.dumps
default ensure_ascii=True) so the file is reviewable in any editor and
diff-friendly. JSON parsers (including shaka-player's) decode the
escapes transparently at load time.
"""

import json
import os
import sys
import yaml

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scripts_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, scripts_path)
import stats as stats_module

source_path = os.path.join(base_path, "sjn-translations.yaml")
source_json_path = os.path.join(base_path, "source.json")
destination_path = os.path.join(base_path, "sjn.json")
stats_path = os.path.join(base_path, "translation-stats.json")

with open(source_path) as f:
  source = yaml.safe_load(f)

with open(source_json_path, encoding="utf-8") as f:
  source_json = json.load(f)

destination = {}
for item in source["translations"]:
  destination[item["key"]] = item["sjn"]["tengwar"]

with open(destination_path, "w") as f:
  # ensure_ascii=True emits Tengwar PUA codepoints as \uXXXX escapes
  # for reviewability. Set to False if you ever need the literal-byte
  # form (e.g. piping into a font-aware preview).
  f.write(json.dumps(destination, ensure_ascii=True, indent=2) + '\n')

translation_stats = stats_module.compute(source, source_json)
with open(stats_path, "w") as f:
  f.write(json.dumps(translation_stats) + '\n')
