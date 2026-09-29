# Project skill release status
Contract revision: 1
Upstream baseline: 89141afdf32036b49240c1937f017c15d55fdf04
Delivery branch: codex/project-skill-v1
Phase: local verification complete; remote delivery/checks pending

Completed: canonical skill, model policy, references, reversible offline tooling, portable skills-only manifest, self-install instructions, evaluation fixtures, maintenance/security/contribution guidance, and CI configuration.
Evidence: 57 deterministic tests PASS, zero skipped, Python 3.13.5/Linux. Package validation, separate YAML parsing, deterministic archive, sandbox installation/status/uninstall and diff whitespace checks PASS. Exact file hashes and limitations: docs/local-validation.json and docs/VALIDATION.md.
Not run: authenticated native Codex/ChatGPT discovery, manual host switching, plugin import, actual model behavioral trials. These prevent any claim of broadly tested model efficacy or native-host certification, not delivery of the tested distribution tooling.
Next: publish source on the reviewable branch, open a PR, and inspect remote checks. Then use INSTALL.md in an authenticated Codex client for the first native installation/discovery trial.

Repository visibility is unchanged. No directory registration, global settings changes, user-machine installation, paid evaluation, or external outreach was performed.
