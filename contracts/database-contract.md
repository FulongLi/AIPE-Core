# Database Contract v0.1

A database owns canonical records and their domain schema. It accepts documented
queries/identifiers or import formats and returns records or explicitly missing
data. It declares source rights, record version, source/locator, provenance,
operating conditions and review/validation status. Raw, canonical and derived
records remain distinguishable; derived values retain links to inputs/methods.

Publish a mapping to the relevant Core object and evidence records. Convert
physical values to explicit SI quantities; identify any unrepresentable fields
through documented namespaced extensions or leave them in a referenced domain
record. State `database_ref` resolves to a versioned record, not an unexplained
part number. Do not fabricate missing ratings, materials, losses or measurements.

An adapter declares accepted domain versions, Core version, conversion rules and
unsupported/missing data behavior. Tests must exercise both a real supported
shape and invalid/ambiguous input. An evidence source without known rights may
be referenced but must not be silently relicensed or redistributed.

On errors, return diagnostic context and no successful partial state. Read-only
queries do not mutate canonical records. Imports/curation changes are reviewed
separately and must retain original source provenance.
