# Validation evidence

## Current public preview — 1.2.0, 2026-09-30

The release-readiness suite covers both host distributions, integrity, reversible Codex
installation, portable Claude copies, drift rejection, deterministic release ZIPs/checksums,
and exact public metadata. Run the complete [release checks](RELEASE.md) against your pinned
revision. CI runs on Linux, macOS and Windows; use the exact commit's checks in
[GitHub Actions](https://github.com/bohselecta/OAI-Project-Skill/actions), not historical hashes below.

The Claude adapter's original commit `ce9e609111c0664423337bad5c63babcab85c63b`
passed 67 Python and 47 Node tests locally, an independent read-only review, and the complete
[PR #3 CI matrix](https://github.com/bohselecta/OAI-Project-Skill/pull/3/checks).
Release-readiness local checks passed **72 Python tests and 47 Node tests**, with no skips,
on Python 3.12.14 / Node 24.19.0 / Linux. Both ZIPs were built twice identically, extracted
and validated; all 92 relative Markdown links resolved. Official installation/model guidance
links were reachable. A limited pattern review of current files and available history found
no credential matches; this is not an exhaustive security audit. Exact final CI remains
revision-specific and is linked from the release-readiness PR.

**NOT_RUN:** authenticated Codex/Claude discovery, real model selection/switch/resume,
model-backed behavioral comparisons, and marketplace acceptance. No native certification,
cost/quality improvement, or broad production-readiness claim is made. The historical
records below retain their original scope and do not substitute for current validation.

## Historical local checks — 2026-09-29

**58 deterministic tests passed, zero skipped**, on Python 3.13.5 / Linux x86_64. The run exercised package integrity/metadata, preservation of user configuration, install/idempotence/upgrade, uninstall/restore, injected rename-failure recovery, conflict/symlink rejection, deterministic archive/extraction, CLI scope handling, repository consistency, and fixture-checker positive and negative controls.

Executed commands:

```text
python3 scripts/project_tool.py validate
python3 -m unittest discover -s tests -v
python3 scripts/project_tool.py pack --out /mnt/data/project-skill-1.0.0.zip
python3 scripts/project_tool.py install --skills-dir /mnt/data/project-install-check/.agents/skills
python3 scripts/project_tool.py status --skills-dir /mnt/data/project-install-check/.agents/skills
python3 scripts/project_tool.py uninstall --skills-dir /mnt/data/project-install-check/.agents/skills
git diff --check
```

Independent PyYAML parsing also succeeded for skill frontmatter, UI metadata, and the CI workflow. PyYAML is not a runtime dependency of the distributed tooling. The built-in validator intentionally checks this repository's restricted metadata format rather than arbitrary YAML.

[local-validation.json](local-validation.json) records the tested executable source SHA-256 values and environment. The canonical skill has 87 lines / 1,487 body words; its nine content files plus manifest form the standalone package.

```text
Skill manifest SHA-256:
44e8f95f8ba4485ba9a4b3b568a5465c7e72868240f1557f9d2e37573b7cf0ac
Standalone ZIP SHA-256:
683c9b72464e525eb55a0787fed39de6d2a1f8ec967c1aeba7f2910b34787864
```

The smoke installation above was in the build sandbox, **not the user's home directory or computer**. The fixture checker was tested against handwritten implementations and deliberately broken controls, not a Codex-generated trial.

## Native-host and outcome evidence

**NOT_RUN:** native Codex skill selection, natural `Project:` matching, manual model switching/resume in a real client, ChatGPT/plugin import, and real LLM behavioral trials. No authenticated Codex executable was available in this build environment. The portable plugin manifest has local consistency checks, not a certified native import.

No model/API cost, speedup, quality improvement over a baseline, or general project success rate has been measured. Review was performed in the same assistant session, not by an independent model or human. The [two executable fixtures and 18 scenarios](../evals/README.md) are ready for these further trials.

## Remote CI

The workflow defines Python 3.10 and 3.13 on Linux, plus Python 3.13 on macOS and Windows, with read-only repository permissions and pinned GitHub action revisions. Remote results belong to the exact PR commit and are not inferred from the local test run. That historical result is recorded in [PR #1 checks](https://github.com/bohselecta/OAI-Project-Skill/pull/1/checks), not inferred or cached in this file.

The initial run at `6456e8b4cbd585379f499410fa98675aaca5319b` passed Linux and macOS but exposed one Windows test-fixture defect: the fixture explicitly wrote CRLF through a text stream, which Windows translated again. The correction emits explicit bytes and adds a negative control that rejects malformed double-CRLF. No production-output assertion was relaxed. The CI actions were also moved from deprecated runtime versions to verified, SHA-pinned checkout v7.0.1 and setup-python v7.0.0. See the succeeding commit and its complete matrix for verification.
