# Model Cadence Valve

Load at a meaningful routing decision, difficult failure, or handoff—not before every edit.

## Resolve capabilities before names

Use the current client's observed model picker/configuration, tool availability, and account/workspace constraints. Never make a model API request just to discover entitlement. Consult the adjacent `model-policy.json` as dated guidance; read current official sources when stale recommendations materially affect the decision. No browsing available: keep the capable current model, state uncertainty, and continue safe work.

Roles are stable; names are replaceable:

| Role | Decision boundary | Default behavior |
| --- | --- | --- |
| Reasoner | Unclear correctness; architectural conflicts; security/data risk; difficult integration or review | Use sufficient reasoning; resolve uncertainty and return work to execution. |
| Builder | Defined behavior, substantive engineering, testable interfaces | Default for sustained construction and ordinary debugging. |
| Mechanical | Explicit transform, small blast radius, strong verification | Optional batching lane; avoid disruptive micro-switches. |

These are roles, not constraints on model capability. The same model may fill every role. A fast model may handle complex work with sufficient evidence; the strongest may be the simplest and most economical overall choice. Do not impose arbitrary effort caps. Host defaults are a starting point, not a universal optimum.

## Switching policy

Assess expected remaining work, uncertainty, failure cost, cache discontinuity, and the human interruption. Do not claim numerical savings without measurements. A short task rarely benefits from manual downshifts. Batch useful switches at real boundaries, not every file.

Use a supported runtime switching control only when the host exposes it and existing authorization covers it. Otherwise save STATUS before asking for one manual switch and `proceed`. Never edit global model config to impersonate a live switch. Record one pending request; do not repeat it on each resume. On `proceed`, re-read checkpoint and actual repo state. Model identity remains unknown unless observed; record user confirmation separately.

Two failed, independent repair hypotheses trigger reassessment—not two test invocations. Escalation can mean deeper reasoning in the same model, a fresh diagnostic review, or a stronger model. Inability to access a provider is an external blocker, not a reasoning failure.

## Recommendations and updates

The packaged policy separates **documented capability**, **our suggested role**, and **local evaluation status**. A model card is not evidence that this workflow outperforms alternatives. Resolve exact runtime IDs and effort values; a UI label is not automatically an API enum. Never auto-install a successor, spend new credits, or mutate the pinned policy mid-build.

At the next maintenance cycle, compare official cards/docs, run matching regression cases, and revise only the policy fields supported by evidence. Projects already running keep their policy revision unless a compatibility/security correction is necessary. In that case record the change.

## Telemetry

Collect locally only when available and useful. Record source and definitions: model/effort; calls; elapsed time; input, cache reads/writes, output; observed reasoning subcounts; repair attempts; contract amendments; acceptance; interventions. Missing values are `null`/unknown, never zero. Reasoning tokens may be included in output—do not add them twice. Cached tokens may still have charges; token counts are not compute measurements.

Compare matched tasks and quality gates. Treat total dollars, wall time, review defects, accepted behavior, and human attention jointly. Never equate fewer steps with faster wall time or better product quality. Do not read unrelated conversation databases, credentials, or private logs to manufacture telemetry.
