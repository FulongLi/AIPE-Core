# Skill Contract v0.1

A skill is an engineering workflow with a stable ID, purpose, domain, prerequisites,
input objects, output objects, supported tools and completion/acceptance criteria.
Declare Core/Engineering State versions, maturity, validation evidence, platforms,
preferred open tool, optional alternatives and connector status. A skill can
compose tools; it must not be only an undocumented sequence of UI clicks.

Before execution, validate required state and identify unknown assumptions,
fidelity requirements and installed tool availability. Do not fill missing
engineering inputs from guesses. If a calculation deliberately assumes a value,
record it as assumption evidence and surface its effect/limitations for review.

After execution, attach output artifacts and producer versions. Emit supported
state updates with input evidence references, acceptance checks and explicit
failure status. A design workflow that merely scaffolds files stays `scaffold`
or `prototype`; it cannot claim a solver or MCP ran when only its API was read.

Repository-wide commercial integrations remain optional. A specific professional
variant that requires a licence must say so in its own metadata. Open alternatives
are selected by capability and fidelity, with limitations documented.
