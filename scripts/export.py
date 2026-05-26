#!/usr/bin/env python3
#
# Copyright 2026 Joey Parrish
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
import yaml

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source_path = os.path.join(base_path, "sjn-translations.yaml")
destination_path = os.path.join(base_path, "sjn.json")

with open(source_path) as f:
  source = yaml.safe_load(f)

destination = {}
for item in source["translations"]:
  destination[item["key"]] = item["sjn"]["tengwar"]

with open(destination_path, "w") as f:
  # ensure_ascii=True emits Tengwar PUA codepoints as \uXXXX escapes
  # for reviewability. Set to False if you ever need the literal-byte
  # form (e.g. piping into a font-aware preview).
  f.write(json.dumps(destination, ensure_ascii=True, indent=2) + '\n')
