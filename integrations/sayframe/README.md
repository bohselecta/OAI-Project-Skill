# SayFrame → Project

**SayFrame is the authoring front end. Project is the builder.**

A versioned, local-first connector carries the entire accepted natural-language proposal and
functional architecture into Project. It is not an MCP server, hosted API or autonomous agent
launcher. Language acceptance, readiness and build authorization remain separate decisions.

## Start

For the existing SayFrame app, give Antigravity [ANTIGRAVITY.md](ANTIGRAVITY.md).
Repository discovery starts at [sayframe.connector.json](../../sayframe.connector.json).
Read [AUTHORING.md](AUTHORING.md) for the language-development profile and
[CONTRACT.md](CONTRACT.md) for the transport, integrity and host-transaction requirements.

This connector is on `codex/sayframe-connector`, stacked on the Project candidate branch.
Use the exact reviewed commit, not `main`, until the PRs are merged. A bare repository URL
is not permission to download/execute code or to silently follow a moving branch.

## What is implemented here

The dependency-free [ESM SDK](../../skills/project/scripts/sayframe.mjs) and
[TypeScript declarations](../../skills/project/scripts/sayframe.d.mts) provide pinned
read-only discovery, exact accepted-prose packaging, revision/action-bound review, explicit
stale-safe approval, tamper validation, and deterministic exports. The
[CLI](../../skills/project/scripts/sayframe-cli.mjs) verifies/imports safely without launching
anything. Its [intake guide](../../skills/project/references/sayframe.md) ships inside the
same sealed, installable Project package; it is not a second Project skill.

The fixture and tests exercise this connector. They do not claim that an inaccessible local
SayFrame app has already been modified or that a real Codex build has run. See
[STATUS.md](STATUS.md) for actual evidence and remaining host checks.

## Producer sequence

Import the SDK in SayFrame from a reviewed pinned/vendored local copy. Start from the app's
accepted state; do not feed arbitrary model output to these functions as if it were accepted.

1. Compute `reviewSubjectDigest` for the accepted snapshot + connector + target + scope.
2. Conduct a visible model/manual review of that exact subject. Preserve its source identity.
3. Call `prepareHandoff`, show its full prose and limits, and allow revision without acceptance.
4. On explicit user approval call `approveHandoff`; compare-and-swap the durable state AFTER
   asynchronous hashing. See CONTRACT.md. Hashes do not replace database transactions.
5. Persist the approval, then `exportFiles`. Download/copy retries reuse the saved bytes.

`exportFiles` returns exactly `proposal.md`, `handoff.json`, `CODEX-START.md`; package these
without a transcript, secrets, executable code or a competing summarized specification.
Changing text, next action, target or connector invalidates the prior review binding. Restore
creates a new revision/approval, not resurrection of old permission.

## Codex intake

Install/update the reviewed Project skill using [INSTALL.md](../../INSTALL.md). The connector
CLI requires Node 22+; the ordinary skill and Python installer do not acquire a Node requirement.
In the PRODUCT workspace, using the trusted installed CLI or a pinned tool checkout:

```sh
node /trusted/Project/skills/project/scripts/sayframe-cli.mjs verify /path/to/bundle --for-build
node /trusted/Project/skills/project/scripts/sayframe-cli.mjs import /path/to/bundle /path/to/product --for-build
```

Use actual local paths. The importer returns a new `.project/sayframe/handoff-<digest>` directory.
It does not overwrite AGENTS.md, existing contracts or another handoff. Then explicitly ask
Codex: `$project build from the approved SayFrame handoff at <returned directory>.`
Project must verify current user authority and target, adopt the complete accepted contract,
inspect live evidence, resolve real conflicts and build through its normal acceptance loop.
A successful import is not a build. A digest is not a signature or permission enforcement.

## Verification

```sh
node --test integrations/sayframe/tests/connector.test.mjs
python3 scripts/project_tool.py validate
python3 -m unittest discover -s tests -v
```

These are non-paid deterministic tests. The authored Next Chapter input uses an all-zero
synthetic commit and is explicitly a TEST FIXTURE, not an actual review or installable source
pin. Replace it by a verified real pin through the app adapter for an actual host trial.

## Scope

No new provider, cloud database, telemetry, network service, global configuration or auto-update.
No two-way live synchronization. Build results can be brought back as proposal source, never
silent accepted changes. No native one-click launch is claimed; explicit verified handoff is
the complete version-1 transport. MIT licensing follows the root and skill package licenses.
