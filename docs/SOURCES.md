# Source ledger
Verified against official documentation on **2026-09-29**. These are provider documentation claims, not local behavioral measurements. Pages can change; the [model policy](../skills/project/references/model-policy.json) records the dated candidate mapping.

| Source | Narrow fact used | Design consequence |
| --- | --- | --- |
| [OpenAI: Build skills](https://developers.openai.com/codex/skills/) | Skills use `SKILL.md`, metadata, optional references and UI metadata. Current user discovery root is `~/.agents/skills`; explicit and implicit selection differ. | Self-contained package, progressive disclosure, documented explicit fallback, no claim that `Project:` is a registered command. |
| [OpenAI: Models](https://developers.openai.com/codex/models/) | Available models and controls vary by client; current coding recommendations include GPT-6.1 Sol. | Host capability checks before routing; no silent model-setting edits. |
| [GPT-6 Astra model card](https://developers.openai.com/api/docs/models/gpt-6-astra) | Current high-capability reasoning model metadata. | Candidate for consequential uncertainty; actual suitability must be evaluated. |
| [GPT-6.1 Sol model card](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | Current coding/agentic model metadata. | Candidate builder, not a universal mandatory setting. |
| [GPT-6 Luna model card](https://developers.openai.com/api/docs/models/gpt-6-luna) | Current efficient-model metadata. | Optional bounded-work candidate. |
| [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Guidance favors useful context, scoped instructions, and avoiding obsolete overprescription. | Short core with relevant references, not a large mandatory ritual. |
| [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) | Cache behavior depends on request prefixes and supported runtime configuration. | Stable repository text can help continuity; it does not guarantee cache reuse or free input. |
| [AGENTS.md](https://developers.openai.com/codex/guides/agents-md/) | Repository-scoped instructions apply to coding work. | Inspect applicable hierarchy and preserve existing conventions. |
| [Package your plugin](https://developers.openai.com/plugins/build/plugins) | Portable plugins use root `plugin.json` and `skills/`; directory publication is separate from local distribution. | Minimal skills-only wrapper; no claim of registration or adoption. |

## Corrections relative to the initial conversation design

The current documented user skill root is `~/.agents/skills`, not the older proposed `~/.codex/skills`. Do not migrate an existing installation without inspection. GPT-6.1 Sol replaces the earlier proposed Sol candidate in this dated policy, not in the stable workflow. Reasoning control names and availability come from the host, not from a hardcoded universal `High/XHigh` ladder.

No real Codex execution, model-switch behavior, task-quality benefit, cache ratio, cost reduction, or OpenAI endorsement follows from these documentation references. Those require separate evidence.
