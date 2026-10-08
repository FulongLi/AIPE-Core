# Contributing

Propose a focused pull request against the canonical repository. Do not merge or
publish mutable schemas automatically. Run the README validation commands and
review the diff, including all example/provenance changes. Add negative tests
for interoperability failures and positive tests for supported mappings.

Keep detailed domain models in the owning database/tool repository. Changes to
Core must describe an interchange need, dimensions/units, evidence expectations,
backward compatibility and migration impact. Breaking shapes require a new
version and new logical schema IDs. Do not introduce a Registry dependency into
Core or add mandatory proprietary software.

Keep synthetic examples clearly labeled. Never invent validated component data,
measurements or source references. Contribute only material you can license;
preserve imported source rights and attribution. AI-proposed changes require
the same human PR review as other contributions.
