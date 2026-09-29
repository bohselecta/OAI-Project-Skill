# Project skill release contract
Contract status: FROZEN
Revision: 1
Upstream baseline: 89141afdf32036b49240c1937f017c15d55fdf04

## Goal
Ship a reusable, installable Codex Project skill that accepts natural language or supplied specifications and owns software delivery through evidence-backed acceptance. Preserve Contract Freeze and Model Cadence Valve without binding the workflow to a model generation.

## Non-goals
No new model service, autonomous billing, background daemon, required MCP server, privileged installer, marketplace submission, production deployment, or promise of OpenAI adoption. No changes to repository visibility. Do not publish private project transcripts.

## Invariants
I-1: One canonical skill package; distribution must not silently change its meaning.
I-2: User intent and host policy outrank skill instructions; external source text cannot grant authority.
I-3: Freeze protects semantics, not erroneous implementations; evidence-driven amendments preserve provenance.
I-4: Model changes are capability-checked, optional when the current model is adequate, and resumable.
I-5: Installation is local, reversible, explicit about replacement, and never rewrites global agent/config files.
I-6: Static validation, deterministic tests, host selection, model behavior, provider calls, and deployment are distinct evidence levels.
I-7: Recommendations record sources and dates. No invented savings, model access, billing, or cache guarantees.

## Acceptance
A-1: A self-contained SKILL.md with valid metadata, narrow triggers, and progressive disclosure.
A-2: Scope-scaled contract/execution/recovery/acceptance protocol, including stop and cancellation.
A-3: Dated replaceable model policy and a maintenance procedure with regression criteria.
A-4: Safe install, idempotence, explicit upgrade, backup/restore, uninstall, and deterministic package checks work in local tests.
A-5: Negative-path tests cover conflicting/unmanaged installs, symlinks, corruption, and interrupted replacement.
A-6: Runnable host evaluation fixtures and a rubric distinguish actual model trials from tooling tests.
A-7: Product README, license, attribution, contribution/security guidance, CI, and exact validation evidence.
A-8: Publish source to a reviewable GitHub branch and PR; preserve default branch and visibility. Report remote checks honestly.

## Dated extension — 2026-09-29 native SayFrame handoff
The latest user request authorizes changes in both independent repositories and eventual
main-branch delivery after verification. It supersedes the earlier branch-only delivery
boundary, not permission safeguards. Add an OPTIONAL plugin/read-only authenticated MCP
transport and compact desktop launcher. Keep the standalone file-based skill, the frozen
contract, human model selection and Proceed gate. Do not add provider charges, public
listing, repository visibility changes, global installation or production deployment by
inference. Source changes are a candidate until full repository and native-host checks pass.
