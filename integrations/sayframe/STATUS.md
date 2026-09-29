# SayFrame connector status

Contract: [CONTRACT.md](CONTRACT.md), connector/protocol version 1.0.0 / sayframe.project/1.
Base: Project candidate `54c14a1e1298bdc90f2e289b330f2b39021da60f`.
Delivery branch: `codex/sayframe-connector`; stacked on `codex/project-skill-v1`.
Scope: implement the connector in the skill repository and provide an executable Antigravity
integration directive. The separately built SayFrame application is not present here.

## Implemented

Pinned read-only discovery, authoring profile, complete accepted-prose export, exact revision /
action / target-bound review, explicit approval, digest verification, TypeScript declarations,
safe local import, installed Project intake instructions, regression fixtures and CI integration.
No runtime dependencies, model calls, agent launch, private transcript upload or auto-update.

## Local evidence, 2026-09-29

Linux, Node 22.16.0, Python 3.13.5:

- `node --test integrations/sayframe/tests/connector.test.mjs`: **40 PASS**, zero failed/skipped.
  Includes negative controls, corruption, stale reviews/approval, exact-text preservation,
  three-file round trip, import idempotence/conflicts/locks/linked paths, CLI process behavior
  and bounded mocked repository discovery. A mocked fetch is not real GitHub discovery.
- `tsc --noEmit --strict --target ES2022 --module nodenext --lib ES2023,DOM integrations/sayframe/tests/types.mts`:
  **PASS**, including negative type assertions. Used existing local TypeScript installation.
- SDK, CLI and test JavaScript syntax: **PASS**.
- Original SKILL.md reconstruction verified against baseline SHA-256 before adding the intake
  paragraph. Unchanged sealed-file hashes are preserved; added/changed files are resealed.

The optional Python/Playwright browser SDK smoke could not reach its local test origin:
Chromium returned `net::ERR_BLOCKED_BY_ADMINISTRATOR`. **Browser SDK verification NOT_RUN**;
no policy bypass attempted. Its runnable harness is tests/browser-smoke.py. This is not a UI test.

The complete upstream checkout was unavailable through the local network. The pre-existing
Python suite and full package validation must run against this complete source in GitHub CI;
see this branch/PR's exact head checks. Earlier PR #1 success is not evidence for this revision.
CI now runs the existing Python suite, package validator/packager and the 40 connector tests
on Linux (Python 3.10/3.13), macOS and Windows with Node 22. The PR records actual final outcomes.

## CI findings retained

The first complete CI run (36620167653, head b45514267e42ca019ef3887aa2cce5c82bb47f1d)
validated the sealed package on all four runners but exposed an obsolete test asserting the
old nine-file inventory. The package now intentionally has thirteen sealed files. Replaced
that count with an exact thirteen-path set while retaining complete file/hash equality and
all drift/missing/extra-file negative controls. No production validation was relaxed.
The Node positive temp-directory fixture also resolves macOS's /var alias, matching the
existing Python fixture; explicit linked-workspace rejection remains tested and unchanged.
Final full-suite outcomes are recorded on the PR for the repaired head.

## Not claimed

Existing SayFrame code inspected or modified: **NOT_RUN** (repository not located).
Retained browser data/migrations and actual SayFrame UI integration: **NOT_RUN**.
Live model semantic review, authenticated Codex discovery/build, native model switching:
**NOT_RUN**. No paid calls, deployment, marketplace registration or user-machine installation.
The transport validates structure/integrity, not semantic truth, human identity or OS permissions.

## Next agent

Start in the existing SayFrame workspace with [ANTIGRAVITY.md](ANTIGRAVITY.md), using the
exact reviewed connector commit. Complete its adapter, retained-data and browser acceptance;
then perform a bounded native Codex trial when the user has authorized the target and host.
Keep all source/host evidence distinct. Do not create a replacement app or merge repositories.
