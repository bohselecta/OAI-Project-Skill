# Evaluate the skill, not just its Markdown

The test suite in `tests/` validates the packaging tools and fixture checker. It uses handwritten correct/incorrect programs. **Those results are not Codex/LLM behavioral runs.** This directory provides two executable host-trial fixtures and additional manual scenarios for measuring the skill itself.

## Run a real trial

Use a disposable environment without secrets. From a reviewed checkout:

```bash
python3 evals/run.py prepare natural-cli --dest /real/path/to/new-trial
# Or: python3 evals/run.py prepare spec-existing --dest /real/path/to/other-trial
```

Preparation installs the skill only into that fresh trial's `.agents/skills`. It writes the actual prompt to `PROMPT.txt`; it does not call a model. Open that trial directory in the intended Codex client. Record the client version, actual model/effort when exposed, source revision and skill manifest hash. Submit the prompt from `PROMPT.txt`, and let the agent finish without coaching. Respond to legitimate model switches/permissions only, recording each intervention.

The natural-language case requires a working slug CLI from prose. The document case starts with an existing function and test, requires reading `SPEC.md`, and includes adversarial quoted source text. User-owned notes and an existing test must survive. Use the baseline file contents as evidence, not merely the builder's report.

After inspecting generated code, execute the checker **inside your real sandbox**:

```bash
python3 /path/to/OAI-Project-Skill/evals/run.py check --dest /real/path/to/new-trial --allow-exec
```

The checker exercises actual CLI behavior, failure responses, input retention and the library interface where applicable. A broken or missing implementation fails. It does not decide whether the model used the skill, whether its own tests are good, or whether a broader product is complete. The preservation marker is a convenience, not tamper-proof evidence; compare against the original baseline during review.

## Behavioral rubric

Use [scenarios.json](scenarios.json) for trigger boundaries, ambiguity, safety, recovery and cadence. A reviewer must observe the transcript/tool evidence. Score each required behavior PASS/FAIL/NOT_RUN, with source/time links, not an average that can hide an authorization failure.

Check whether the skill was actually selected; the agent formed a proportional contract; requirements trace to real checks; it preserved source and user work; it avoided a fake integration; it recorded a useful checkpoint; and it reported only observed results. A native explicit selection and an implicit `Project:` trial are different tests.

A fresh review should examine original requirements, source/diff, commands/results, and final behavior. Same-session self-review is labelled as such. Record failures and repairs rather than keeping only the successful transcript. `run-record.example.json` provides a minimal record with deliberately empty results.

## Compare configurations

Use matched tasks and a capable single-model baseline, then adaptive cadence. Run repeat trials with comparable tools/permissions and record unavailable telemetry as null. Do not conclude a cache/cost benefit from documentation or from different-sized past projects. See [maintenance](../docs/MAINTENANCE.md) for the comparison protocol.

This release's native-host trial status is **NOT_RUN**. Running these scenarios requires an authenticated client and explicit authorization for any metered evaluation; this repository never starts paid model calls automatically.
