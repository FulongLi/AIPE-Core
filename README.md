# AIPE — Core

AIPE Core is the shared engineering language of **AI for Power Engineering**:
versioned JSON Schema 2020-12 interchange schemas for a portable Engineering
State, SI quantity and evidence conventions, and the semantic contracts that
databases, tools, skills and agents implement. Power electronics is the first
domain. Core contains no solver, database or agent code; those live in their
own AIPE repositories and declare their capabilities to
[AIPE-Registry](https://github.com/FulongLi/AIPE-Registry).

## Features

- Engineering State schema covering project, requirements, architecture,
  converter, semiconductors, magnetics, passives, control, thermal, simulation,
  validation and evidence
- Metadata conventions for identifiers, typed SI quantities, evidence,
  provenance, timestamps and attribution
- Database, Tool, Skill and Agent semantic contracts that describe behaviour,
  not network protocols
- Offline contract checker that resolves every schema from `schemas/` and
  refuses unknown remote schemas
- Synthetic 10 kW dual-active-bridge example with no fabricated results
- Frozen v0.1 ecosystem architecture and repository audit

## Installation

Python 3.10 or newer. The only dependency is the open-source JSON Schema
validator; after installation nothing needs a network connection, account,
API key or commercial software.

```sh
python -m pip install -r requirements-dev.txt
```

## Usage

Validate an Engineering State document and run the contract tests:

```sh
python scripts/validate.py examples/dab-10kw/engineering-state.json
python -m unittest discover -s tests -v
```

The checker verifies structure, units, formats, unique entity IDs, evidence
references, provenance cycles and the consistency between a reported validation
status and its evidence. It does not prove that a measurement exists, that a
model is suitable or that a design is safe; see
[docs/validation.md](docs/validation.md).

## Project Information

- Version: 0.1.0 (proposed, unreleased; no release tag has been published —
  see [CHANGELOG.md](CHANGELOG.md))
- Status: Prototype (`aipe.yaml`: status `experimental`, maturity `prototype`)
- Developer: Fulong Li
- Organisation: Spirit Connect / AIPE Labs
- License: MIT ([LICENSE](LICENSE))

## Documentation

- [Engineering State schema](schemas/engineering-state.schema.json) and the
  domain schemas in `schemas/`
- [Metadata and SI conventions](docs/metadata.md)
- [Database, Tool, Skill and Agent contracts](contracts/README.md)
- [Validation scope, schema identifiers and limits](docs/validation.md)
- [Ecosystem architecture v0.1](docs/architecture-v0.1.md) and
  [repository audit](docs/ecosystem-audit.json)
- [Capability manifest](aipe.yaml) indexed by AIPE-Registry
- [CHANGELOG.md](CHANGELOG.md) · [CONTRIBUTING.md](CONTRIBUTING.md)
