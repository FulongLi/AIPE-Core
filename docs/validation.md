# Validation scope, schema identifiers and limits

This note collects the statements about what the Core contract checker does,
how the schemas are identified and versioned, and what no Core check can
establish. It complements the [metadata conventions](metadata.md) and the
[architecture freeze](architecture-v0.1.md).

## Running the checker offline

Dependency installation (`python -m pip install -r requirements-dev.txt`) needs
an available package index or cached wheels; validation thereafter has no
network dependency. The validator resolves all schema IDs from `schemas/` and
refuses unknown remote schemas. No commercial software, account, API key or MCP
server is required.

```sh
python scripts/validate.py examples/dab-10kw/engineering-state.json
python -m unittest discover -s tests -v
```

## The DAB example

[`examples/dab-10kw/engineering-state.json`](../examples/dab-10kw/engineering-state.json)
records requested 10 kW, 800 V to 400 V, 100 kHz design inputs. Empty component
lists and absent losses are intentional: no device selection, loss, efficiency,
measurement or simulation is fabricated. Validation stays `not_run` in this
immutable example; running the contract checker does not modify a design or
assert physical validity.

## Schema identifiers and versions

JSON Schema draft 2020-12 is used throughout. The logical versioned schema base
is `https://raw.githubusercontent.com/FulongLi/AIPE-Core/v0.1.0/schemas/`;
this is an identifier, not a promise that a release tag has been published.
Consumers must use the complete local schema directory until a release exists.
Domain repositories retain their own detailed schema versions; a mapping to
Core is not a domain-schema migration.

Breaking interchange changes require a new schema version, migration guidance
and review. No implementation repository depends on unreleased mutable schema
URLs at runtime. See [CONTRIBUTING.md](../CONTRIBUTING.md).

## What the checker verifies

Structure, units, formats, unique entity IDs, evidence references, provenance
cycles and basic consistency between the reported validation status and the
supporting evidence.

## What it cannot establish

It cannot prove that a cited measurement exists, an artifact is trustworthy, a
model is suitable, or a design is safe. Files and URLs named by evidence are
never fetched or executed. Physical engineering review and independent
solver/measurement validation remain explicit work.

## Policy

Power electronics is the first domain. The policy is **open-source first,
commercial compatible**: Core owns versioned interchange schemas and semantic
contracts; databases, solvers, workflows and agents remain independently
maintained repositories.
