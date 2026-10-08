# AIPE Ecosystem v0.1 architecture freeze

Frozen 2026-10-07 after inspecting all eleven canonical checkouts, repository
metadata, existing schemas/APIs, Academy instructions, and the existing awesome
list. AIPE means **AI for Power Engineering**; power electronics is the first
domain. This is the coordinator's shared implementation contract.

## Ownership and dependencies

| Repository | Role | Existing implementation to preserve |
| --- | --- | --- |
| AIPE-Core | standard | Empty; shared JSON Schema 2020-12 and semantic contracts only |
| AIPE-Registry | registry | Empty; manifest schema, read-only discovery, deterministic JSON/Markdown |
| AIPE-Semiconductor-Database | database | Python/Pydantic v3; raw XML, canonical records, evidence, exporters |
| AIPE-Magnetics-Database | database | README-only Rogowski_Coil identity; new evidence-first scaffold |
| AIPE-Simulation-Skills | skill_collection | Eight existing engineering skills and README generator |
| AIPE-Sketch | tool | Circuit IR, deterministic graph/geometry/SVG pipeline |
| AIPE-Design-Agent | agent | pea calculators, optimiser, UI and CLI; additive orchestration |
| AIPE-Academy | education | Seven existing stages, F00-F09 prerequisite path, tutor workflow |
| AIPE-IEEE-Paper-Agent | agent | Evidence-based paper engine, venue templates and release tools |
| Spirit-Connect-AIPE-Labs | presentation | Jekyll, bilingual posts, legacy redirects |
| awesome-open-source-power-electronics | catalogue | Community-curated external tools; remains separate from Registry |

Core has no runtime dependency on Registry or any implementation. Registry owns
manifest syntax and depends semantically on Core version identifiers. Registry
indexes canonical manifests, not every project from the awesome catalogue.
Implementations own their detailed schemas; Core describes portable interchange.
Website consumes generated Registry and Academy outputs at build time. No runtime
GitHub dependency for readers. No automatic repository rewrite or merge.

## Frozen manifest contract

Every participating repository has `aipe.yaml` (YAML 1.2 JSON-compatible values;
no custom tags). Version `0.1.0`. The sibling `manifest-template.json` gives exact
shapes. Registry owns `schema/capability-manifest.schema.json`.

- `id`: stable lowercase dotted identifier, e.g. `aipe.core`,
  `aipe.semiconductor-database`, `aipe.simulation-skills`.
- `type`: `standard`, `registry`, `database`, `tool`, `skill_collection`, `skill`,
  `agent`, `education`, `presentation`, `catalogue`.
- `repository`: canonical HTTPS GitHub URL, even when developed in a fork.
- `status`: `active`, `experimental`, `planned`, `deprecated`.
- `maturity`: `scaffold`, `prototype`, `usable`, `stable`.
- `license`: SPDX identifier/expression or `NOASSERTION` for unresolved rights.
  Do not assign an open licence to previously unlicensed assets. New Core/Registry
  code may propose MIT in their reviewable initialization changes.
- `inputs`, `outputs`: arrays of `{name, description, schema?}`. Schema is a URI;
  local implementation objects can be described without falsely claiming Core
  compatibility.
- `dependencies`: array of `{id, version, optional}`. `version` is `0.1.x` for
  v0.1 ecosystem dependencies; unknown IDs fail unless explicitly external (use
  tools/connectors instead for external software).
- `compatibility`: `{core: "0.1.x", engineering_state: "0.1.x",
  integration: "native"|"mapped"|"none"}`. Mapping documentation alone is
  `mapped`; do not claim executed interoperability without a tested adapter.
- `tools`: array of `{id, name, capabilities, licence_class, optional, interfaces,
  platforms, url, limitations}`. `licence_class` is `open_source`,
  `free_proprietary`, or `commercial`; `interfaces` and `platforms` are arrays
  of strings. All proprietary tools must be optional at repository level.
  Required proprietary skill variants must say so in skill-specific metadata.
- `connectors`: array of `{id, tool, type, repository, license, status,
  supported_versions, platforms, security_notes}`. `type` is `mcp`, `api`,
  `cli`, or `python`; `status` is `evaluated`, `experimental`, `supported`.
  A researched connector is not thereby supported or installed.
