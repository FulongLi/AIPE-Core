# AIPE Core

**AI for Power Engineering** starts with a shared engineering language.
Core owns versioned interchange schemas and semantic contracts; databases,
solvers, workflows and agents remain independently maintained repositories.
Power electronics is the first domain. The policy is **open-source first,
commercial compatible**.

## Start offline

Use Python 3.10 or newer and the open-source JSON Schema validator:

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate.py examples/dab-10kw/engineering-state.json
python -m unittest discover -s tests -v
```

Dependency installation needs an available package index or cached wheels;
validation thereafter has no network dependency. The validator resolves all
schema IDs from `schemas/` and refuses unknown remote schemas. No commercial
software, account, API key or MCP server is required.

The [DAB example](examples/dab-10kw/engineering-state.json) records requested
10 kW, 800 V to 400 V, 100 kHz design inputs. Empty component lists and absent
losses are intentional: no device selection, loss, efficiency, measurement or
simulation is fabricated. Validation stays `not_run` in this immutable example;
running the contract checker does not modify a design or assert physical validity.

## Contract surface

- [Engineering State schema](schemas/engineering-state.schema.json): project,
  requirements, architecture, converter, semiconductors, magnetics, passives,
  control, thermal, simulation, validation and evidence.
- [Metadata and SI conventions](docs/metadata.md): identifiers, typed quantities,
  evidence, provenance, timestamps, attribution and extensions.
- [Database, Tool, Skill and Agent contracts](contracts/README.md).
- [Frozen v0.1 ecosystem architecture](docs/architecture-v0.1.md) and
  [repository audit](docs/ecosystem-audit.json).
- [Repository capability manifest](aipe.yaml), indexed by AIPE-Registry.

JSON Schema draft 2020-12 is used throughout. The logical versioned schema base
is `https://raw.githubusercontent.com/FulongLi/AIPE-Core/v0.1.0/schemas/`;
this is an identifier, not a promise that a release tag has been published.
Consumers must use the complete local schema directory until a release exists.
Domain repositories retain their own detailed schema versions; a mapping to
Core is not a domain-schema migration.

## Scope and limits

The checker verifies structure, units, formats, unique entity IDs, evidence
references, provenance cycles and basic consistency between reported validation
status and supporting evidence. It cannot prove that a cited measurement exists,
an artifact is trustworthy, a model is suitable, or a design is safe. Files and
URLs named by evidence are never fetched or executed. Physical engineering review
and independent solver/measurement validation remain explicit work.

Breaking interchange changes require a new schema version, migration guidance
and review. No implementation repository depends on unreleased mutable schema
URLs at runtime. See [CONTRIBUTING](CONTRIBUTING.md).
