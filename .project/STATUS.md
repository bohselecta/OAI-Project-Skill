# Project skill release status
Contract revision: 1
Upstream baseline: 89141afdf32036b49240c1937f017c15d55fdf04
Delivery branch: codex/project-skill-v1
Pull request: https://github.com/bohselecta/OAI-Project-Skill/pull/1
State: source delivered for review; distribution/tooling locally verified

Completed: canonical skill, dated model policy, progressive references, reversible offline tooling, portable skills-only manifest, self-install directive, host-evaluation fixtures, maintenance/security/contribution guidance, and cross-platform CI.
Evidence: 58 deterministic tests PASS, zero skipped, Python 3.13.5/Linux. Package validation, independent YAML parsing, deterministic archive, sandbox installation/status/uninstall and diff checks PASS. Exact tested file hashes and limitations: docs/local-validation.json and docs/VALIDATION.md.
Remote evidence: PR #1 checks are authoritative for each commit. The first Linux/macOS runs passed; a Windows fixture's double newline translation was corrected with a strict negative control. Do not treat an earlier successful job as evidence for a later changed revision.
Not run: authenticated native Codex/ChatGPT discovery, manual host switching, plugin import, actual model behavioral trials. No broad efficacy or native certification claim is made.
Next: inspect the PR's final checks, then use INSTALL.md in an authenticated Codex client for installation/discovery and evals/README.md for the first native trial. Main is preserved for review.

Repository visibility is unchanged. No directory registration, global settings changes, user-machine installation, paid evaluation, or external outreach was performed.