- `validation`: `{status: "not_run"|"schema_validated"|"tested"|"measured",
  evidence: [relative-path-or-URI], limitations: [string]}`. This describes the
  integration; physical validation must be recorded separately in evidence.
- `documentation`: array of repository-relative document paths or HTTPS URLs.
- `capabilities`: array of stable capability strings, e.g.
  `engineering-state-schema`, `switching-circuit-simulation`.
- Optional `extensions`: namespaced object for domain-specific metadata.

Registry output `generated/aipe.json` is `{schema_version: "0.1.0",
capabilities: [manifest objects sorted by id]}`. It contains no wall-clock build
time. `generated/aipe.md` is an agent-readable Markdown index. Source records in
`sources/repositories.yaml` identify canonical repository, immutable ref (or an
explicit pending PR ref during staging), path and ID. Local checkout discovery
must be supported for unmerged multi-repository validation. Validation errors
must not silently produce a partial successful index. Network activity is opt-in
for maintenance/link checks; deterministic builds use checked-in snapshots with
source provenance and a refresh command.

## Engineering State boundary

Core owns `schemas/engineering-state.schema.json`, project, requirements,
operating-point, converter, semiconductor, magnetics, control, thermal,
simulation, validation and evidence schemas, with shared quantity/provenance
definitions as needed. Schema `$id` base is
`https://raw.githubusercontent.com/FulongLi/AIPE-Core/v0.1.0/schemas/` (logical
version identifier; validators must resolve locally until a release exists).

State version is `0.1.0`. Top-level fields include `id`, `schema_version`,
`project`, `requirements`, `architecture`, `converter`, `semiconductors`,
`magnetics`, `passives`, `control`, `thermal`, `simulation`, `validation`,
`evidence`. Optional fields may stay unset/empty rather than invent facts.
Numbers carrying physical meaning use `{value: number, unit: SI-unit}`.
Domain versions remain independent (semiconductor v3 is not rewritten to v0.1).
Core author defines exact domain structures and publishes a tested synthetic
10 kW / 800 V / 400 V / 100 kHz DAB example before dependent adapters finalize.
No device choices, losses, efficiency or measurements are invented. Evidence
distinguishes assumption, analytical result, simulation and measurement, with
source, provenance, versions, timestamps and tool/skill/agent attribution.
Extensibility uses namespaced `extensions`, avoiding typo-tolerant core objects.

## Academy and public URL contract

Keep existing curriculum paths. Enrich actual lessons with YAML front matter
or a sidecar catalogue when document types do not support it. Required lesson
metadata: title, slug, domain, track, level, type, prerequisites,
learning_objectives, next, estimated_time (minutes), tools, status, references.
Use globally unique slugs (include locale suffix where needed); prerequisite and
next references resolve by slug. Publish a deterministic `generated/lessons.json`
with `schema_version` and `lessons` array; each lesson includes metadata and
`source` relative path. Stable URL `/academy/<domain>/<slug>/` is derived from
metadata. Website sync consumes this catalogue and copies vetted Markdown/assets
with attribution. Never execute source Liquid/includes from imported content
without an explicit supported conversion. Retain educational post URLs; classify
LEARN/RESEARCH/BUILD/NEWS and migrate one suitable LEARN source with provenance if
practical, maintaining a canonical URL/redirect without losing bilingual pages.

## Delivery and audit requirements

Each repository uses `codex/aipe-ecosystem-v0.1`, separate commits and PR. Do not
merge. Existing upstream branches remain untouched. Empty Core/Registry need an
initial baseline before a PR is possible: create a local empty baseline commit
on main and stage implementation on the feature branch; publishing that baseline
requires upstream write access (requested from user). Current account
MrCoconut616 has push only to AIPE-Design-Agent; use forks for populated repos.
Keep existing fork names/remotes; do not overwrite unrelated branches or commits.

Testing must prove schema negative cases, deterministic Registry generation,
manifest/dependency/reference validity, Academy prerequisites and rendering,
state adapter behaviour, and existing repository regression tests as applicable.
Do not claim installed solver/MCP execution when only interfaces were researched.
Preserve history, research data, commercial skills and copyright notices.
No AIPS migration, no deletion/archive, no third-party code vendoring.
