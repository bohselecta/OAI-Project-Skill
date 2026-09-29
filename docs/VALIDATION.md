# Validation evidence

## Local checks — 2026-09-29

**57 deterministic tests passed, zero skipped**, on Python 3.13.5 / Linux x86_64. The run exercised package integrity/metadata, preservation of user configuration, install/idempotence/upgrade, uninstall/restore, injected rename-failure recovery, conflict/symlink rejection, deterministic archive/extraction, CLI scope handling, repository consistency, and fixture-checker positive and negative controls.

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

The workflow defines Python 3.10 and 3.13 on Linux, plus Python 3.13 on macOS and Windows, with read-only repository permissions and pinned GitHub action revisions. Remote results belong to the exact PR commit and are not inferred from the local test run. At preparation of this record, remote execution is pending; inspect the PR's checks for its current status.
