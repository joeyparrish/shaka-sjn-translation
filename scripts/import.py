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

"""Import source.json from upstream shaka-player.

Fetches the latest English UI strings from the shaka-player main branch
and writes them to source.json in the project root. Prints a brief diff
summary (added / removed / changed keys) so it's obvious whether the
sjn translations need updating.
"""

import json
import os
import sys
import urllib.request

URL = ("https://raw.githubusercontent.com/shaka-project/shaka-player/"
       "refs/heads/main/ui/locales/source.json")

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
destination_path = os.path.join(base_path, "source.json")


def load_json_safe(path):
  if not os.path.exists(path):
    return None
  with open(path, encoding="utf-8") as f:
    return json.load(f)


def summarize_diff(before, after):
  if before is None:
    return f"first import: {len(after)} keys."
  before_keys = set(before)
  after_keys = set(after)
  added = sorted(after_keys - before_keys)
  removed = sorted(before_keys - after_keys)
  changed = sorted(
      k for k in (before_keys & after_keys) if before[k] != after[k])
  parts = []
  if added:
    parts.append(f"added ({len(added)}): {', '.join(added)}")
  if removed:
    parts.append(f"removed ({len(removed)}): {', '.join(removed)}")
  if changed:
    parts.append(f"changed ({len(changed)}): {', '.join(changed)}")
  if not parts:
    return "no changes."
  return "\n  ".join(parts)


def main():
  print(f"Fetching {URL} ...", file=sys.stderr)
  before = load_json_safe(destination_path)
  with urllib.request.urlopen(URL) as r:
    raw = r.read()
  # Verify it parses as JSON before writing.
  after = json.loads(raw)
  with open(destination_path, "wb") as f:
    f.write(raw)
  print(f"Wrote {len(raw)} bytes to {destination_path}", file=sys.stderr)
  print(summarize_diff(before, after), file=sys.stderr)


if __name__ == "__main__":
  main()
