# Project for Claude Code

The Claude Code distribution is [`.claude/skills/project`](../.claude/skills/project/SKILL.md).
It preserves **Contract Freeze + Model Cadence Valve** from canonical Project 1.1.0,
with Claude-specific invocation, model guidance, and file-based SayFrame intake.
The existing OpenAI package, installer, archive, plugin and native transport are unchanged.

## Installation

Review a trusted, pinned revision of this repository first. In that checkout, run:

```bash
python3 scripts/project_tool.py validate
python3 scripts/build_claude_skill.py --check
python3 -m unittest discover -s tests -v
```

Claude Code can discover the committed skill when opened in this repository. To use it
in a **product repository**, copy the **whole folder**, including references and scripts,
to `<product-repository>/.claude/skills/project/`. For personal use across local projects,
copy it to `~/.claude/skills/project/` instead. Choose one scope; avoid a personal copy
shadowing a newer project copy. The current OpenAI installer does **not** install this
adapter; its `.agents/skills` destination is for Codex.

Example, from this checkout (Python 3.10+, no third-party dependencies):

```python
from pathlib import Path
import shutil

source = Path('.claude/skills/project').resolve()
# Choose exactly one destination; replace this example with your product repository.
destination = Path('/absolute/path/to/product/.claude/skills/project')
# Personal alternative: destination = Path.home() / '.claude/skills/project'
for entry in (destination, *destination.parents):
    if entry.is_symlink():
        raise SystemExit(f'Inspect linked destination before installing: {entry}')
shutil.copytree(source, destination)  # Refuses any existing destination; no overwrite.
print(f'Copied skill to {destination}; native discovery still needs checking')
```

Run the snippet in Python, or save it to a temporary `.py` file and execute it. On Windows,
use a native absolute destination and `python` if `python3` is unavailable. Installation
requires no credential, daemon, hook, MCP configuration or global instruction changes.
Node 22+ is needed only for optional SayFrame verification/import.

To update, inspect local modifications first; move the existing `project` folder to a
uniquely named backup **outside `.claude/skills`**, then copy the new folder. To uninstall,
move only that skill folder outside discovery. To restore, move the preserved backup back
after moving aside any current copy. Do not delete backups or merge over an existing folder.
Do not modify `CLAUDE.md`, permissions, models or unrelated skills during installation.

## Invocation and cadence

Start Claude Code in the product repository and check its skill menu for `/project`.
Restart the session if it has not detected a new copy. Native discovery has not been tested
in this release; copying files is not evidence of successful host loading.

```text
/project build a local-first research notebook with Markdown export
/project implement ./PRODUCT-SPEC.md end-to-end
/project finish this repository against its existing acceptance criteria
```

`Project: build …` retains natural-language matching. Quoted examples, brainstorming and
review-only requests do not authorize construction. `/project` with no task asks for a goal.
The workflow stays in the main conversation, inherits permissions and the current model,
and does not pre-approve tools or hard-code a model. No paid model-backed tests run on install.

The adapter maps stable roles to advisory `opus`, `sonnet`, and `haiku` aliases; they are
not requirements or measured performance claims. It checkpoints before a worthwhile model
change and asks you to use `/model`, then say **proceed**. Prefer a session-only selection
where available: saving a model default can affect later sessions. Your actual client and
provider determine availability and effort controls. If the current model is adequate,
it continues without a switch. **Proceed never grants new execution or publishing authority.**

## SayFrame compatibility

Use the exported `proposal.md`, `handoff.json`, and `CODEX-START.md` bundle. The last filename
is an existing protocol field, not a Claude command or instruction to open Codex. The bundled
trusted CLI validates exact contents/digests, rejects drafts for build and never starts work.
The current user must still authorize this handoff's action, target and limits.

A native `codex://` launch alone is unsupported here: export the file bundle instead. This
addition does not adapt the native launcher/MCP transport or claim Claude host acceptance
for them. Review-only and launch-only contexts remain read-only pending explicit build
authorization, including any requested model/Proceed gate. A direct authorized file-based
build does not acquire an unnecessary extra approval ceremony. See the installed
[intake reference](../.claude/skills/project/references/sayframe.md).

## Maintenance: one workflow, generated distributions

Do not edit generated `.claude/skills/project` files directly. Core changes belong in
`skills/project`; host-specific references belong in `adapters/claude-code/references`.
The generator applies narrow, checked substitutions to the canonical entrypoint, copies
shared records/cadence/acceptance/recovery/evidence and the local SayFrame verifier unchanged,
and supplies the Claude references/model policy. It excludes OpenAI UI metadata, manifest,
remote transport and native intake. Generated copies are self-contained, with no symlinks
or references outside the installed folder.

After an intentional source change:

```bash
python3 scripts/build_claude_skill.py
python3 scripts/build_claude_skill.py --check
python3 scripts/project_tool.py validate
python3 -m unittest discover -s tests -v
node --test integrations/sayframe/tests/claude-adapter.test.mjs
```

Canonical skill changes still require the existing reviewed `project_tool.py seal` process.
The Claude generator does not reseal or mutate that package. Changed anchors fail closed;
unknown generated files are preserved and require inspection. CI catches missing, stale,
modified or extra distribution files. Keep host references dated and review policy before
its review date; do not automatically update installed skills during product work.

## Evidence and remaining checks

Local checks on 2026-09-30: Python 3.12.14 / Node 24.19.0 / Linux. The 67 Python tests
passed, including 9 Claude adapter tests for deterministic generation, unchanged canonical
inputs, drift, corruption, unknown files, anchors, portable references and linked outputs.
The isolated Node test passed for approved bundle verification, draft refusal, and tamper
rejection after copying the skill out of the source repository. These are offline tooling
checks, **not** an authenticated Claude run or proof of model behavior.

Native-host acceptance is **NOT_RUN**. In a disposable product repository, with normal
permissions and an authorized account, a human can evaluate:

1. Personal/project discovery and `/project` argument delivery; no duplicate/shadowed skill
2. Small CLI change: proportional contract, preserved dirty work, real tests, no mandatory switch
3. Quoted trigger/review-only input: no build; missing task/spec: focused question
4. Model checkpoint, optional `/model` selection, `proceed`, interruption and cancellation;
   distinguish observed model from user-reported identity
5. SayFrame approved/draft/tampered bundles; native-link-only remains blocked; no approval-field
   bypass or global config changes
6. Substantial build: trace frozen acceptance IDs to actual evidence; no simulated live success

Record exact skill/source revision, Claude version/provider, observed model, prompts,
outputs, permissions, checks and limitations. Do not infer success from this checklist.
The broader [host-evaluation rubric](../evals/README.md) still applies; translate explicit
`$project` cases to `/project` and evaluate Claude's actual tools rather than Codex APIs.

## Official sources

Checked 2026-09-30; documentation supports packaging/host conventions, not behavioral claims:

- [Claude Code skills](https://code.claude.com/docs/en/skills): directories, invocation,
  arguments, supporting files and inherited defaults
- [Model configuration](https://code.claude.com/docs/en/model-config): aliases and model picker
- [Project instructions](https://code.claude.com/docs/en/memory): CLAUDE.md and repository context
- [Subagents](https://code.claude.com/docs/en/sub-agents): optional delegated work

Project is a community project, not an official Anthropic or OpenAI product.
