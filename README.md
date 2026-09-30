> Optional native SayFrame handoff/plugin candidate: [installation and operating limits](docs/NATIVE-SAYFRAME.md). This is not a published directory listing; native-host acceptance remains NOT_RUN. The standalone Project workflow stays available.

# Project
### Say what to build. Let the agent own the development loop.

**Contract Freeze + Model Cadence Valve**, packaged as a reusable skill for Codex, compatible skill-enabled OpenAI environments, and [Claude Code](docs/CLAUDE-CODE.md).

```text
Project: build a local-first research notebook with Markdown export.
Project: implement ./PRODUCT-SPEC.md end-to-end.
Project: finish this repository against its existing acceptance criteria.
```

**Version:** 1.2.0 public preview · **License:** MIT · **Status:** offline tests and cross-platform CI; native-host behavioral evaluation pending. See [validation evidence](docs/VALIDATION.md).

Project is a community project by Hayden Lindley, not an official OpenAI or Anthropic product. It requires an agent with suitable tools and permissions. It is not a hosted service, model router, or guarantee that any specification can be completed without an external decision.

## Why Project

The agent turns intent into a concise contract, proves the core interaction, builds through verified vertical slices, and checks the result against the contract—not merely against its own implementation. The contract protects the meaning of the product; recorded evidence can still correct it.

Model effort follows uncertainty and consequence. Use strong reasoning where mistakes propagate, a capable builder for known work, and a lighter model only when useful. The agent checkpoints before a meaningful manual switch; you switch and reply **proceed**. It does not ask you to supervise routine development or stop after a passing build.

The workflow scales down for small changes. It preserves existing systems and user work, loads detailed guidance only when needed, distinguishes genuine integration from simulations, and keeps permissions and cancellation intact.

## Requirements

Use Codex, Claude Code, or a compatible skill-capable client with filesystem and execution access for software construction. Model availability, tools, and approval controls depend on the host and account. A local skill does not automatically install into ChatGPT web.

The optional installer, validator, and fixture runner require **Python 3.10+**, with no third-party packages. The core skill is Markdown and JSON/YAML; it needs no daemon, MCP server, API key, hooks, or runtime dependency of its own. On Windows use `python` where `python3` is unavailable. Use a real, non-symlinked checkout/destination with this installer.

## Install once

### Let Codex perform the installation

Open a trusted checkout of this repository in Codex and paste:

> Read INSTALL.md and install Project for this user. Inspect the package and existing destination first; run the validation and tests; use the reversible installer. Preserve any existing skill and do not change global instructions, model configuration, permissions, or services. Verify native skill discovery when the host allows it; distinguish that from file validation.

[INSTALL.md](INSTALL.md) contains the complete self-install directive, including recovery for an existing installation.

### Or install from the terminal

After reviewing a trusted, pinned revision of this repository:

```bash
python3 scripts/project_tool.py validate
python3 -m unittest discover -s tests -v
python3 scripts/project_tool.py install --dry-run
python3 scripts/project_tool.py install
python3 scripts/project_tool.py status
```

The default user location is **`~/.agents/skills/project`**. For one repository instead:

```bash
python3 scripts/project_tool.py install --repo /absolute/path/to/your-repo
```

