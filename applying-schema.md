# Applying the translation schema to sjn-translations.yaml

The general schema lives in `elvish-translation-tools/references/translation-schema.md`
(sibling repo). This document covers what's specific to this project:
which fields the build pipeline requires, and how to migrate the
existing flat file to the structured form.

## What the build pipeline requires

`scripts/export.py` reads `sjn-translations.yaml` and writes `sjn.json`.
The only field it consumes is the Tengwar-encoded form per key, at
`sjn.tengwar`.

Everything else in each entry (`sjn.roman`, `sjn.literal`, `elements`,
`composition`, `status`, `concerns`, `history`) is for human use and
ignored by the build.

## Tengwar encoding: escape sequences end-to-end

The Tengwar CSUR codepoints (U+E000-U+E0AE) are stored as `\uXXXX`
escape sequences in both `sjn-translations.yaml` and the generated
`sjn.json`, not as literal PUA characters:

```yaml
sjn:
  tengwar: ""
```

```json
"PLAY": ""
```

YAML and JSON both decode these escapes to the same in-memory string
the consumer would see if literal characters were stored. The escape
form is reviewable in any editor (GitHub diff view, plain terminals,
file pickers) and diff-friendly. It also survives tools that might
silently corrupt PUA characters.

To produce escape-encoded Tengwar, use
`elvish-translation-tools/scripts/transliterate.py` (escape is the
default output). To preview the Tengwar in a font-aware terminal,
pipe through `elvish-translation-tools/scripts/preview.py`.

`export.py` uses `json.dumps(..., ensure_ascii=True)` to keep the
escape form through the build. If you ever need raw bytes for testing
in a font-aware tool, flip to `ensure_ascii=False`.

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

The migration ran in two phases:

1. **Mechanical** (done): lifted the three existing fields into the
   `sjn` map. `sync-sjn.py` was renamed to `scripts/export.py` and
   updated to read `item["sjn"]["tengwar"]`. All entries still build.
2. **Provenance backfill** (in progress): adding `elements`, `status`,
   etc., per entry as part of revision and translation work. Entries
   without `elements` are valid under the schema, just less documented.

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
