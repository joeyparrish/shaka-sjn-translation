# Shaka Player Sindarin (sjn) Translation

Maintenance workspace for the Sindarin (Elvish) translation of the
Shaka Player UI.

## Files

- `source.json` -- the English source strings that need translating.
  Snapshot of `ui/locales/source.json` from the shaka-player repo.
- `sjn-translations.yaml` -- the working file. Romanized Sindarin plus
  Tengwar-encoded forms plus literal back-translations.
- `sync-sjn.py` -- generates `sjn.json` from the YAML.
- `sjn.json` -- generated output. The actual locale file shaka-player
  consumes.

## Analysis docs

- `glossary.md` -- every vocabulary choice in the YAML with attestation
  status (attested / Neo-Sindarin / Quenya / coined / etc.) checked
  against Eldamo.
- `translator-intent.md` -- inferred reasoning behind each translation
  choice, including defenses of entries that look wrong on the surface
  but are grammatically derivable from attested roots.
- `applying-schema.md` -- how this project applies the general
  translation schema (defined in the framework repo's
  `references/translation-schema.md`): which fields the build pipeline
  requires, the migration plan from the current flat YAML, and
  project-specific decisions.

## Status

The sjn locale has been dropped from shaka-player's main branch as
unmaintained. This workspace exists to bring it back up to current
strings, restore it to maintainable shape, and then re-introduce it
upstream.

## Related

The general Sindarin/Quenya translation framework lives in the sibling
repo `elvish-translation-tools/` (Eldamo extracts, grammar references,
mutation tables, lookup tools).
