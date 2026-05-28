#!/usr/bin/env python3
# Shaka Player Sindarin (Elvish) Translations
# Copyright 2026 Joey Parrish
# SPDX-License-Identifier: Apache-2.0

"""Import source.json from upstream shaka-player.

Fetches the latest English UI strings from the shaka-player main branch
and writes them to source.json in the project root. Also writes
source-meta.json with the SHA and committer date of the upstream commit.
Prints a brief diff summary (added / removed / changed keys) so it's
obvious whether the sjn translations need updating.
"""

import json
import os
import sys
import urllib.request

COMMITS_API_URL = (
    "https://api.github.com/repos/shaka-project/shaka-player/commits"
    "?path=ui/locales/source.json&per_page=1")
RAW_URL_TEMPLATE = (
    "https://raw.githubusercontent.com/shaka-project/shaka-player"
    "/{sha}/ui/locales/source.json")

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
destination_path = os.path.join(base_path, "source.json")
meta_path = os.path.join(base_path, "source-meta.json")


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
  print(f"Fetching commit metadata from GitHub API ...", file=sys.stderr)
  req = urllib.request.Request(
      COMMITS_API_URL,
      headers={"User-Agent": "shaka-sjn-translation-import",
               "Accept": "application/vnd.github.v3+json"})
  with urllib.request.urlopen(req) as r:
    commits = json.loads(r.read())
  commit = commits[0]
  sha = commit["sha"]
  date = commit["commit"]["committer"]["date"]

  raw_url = RAW_URL_TEMPLATE.format(sha=sha)
  print(f"Fetching {raw_url} ...", file=sys.stderr)
  before = load_json_safe(destination_path)
  with urllib.request.urlopen(raw_url) as r:
    raw = r.read()
  # Verify it parses as JSON before writing.
  after = json.loads(raw)
  with open(destination_path, "wb") as f:
    f.write(raw)
  print(f"Wrote {len(raw)} bytes to {destination_path}", file=sys.stderr)

  meta = {"sha": sha, "date": date}
  with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(meta, f)
    f.write("\n")
  print(f"Wrote metadata to {meta_path} (sha={sha[:7]}, date={date})",
        file=sys.stderr)

  print(summarize_diff(before, after), file=sys.stderr)


if __name__ == "__main__":
  main()
