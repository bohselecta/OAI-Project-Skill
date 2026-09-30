# Claude Code host adapter

Keep Project in the main conversation: it needs the user's current intent and checkpoint.
This package does not set `context: fork`, a fixed `model`, `allowed-tools`, or hooks.
It inherits host permissions and the selected model. Use available specialist skills or
subagents only when useful; give them bounded ownership and integrate their evidence.

`/project <goal>` selects the skill. `Project: build …` is natural-language matching,
not a registered command. Quoted examples and review-only requests do not start builds.
Resolve bundled references and scripts from this skill's loaded directory, not the
product working directory. Preserve applicable CLAUDE.md and repository instructions.

At a useful cadence boundary, checkpoint first. Ask the user to open `/model`, choose
an available model (and supported effort), then reply **proceed**. Prefer a session-only
choice where offered: saving a default can change future sessions. Do not edit settings,
launch a second CLI, or claim prose changed the runtime. Observe runtime identity if
available; otherwise record it as unknown or user-reported. Keep the current model when
switching is unavailable or not worthwhile. `opusplan`, if already selected, follows
plan-mode transitions; it does not implement Project's semantic cadence by itself.

In plan mode or read-only contexts, respect those restrictions: prepare the contract
and checkpoint, then use the host's normal approval flow before implementation. Neither
Contract Freeze nor **proceed** bypasses a permission prompt or expands release authority.
No Claude CLI is needed merely to read this package; execution needs a tool-enabled host.

Official sources (checked 2026-09-30; documentation, not host-test evidence):
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/model-config
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/sub-agents
