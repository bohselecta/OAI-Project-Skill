# Maintain Project across model generations

## Change the smallest layer

A new model card normally changes `skills/project/references/model-policy.json`, not the workflow. Capability or host behavior changes may require reference or packaging updates. Rewrite the core only when evaluation demonstrates a better protocol or a real correctness defect.

On a maintenance request or before recommending stale candidates, read current official documentation for the affected host (OpenAI or Anthropic) and inspect the actual client's available models and controls. Record verification date, source URLs, documented positioning, suggested role, and **separate** workflow-evaluation status. If sources cannot be verified, retain the last dated policy with a stale/unverified warning; use the current capable host model instead of inventing a successor. `review_after` is a review prompt, not a timer, background job, or automatic update.

Never assume API identity equals a ChatGPT display label, that a subscription covers runtime API costs, that a picker is available, or that cache persists across models. Do not change global defaults or start paid evaluations to refresh the policy.

## Reviewable update procedure

1. Read `AGENTS.md`, the current release contract/status, and the changed source documentation. Use a branch; preserve unrelated work.
2. Record the proposed hypothesis and affected scenarios. Change only the needed layer, update `VERSION`, skill metadata and root `plugin.json` together for a release, and write a changelog entry. Policy versions also carry a date/revision.
3. Regenerate the Claude adapter with `python3 scripts/build_claude_skill.py` after canonical or adapter edits. Run `python3 scripts/project_tool.py seal` **only after reviewing intentional package changes**. Review the manifest diff. `validate` and installation never silently reseal.
4. Run package tests, fixture-runner tests, and the relevant native-host trials in [evals](../evals/README.md). Preserve negative controls. Static wording checks do not prove skill behavior.
5. Report the exact code revision, skill hash, host/client version, actual model and supported effort when exposed, starting state, evidence, and limitations. Unknown telemetry stays null/not recorded.
6. Open a PR with the evidence and regression assessment. Retain a known-good version. Changes that weaken permissions, retention, disclosure boundaries, or evidence honesty are release blockers.

## Measure the proposition, not a marketing claim

Compare matched tasks under (a) a capable single-model baseline and (b) adaptive cadence with the same contract/acceptance scope. To isolate contract freeze, separately compare stable-contract and ordinary workflows; do not change every variable at once. Counterbalance task order and repeat enough to characterize variability. Record task complexity and environment, not just step counts from unrelated projects.

Prioritize accepted behavior, retained data, safety, and user intent. Then examine elapsed time, directional interventions, independent failed repair hypotheses, post-freeze semantic changes, escalation reasons, and measured usage. Cache reads/writes, uncached input, output, and reasoning counts may use provider-specific accounting; document whether reasoning is included in output. Do not double-count, treat unavailable data as zero, or use lines of code as success.

Do not claim a speed/cost improvement when quality, scope, or permissions differ. A smaller model may be slower after rework; a strong model may be best throughout. Report paired differences and uncertainty, not invented industry averages or optimal ratios.

## Release gates

All deterministic checks must pass. Required behavioral scenarios need actual host evidence before a broadly tested/stable claim. Mark unsupported surfaces, missing tools, manual switching, and unrun trials explicitly. A new model-card recommendation alone is **documented**, not **workflow-validated**. A breaking contract/record change merits a major version; backward-compatible workflow capability a minor; a compatible correction a patch. The maintainer decides after reviewing evidence, not the running product agent.

Use the [release preparation checklist](RELEASE.md) for both host bundles and checksum artifacts. Never replace native-host evidence with deterministic fixture success.
