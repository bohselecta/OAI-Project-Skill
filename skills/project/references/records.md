# Contract and resumption records

Use this reference when creating project state or resuming after compaction, interruption, or a model switch. Adapt names to existing canonical files. These are examples, not mandatory boilerplate.

## Contract

```markdown
# Project contract
Contract status: FROZEN
Revision: 1
Source: user request/date; specification path and revision

## Outcome and non-goals
What must work; what is explicitly excluded.

## Decisions and assumptions
Distinguish explicit requirements, inferred reversible choices, and unresolved material questions.

## Core experience and boundaries
Journeys, visual intent, state/interfaces, persistence, failure/recovery, platform/performance constraints.

## Invariants
I-01: <observable promise>

## Acceptance
A-01: <observable test> — supports I-01 — required evidence: <level>

## Authorization
Local scope: <permitted>
External/provider scope: <permitted or not authorized>
Delivery: <artifact/branch/preview/production, destination and authority>
Data/cost constraints: <known limits or unknown>
```

Use source paths, commit IDs, or document sections so requirements remain traceable. Do not embed a private transcript when a minimal attributed summary suffices. Keep executable domain contracts and fixtures beside the source; link them rather than duplicating them in Markdown.

## Status and checkpoint

```markdown
# Status
State: IN_PROGRESS | WAITING_FOR_MODEL | BLOCKED | VERIFIED | DELIVERED | CANCELLED
Run: <local identifier>
Contract: <path, revision, content digest when useful>
Source: <repo/branch/HEAD>; working tree: <clean/changed, diff identity>
Skill/model-policy version: <observed versions>
Model/effort: <runtime-observed | user-reported | unknown>

Completed: <accepted slices and evidence references>
Active: <one concrete next action>
Remaining: <bounded slices/checks>
Blockers: <exact dependency and independent work still possible>
Evidence: <check IDs, commands, environment, source identity, results>
Pending model switch: <target, reason, requested at, return task | none>
Authorization: <important constraints and unchanged permissions>
Owned resources: <local processes/ports/temp worktrees requiring cleanup>
```

For a small change this may be a short section in an existing issue/plan. For a long build, keep STATUS compact and link detailed evidence. Never make a checkpoint depend solely on conversation memory.

## Contract amendment

A meaningful decision records its ID, old revision, evidence, changed promise or interpretation, authority, affected acceptance checks, and new revision. Compatible implementation changes need not bump the semantic revision. Moving a digest computation out of a transaction while retaining atomicity is usually an implementation repair, not a new contract.

Material amendments require the authority already available for that decision. A model upgrade does not supply user approval. The original spec remains provenance; a new user instruction can supersede it with an explicit record.

## Cache discipline

Keep canonical requirements stable; put changing progress in STATUS. Load only relevant files, and preserve useful checkpoints across compaction. File references are navigation hints, not a substitute for reading needed content. Do not pad prompts to chase a cache percentage or insist on retaining an obsolete transcript. The host owns rendered prompts, routing, compaction, and cache behavior; unchanged files do not guarantee cache hits or reuse across models.
