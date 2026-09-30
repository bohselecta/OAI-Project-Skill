# Resume, interrupts, and honest stop conditions

## Resume protocol

1. Read the latest user instruction, applicable host/repo rules, and checkpoint. A new instruction can supersede old task intent; it cannot waive host safety rules.
2. Compare actual repo/branch/HEAD and uncommitted work with the checkpoint. Inspect unexpected changes and reconcile; never reset to make the checkpoint appear true.
3. Confirm contract revision, pending action, completed evidence, and unchanged authority. Revalidate evidence only where source/environment changes invalidate it.
4. Resolve any pending model request. 'Proceed' resumes work; it does not broaden access or confirm an exact model ID. Do not demand another switch if the current model is adequate.
5. Continue the next safe action without rebuilding the plan or rereading all historical material.

When several projects are active, keep separate checkpoints in their own repositories/worktrees. Never resume a different project merely because it was most recent in memory.

## Blocked tool or provider

Check the actual capability once and try a reasonable supported alternative. Do not fabricate a browser session, tool result, model entitlement, provider call, or deployed check. Work on independent code/tests/docs; isolate the external adapter and test it with explicitly labeled fixtures. Keep live acceptance NOT_RUN until real access exists.

If no write/exec host is available, produce a bounded executable handoff, not a claim of installation or completion. If the original task was implementation, record that execution is blocked, with the exact host/access needed. Do not silently change a build request into a plan-only success.

## Human intervention

Batch genuinely necessary questions when they share a blocking decision. Do not ask the user to choose incidental libraries, run ordinary tests, or repeatedly say continue. Preserve approvals already given and recheck stale blockers when new evidence arrives.

## Cancellation and interruptions

On stop/cancel, stop actions and owned child processes when supported; do not kill unrelated processes or automatically roll back shared state. Save a minimal checkpoint and report external actions already performed. Later 'proceed' resumes only if the user clearly reauthorizes continuation.

At context, execution, or quota limits, checkpoint the exact next action and honest evidence state. Never promise invisible background progress. A model switch is not a workaround for missing authority or an instruction to evade rate limits.

## Multi-agent integration

Use one contract owner and one integration owner. Give each worker a bounded task, base revision, file ownership, interfaces, tests, and authority limits. Workers return source changes and evidence, not automatic contract amendments. Review integration conflicts, rerun affected checks, and invalidate stale evidence. Do not force parallelism for sequential or tightly coupled work.
