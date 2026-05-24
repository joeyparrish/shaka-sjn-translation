# Applying the translation schema to sjn-translations.yaml

The general schema lives in `elvish-translation-tools/references/translation-schema.md`
(sibling repo). This document covers what's specific to this project:
which fields the build pipeline requires, and how to migrate the
existing flat file to the structured form.

## What the build pipeline requires

`sync-sjn.py` reads `sjn-translations.yaml` and writes `sjn.json`. The
only field it consumes is the Tengwar-encoded form per key. Under the
schema, that is `sjn.tengwar`.

`sync-sjn.py` needs a one-line change to match:

```python
# Before:
destination[item["key"]] = item["sjn"]

# After:
destination[item["key"]] = item["sjn"]["tengwar"]
```

Everything else in each entry (`sjn.roman`, `sjn.literal`, `elements`,
`composition`, `status`, `concerns`, `history`) is for human use and
ignored by the build.

## Migration from the current shape

The current YAML uses flat fields per entry:

```yaml
- key: PLAY
  english: "Play"
  sjn-literal: "make-run"
  sjn-roman: "northo"
  sjn: ""           # Tengwar form
```

The schema moves the translation fields under a `sjn` map and adds
provenance:

```yaml
- key: PLAY
  english: "Play"
  sjn:
    roman: "northo"
    literal: "make-run"
    tengwar: ""
  elements: [...]    # added incrementally
  status: ...
```

The migration can run in two phases:

1. **Mechanical**: lift the three existing fields into the `sjn` map.
   Renames only:
   - `sjn-roman`  -> `sjn.roman`
   - `sjn-literal` -> `sjn.literal`
   - `sjn` -> `sjn.tengwar`
   Update `sync-sjn.py` in the same commit. All entries still build.
2. **Provenance backfill**: add `elements`, `status`, etc., per entry,
   as part of normal review work (or driven by the skill when invoked).
   This can be done incrementally; entries without `elements` are valid
   under the schema, just less documented.

## Project-specific decisions

- **Placeholder strings**: when a `source.json` key is new and the
  Sindarin translation doesn't exist yet, use `status: placeholder`
  and leave `sjn.roman` / `sjn.tengwar` empty. The build will produce
  an empty string for that key; we should decide whether shaka-player
  falls back to English in that case or whether the build should warn.
- **Recurring lexemes from `glossary.md`**: when filling out `elements`
  for a new entry, prefer the recurring vocabulary already established
  by the original translator (`fanwos`, `northo`, `hastië an mirian`,
  etc.) unless a `glossary.md` entry has been explicitly flagged for
  revision. Consistency across entries beats local optimization.
- **Untranslated keys in `source.json`**: when `source.json` adds new
  keys (the common case after a shaka-player upgrade), detect them by
  diffing the key sets, then create `placeholder` entries to track
  what needs work.

## Status field interpretations for this project

The general schema status values apply directly. Notes on how they map
to this project's reality:

- `attested` / `attested-components` -- straightforward.
- `defensible-neo-sindarin` -- use for the many derived imperatives
  (`northo`, `adnortho`, `uthro`, `cabo`) where the root is attested
  but the surface form is a regular paradigm extension.
- `coinage` -- the signature inventions of this translation, like
  `hastië an mirian` for "ad" or `cîrwain` for "live". Worth keeping
  but worth flagging.
- `needs-revision` -- the cases identified in `translator-intent.md`
  as wrong (e.g. `hasto`, `neth`, `enquet-`, `bir`, `abont`, `meiras`,
  `la`).
- `placeholder` -- new English strings awaiting translation.
