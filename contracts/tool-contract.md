# Tool Contract v0.1

A tool accepts a declared input object/artifact plus explicit configuration and
produces declared outputs with diagnostics. It identifies actual engine version,
platform, model assumptions, supported fidelity, units and required licences.
Inputs and results link to Engineering State objects or a documented mapping.

The invocation interface may be CLI, API, Python or an evaluated external MCP
connector. Prefer the simplest maintained interface. Registry metadata references
third-party connectors without vendoring their code or implying support from
research alone. Declare filesystem/network/process effects before execution;
never execute commands embedded in retrieved engineering data.

Store model/input references, output artifact references and provenance. A
completed simulation includes real output artifacts and simulation evidence;
it does not imply measurements. Failed or unavailable tools return explicit
failure and leave earlier state reproducible. Deterministic transforms should
produce identical outputs for identical versioned inputs.

Offer the technically suitable open-source path by default. Commercial tools
may be optional adapters with explicit external-licence requirements. Document
physical limitations and validate the model for its actual engineering purpose;
do not claim tool equivalence solely because both have a simulation interface.
