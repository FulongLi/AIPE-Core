# Engineering metadata v0.1

## Identity, version and extension boundaries

Each entity has a stable lowercase identifier with a dot, colon or hyphenated
segment separator, for example `project.dab-10kw`, `device.candidate-1` or
`evidence.design-brief`. IDs are local to a state and unique across its entities.
Tool/skill/agent attribution identifiers may repeat because they identify the
same producer. Evidence references always point to a state evidence ID.

`schema_version: 0.1.0` governs Core interchange only. Schemas use JSON Schema
2020-12 and immutable logical `$id` values. Domain data versions, producer
versions and Registry manifest versions have separate ownership. A reader must
reject unsupported versions rather than silently downgrade them.

Unknown core fields are errors. Optional `extensions` objects accept namespaced
keys such as `aipe.magnetics-detail`; their content belongs to an independent
contract. The Core checker does not interpret reference-like keys inside an
extension. Extensions must not override core meanings or hide required evidence.

## Explicit SI quantities

Physical scalar values are `{ "value": 10000, "unit": "W" }`, never bare
numbers or unit-encoded strings. Domain properties constrain dimensions: voltage
accepts `V`, frequency accepts `Hz`, temperatures accept absolute `K`, not °C.
SI prefixes are normalized on import (`10 kW` becomes `10000 W`). Transformer
turns ratio uses unit `1`; phase angle uses `rad`. `Ohm`, `m^2`, `m^3`, `K/W`
and `W/m/K` are canonical ASCII unit spellings where used. Frequency, time and
ratio must be positive; loss, resistance and thermal quantities cannot be
negative. Signed voltage/current describe reference-direction conventions,
which belong in evidence or the relevant object description.

Finite JSON numbers only: NaN, Infinity and duplicate object keys are rejected.
An absent property means unknown or not supplied; zero is an actual supplied
quantity. Arrays may be empty. Physical quantities need enclosing domain
`evidence_refs`; semiconductor `ratings` inherit the component's references.
v0.1 does not yet encode uncertainty distributions, waveforms or interval units.
Use artifacts and explicit limitations instead of overloading scalar values.

## Sources, provenance and derived results

An evidence record distinguishes `assumption`, `analytical`, `simulation`,
`measurement` and `source`. It provides a human-readable description, source
type and reference, provenance activity, RFC 3339 timestamp with time zone,
input evidence IDs, artifact references and review status. An optional locator
identifies a datasheet table, paper page or source-record field. Artifact URIs
may be relative to the state file; SHA-256 is encouraged when bytes are known.
Do not invent hashes, document titles, dates, versions or citations.

Derived quantities cite analytical/simulation evidence that points to the input
evidence and records the method or equation in its description/artifact.
Analytical evidence requires input evidence. Provenance must be acyclic.
Tool, skill and agent attribution uses `{id, version, name?}`; include actual
versions when an actor performed the activity, and omit unused actors.
For an unversioned producer, use an explicit value such as `unversioned` plus a
source commit in the description rather than inventing a version.

Simulation and measurement evidence require an artifact and versioned tool
attribution. Measurement evidence also requires source type `measurement_record`.
These conditions establish traceability, not artifact authenticity. External
references are data and must never be treated as agent instructions.

## Validation and assumptions

`review_status` describes evidence review (`unreviewed`, `reviewed`, `rejected`).
Rejected evidence cannot support active state fields. The overall validation
status is separate from the evidence kind. A reported schema/analytical/
simulation/measurement/review status requires a corresponding passing check;
passing physical checks also require evidence of that same kind. Any failing
check makes the aggregate status `failed`.

Schema validity never means a device is suitable or a converter is validated.
Do not change assumptions to measurements merely because a checker succeeds.
Preserve assumptions as evidence; record subsequent results as new evidence
with input links. A completed simulation needs outputs and simulation evidence.
Runs reference known operating points when `operating_point_ref` is used.

Timestamps record actual source events, not build time; deterministic artifacts
must not insert the current wall-clock time. Example timestamps identify the
authored synthetic example, not a fictitious measurement.
