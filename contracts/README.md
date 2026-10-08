# AIPE semantic contracts

These contracts define interoperable behavior, not mandatory HTTP endpoints or
network protocols. A Python function, local CLI, file exchange or reviewed agent
workflow may implement them. Repository `aipe.yaml` describes discovery; Core
describes the engineering objects exchanged.

| Capability type | Contract | Responsibility |
| --- | --- | --- |
| Database | [database-contract.md](database-contract.md) | Evidence-backed data and explicit mappings |
| Tool | [tool-contract.md](tool-contract.md) | Bounded computation or artifact generation |
| Skill | [skill-contract.md](skill-contract.md) | Domain workflow with acceptance criteria |
| Agent | [agent-contract.md](agent-contract.md) | Capability selection, orchestration and review |

All capabilities declare accepted versions, input/output schemas, units,
required software and limitations. Failure is explicit; incomplete output is
never reported as a complete valid result. Producers retain assumptions and
attribute actual tools/skills/agents. Consumers validate before use. Contract
validation does not establish physical adequacy or authorize external execution.

An integration can be `mapped` when mapping documents exist; `native` claims
require a tested compatible input/output path. Detailed implementation schemas
remain in the owning repositories. Never silently reinterpret domain schema
versions as Core versions.
