# Evidence-backed acceptance

Choose checks from the promised behavior and consequences—not a fixed test count.

## Evidence record

For each acceptance ID, record the command or manual procedure, tested revision (and working-tree diff identity if dirty), environment, expected result, observed result, and artifact/log location. Use PASS, FAIL, NOT_RUN, or NOT_APPLICABLE with a reason. A later pass supersedes the specific failure it tests; it does not erase the history or validate unrelated code.

An optional machine-readable record is illustrated by `assets/evidence.example.json` in the skill root. Do not generate an evidence record instead of performing the check. Never populate a PASS template before execution.

## Match the surface

Web/mobile UI: a representative user journey, realistic content, screen sizes, state transitions, keyboard/focus, error recovery, reduced motion where relevant, and visual inspection of integrated assets. Automated screenshots alone do not establish good visual judgment.

Library/CLI: public interfaces, valid and invalid inputs, error/exit contracts, packaging/import behavior, regression checks, platform constraints, and documentation examples that actually run.

Service/API: authentication/authorization, request/response validation, state transitions, timeouts/retries/idempotency when needed, integration tests, and observable failure paths.

Persistence/migrations: representative existing data, forward transformation, retained invariants, backup/recovery or rollback as applicable, and concurrency/loss scenarios. Test destructive migrations only against disposable or explicitly authorized environments.

Hardware/research/data products: simulations, bench tests, physical devices, datasets, and participant outcomes are distinct. Do not label an unperformed hardware or participant test as passed because software simulation worked. Use applicable specialist workflows.

## Anti-shortcut checks

A test that mocks the entire feature does not prove integration. Check that tests can fail when behavior is broken; use a negative case or targeted mutation where worthwhile. Search changed production paths for unexplained TODOs, fixed success responses, no-op handlers, skipped tests, and placeholder provider output. Not every TODO is a defect, and legitimate test doubles are not prohibited.

A failing test may itself be invalid. Preserve the old expectation/evidence, establish the correct requirement independently, repair the test, and demonstrate the implementation against the corrected contract. Never change a test solely to match current output.

## Independent review

For substantial/high-consequence work, prefer a fresh reviewer if the host supports it. Supply contract + original source constraints + relevant decisions + exact diff/source + runnable checks. Ask the reviewer to try to falsify important claims, examine errors and recovery, and report concrete defects with reproduction evidence. Keep access within the same authorization envelope. Do not conceal a security-relevant decision in pursuit of a 'blind' review.

A fresh context is not automatically an independent measurement; shared assumptions and correlated model errors remain possible. Report same-agent review accurately. Recheck changed behavior after fixes. Do not require a stronger model merely to rubber-stamp success.

## Release versus verification

VERIFIED: all required scope checks have adequate evidence, or the user explicitly amended scope with provenance. NOT_RUN on a required check prevents this status.

DELIVERED: verified plus the authorized artifact/repository/release step and its applicable checks. Publishing still requires authority even after all tests pass. Record exact revision, destination, and rollback path for consequential releases.

BLOCKED: independent work is done but required execution/verification depends on unavailable access, tooling, budget, or a material choice. State what works, what does not, and the smallest necessary external step. Do not call this production-ready.

Agent verification is not human approval, marketplace certification, legal compliance certification, or a claim of real-world success.
