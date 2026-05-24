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
  f.write(json.dumps(destination, ensure_ascii=False, indent=2) + '\n')
