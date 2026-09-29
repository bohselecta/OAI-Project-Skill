# SayFrame authoring profile: a complete proposal for Project

This is guidance for SayFrame's existing language interaction, not permission to build.
Keep Purpose / Design / Approach as the only canonical language sections. Expand their
substance, not the interface's administrative machinery. Selecting this profile does not
accept text, request a model call, grant execution, or impose software planning on other
SayFrame projects. Use the current accepted revision and eligible conversation as source.

## Outcome

Produce enough clear natural language that Project can implement without inventing the
product. Describe the entire intended result, its functional architecture and proof of
completion. Do not compress the proposal into an elevator pitch at handoff. Functional
architecture means responsibilities, boundaries, state, inputs/outputs and invariants;
it is not necessarily a technology stack, class diagram, database schema or ticket list.
The next action may be a complete build or a deliberately limited experiment. State which.

## How to work with the author

Develop useful prose early. Ask at most one question per turn and only when its answer
materially changes the project. Offer optional tiles with exactly their visible meaning.
Resolve routine gaps with visible reversible suggestions; do not invent user approval.
Discuss alternatives without adopting them. Preserve accepted language and history. Cite
the affected accepted passages when explaining conflicts. Distinguish contradiction,
tradeoff, assumption and unknown. Do not turn this profile into twelve compulsory screens.

A request to develop the complete proposal is a visible language operation. Return proposed
section changes through SayFrame's existing proposal/acceptance path. Do not rewrite the
accepted brief in a hidden export stage. When the author accepts the expanded proposal,
review that exact new revision. Use the existing configured model and cost controls; no
extra agents, background critic loops or silent calls on keystrokes.

## Coverage lenses, not a questionnaire

Every lens must be covered, explicitly not applicable with a reason, or visibly open.
A nonempty field or heading does not establish coverage. Use exact accepted-text references.
Use these stable IDs to bind review findings to the prose; show readable labels in the UI.

### Purpose

- `outcome`: Intended change, audience, problem, useful output and observable success.
  Explain why the result should exist and whose decisions it supports.
- `scope`: What is included, excluded and deferred; important constraints and existing work
  to preserve. Separate the whole proposal from the scope of this authorized next action.

### Design

- `journeys`: Complete core interactions or production sequences, starting conditions,
  decisions, visible outcomes and meaningful edge cases. Include the defining interaction,
  not just a feature list. Explain the intended experience before naming components.
- `presentation`: Visual identity, composition, typography, content, assets/references,
  motion/sound where relevant, responsive behavior and accessibility. Describe what quality
  will look like in the actual result. Record rights/provenance and unreadable references;
  do not invent assets or claim they have been inspected. Nonvisual work may be N/A.
- `states`: Important states/transitions, empty/loading/error cases, recovery, interruption,
  cancellation and retained work. Explain what must never appear to have succeeded falsely.

### Approach

- `components`: Logical functional architecture. Which part owns each responsibility and
  decision? Where do the experience, domain rules, storage, models and external systems meet?
  Keep the architecture proportional; do not mandate services or a framework without need.
- `data`: Information created, retained, read, changed and deleted; source of truth, ownership,
  privacy, sensitive data, existing migrations and retention. Address concurrent/stale writes
  when material. A description of entities is enough; no compulsory database schema.
- `interfaces`: Inputs, outputs, dependencies and side effects across important boundaries.
  Identify real versus fixture behavior, unavailable providers, failure contracts and which
  integrations require credentials, consent or spending. Do not invent access or entitlements.
- `invariants`: Observable promises with stable IDs such as I-01. Preserve user intent, working
  behavior, information and authority. Identify risks that cannot be traded away for convenience.
- `acceptance`: Checks with stable IDs such as A-01, linked to invariants and journeys. Say how
  completion is demonstrated: tests, actual browser paths, visual review, live provider calls,
  deployment, hardware or participant evidence as applicable. Label what is not yet evidenced.
- `delivery`: Definition of done, exact intended artifact/workspace, local/remote scope, costs,
  permitted and prohibited actions, release destination when authorized, and rollback needs.
  The Project Skill repo is never an implicit destination for the user's product.
- `risks`: Assumptions, contradictions, unknowns, sensible alternatives, and stop conditions.
  Explain which unknowns block this action and which a bounded experiment can investigate.
  Distinguish confidence in coherent prose from evidence of feasibility or desirability.

## Review and change discipline

Before review, compute reviewSubjectDigest from the exact accepted snapshot, next action,
target, permission envelope and pinned connector. The returned review is applicable only
to that subject. Capture epoch and durable revision protections remain SayFrame's concern.

Return coverage and findings as proposals. Covered lenses cite actual accepted language;
N/A has a meaningful explanation; unresolved material gaps stay open. Never replace an
unresolved question with invented certainty to enable Build. No numeric completeness score.
Manual review is permitted and labeled. A fixture assessment cannot grant semantic readiness.
Model-assisted review records its actual model/prompt identity, without claiming infallibility.

A harmless wording change needs no invented contradiction, but old review/approval cannot
be reused for new bytes. A review may reuse valid prior reasoning after deliberately checking
the new subject; it must not merely copy the old readiness flag. Changing scope, target or
permissions also invalidates the old review binding and requires a fresh explicit approval.

## Handoff

Export the accepted language in full. The exact proposal, reviewed subject, target and limits
are bound together. Draft export is allowed without approval; build export requires explicit
user approval and no open blocking gaps. Do not export private transcript, unaccepted ideas,
secrets or unrelated project content. Do not hide an unresolved risk merely because it is not
a blocker. Say: “Handoff approved. Nothing has been executed.”

Project's later technical work may resolve implementation details within the accepted
functional contract. It must not silently redesign the product, reduce its acceptance bar,
or treat a new implementation convenience as user-approved intent.