Do not install both scopes unnecessarily. The installer refuses conflicting unmanaged directories and linked paths. It never edits `AGENTS.md`, `config.toml`, permissions, or user settings. `status` verifies bytes and metadata, not whether a running client has loaded the skill. See the current [OpenAI skill guide](https://developers.openai.com/codex/skills/) for host discovery and invocation; restart the client if it has not detected the new skill.

## Claude Code

The Claude-native package is [`.claude/skills/project`](.claude/skills/project/SKILL.md).
Copy the whole folder to your product repository's `.claude/skills/project/`, or to
`~/.claude/skills/project/` for personal use, then invoke **`/project build …`**.
Follow the [Claude Code installation, cadence, and validation guide](docs/CLAUDE-CODE.md)
to preserve existing copies and verify discovery. The Codex installer above remains unchanged.

This adapter keeps the same Contract Freeze and evidence-backed delivery loop, uses
Claude model guidance, and supports verified SayFrame file bundles. Native Codex launch
links are not Claude launchers. Offline package tests pass; authenticated Claude host
behavior remains **NOT_RUN**.

## Use

In Codex, **`$project build …`** explicitly selects the skill. **`Project: build …`** relies on the skill's natural-language matching; it is not a registered command. Quoting the phrase in an explanation should not trigger a build. A plugin-enabled ChatGPT surface may expose an `@` selector instead; availability must be checked there.

Give Project the actual specification or readable source, not an inaccessible filename. It reads the relevant repository instructions and preserves authoritative existing documents rather than replacing them with a new system.

For substantial work, the usual records are:

```text
.project/PROJECT-CONTRACT.md  stable meaning and acceptance IDs
.project/STATUS.md            current state, evidence, next slice, checkpoint
.project/DECISIONS.md         only material amendments, when needed
```

Small changes do not require this full file set. A model-switch request is concise, names a supported choice, and points at a checkpoint. `proceed` resumes that work; it never grants new spending, disclosure, or production permissions. Credential setup, genuinely consequential choices, and host approvals remain possible exceptions to the otherwise hands-off workflow.

## SayFrame front end

**Develop the complete proposal in SayFrame; build the accepted revision with Project.**
The [SayFrame connector](integrations/sayframe/README.md) preserves Purpose / Design / Approach,
including functional architecture, invariants, acceptance and explicit execution limits. It
exports exact accepted language rather than a transcript or shortened implementation prompt.

Discovery: [sayframe.connector.json](sayframe.connector.json). Existing-app implementation:
[Antigravity directive](integrations/sayframe/ANTIGRAVITY.md). Installed consumer:
[SayFrame intake](skills/project/references/sayframe.md). Actual evidence and remaining host
checks: [connector status](integrations/sayframe/STATUS.md).

The optional connector SDK/CLI requires a modern browser or Node 22+, respectively; ordinary
Project use and the Python installer remain unchanged. It does not launch Codex, grant new
permissions or upload project content. Both the connector and Claude Code adapter are on
`main`; pin a reviewed commit for installation. Native-host trials remain pending.

## Updates, recovery, and extension

Review changes and validate before updating an installed version:

```bash
python3 scripts/project_tool.py install --replace
python3 scripts/project_tool.py uninstall
python3 scripts/project_tool.py restore --backup /absolute/path/from-the-command-output
```

Use the same scope flag as installation on every command. `--replace` preserves the current managed installation under the sibling `project-backups` directory, outside skill discovery. Uninstall also moves to backup; it does not delete your copy. Restore requires `--replace` when a current installation exists. Locally modified/corrupt backups are preserved but must be inspected and reconciled before strict restoration.

The core workflow is model-independent. The dated [model policy](skills/project/references/model-policy.json) can evolve without rewriting it. As verified in official documentation on **2026-09-29**, the candidates are GPT-6 Astra for reasoning, GPT-6.1 Sol for building, and GPT-6 Luna for bounded transformations. These are advisory roles, not verified performance results or required entitlements. See [sources](docs/SOURCES.md), [maintenance](docs/MAINTENANCE.md), and [host evaluations](evals/README.md).

To make a deterministic standalone skill archive:

```bash
python3 scripts/project_tool.py pack --out dist/project-skill-1.2.0.zip
```

The root [plugin.json](plugin.json) also packages the **same** `skills/project` directory using OpenAI's documented portable plugin layout. The canonical construction skill is not duplicated. Optional read-only MCP intake and a separate intake skill are provided; no lifecycle hook is introduced. Local skill installation, native plugin import, and public-directory publication are separate operations. See [distribution](docs/DISTRIBUTION.md); no directory submission or installation into your ChatGPT account is performed by this repository.

## Public preview and release artifacts

This repository is public source with tested offline packages, not a claim of broadly
validated native-host behavior. See the [release guide](docs/RELEASE.md) for the release
checklist, reproducible Codex/Claude ZIPs and SHA256SUMS, and remaining host trials.
CI attaches both host packages and their checksums to each successful validation run.
No marketplace listing or GitHub Release is implied by a version in this repository.

## License, contribution, and support

[MIT](LICENSE) permits reuse, modification, and redistribution under its terms, including commercial use by OpenAI or anyone else. This is an invitation to reuse the work—not an assertion of endorsement, discoverability, partnership, or planned integration.

Improvements should bring inspectable evidence: [contribution guide](CONTRIBUTING.md), [security and privacy](SECURITY.md), [design decisions](docs/DESIGN.md), [changelog](CHANGELOG.md). Please use repository issues for non-sensitive bugs. Do not attach secrets, private project transcripts, or credentials.
