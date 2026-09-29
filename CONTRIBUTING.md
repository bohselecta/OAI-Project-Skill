# Contributing

Start with [AGENTS.md](AGENTS.md), the [release contract](.project/PROJECT-CONTRACT.md), and [maintenance guide](docs/MAINTENANCE.md). Keep one canonical skill, use progressive disclosure, preserve authorization boundaries, and make changes on a reviewable branch.

Include the problem, the smallest change, affected scenarios, exact checks, and what was not tested in your PR. Add a regression test for tooling defects and host evidence for behavioral claims. Existing assertions can change only with independent evidence of an incorrect test and replacement coverage. Never submit private user data, credentials, or a claim of a model run that did not occur.

For intentional skill changes, review the files before `python3 scripts/project_tool.py seal`, then run validation and tests. The seal command updates an integrity inventory; it does not certify safety. Update source/date provenance and the changelog for model-policy changes. Contributions are offered under this repository's MIT license; do not copy material you cannot redistribute.
