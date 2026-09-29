# Antigravity: integrate Project into the EXISTING SayFrame

## Mission

Make SayFrame the language-first front end for the OAI Project Skill. SayFrame develops a
complete natural-language proposal and functional architecture; the user revisits and accepts
it; an explicit approved handoff carries that exact revision to Project in Codex. Project
adopts that supplied contract and builds the authorized outcome without redoing product design.
Finish the working integration, not another plan, new app or simulated button.

## Start in the correct place

Work in the existing SayFrame workspace. Inspect Git status/branch/remotes, AGENTS.md hierarchy,
applicable skills, PROJECT-BLUEPRINT.md and contracts.ts if present, PRODUCT/ACCEPTANCE/STATUS,
the actual domain/persistence/model/handoff code, tests and screenshots. The earlier build
prompt is historical intent; the live implementation and latest request govern the change.
Record the starting revision, baseline tests and existing storage format. Preserve user data,
accepted revisions, source attribution, alternatives, branding and working paths.

Read a trusted checkout of OAI-Project-Skill, pinned to the connector revision supplied by the
user. The integration initially lives on `codex/sayframe-connector`, based on the still-open
Project candidate branch. Do not assume `main` already contains it. Resolve and record a full
commit; prefer the user's supplied commit over a moving branch. Never silently switch refs.
This repo is the TOOL SOURCE, not SayFrame's repo and not a generated product destination.

Read in order: root AGENTS.md and sayframe.connector.json; integrations/sayframe/README.md,
CONTRACT.md and AUTHORING.md; skills/project/references/sayframe.md; the adjacent SDK, types,
CLI and connector tests. Review actual code before using it. Do not merge the repositories.

## Implement one thin adapter

Vendor `skills/project/scripts/sayframe.mjs` and its adjacent `.d.mts` into an obvious
SayFrame integration directory, retaining license/provenance and a lock record with upstream
repository, full commit, connector version and file digests. Reuse existing application state
and validation. Do not replace the domain model or persistence system with the connector's
transport types. No remote JavaScript imports/eval, global install or new paid provider.

Add a small Project integration preference: repo, explicit ref, resolved commit/version and
connection/update status. Use loadConnector for bounded read-only public profile retrieval,
or the verified locally vendored profile when offline. Resolve a ref once and pin it for that
project. Updating requires a visible deliberate action; keep the last known version on error.
A compatible code upgrade is an engineering change, not automatic code downloaded by the app.

An imported/vendored profile does not activate execution. Preserve ordinary SayFrame projects.
Select this software-build profile explicitly; other creative/research authoring stays useful.

## Deepen language, not navigation

Integrate AUTHORING.md into the existing visible model operation/context for the Project
profile. Keep Purpose, Design and Approach. Add contextual “Develop the complete proposal”
and “Review for Project” actions, not a twelve-step form. Make assumptions and missing decisions
visible. Do not truncate or summarize the accepted proposal on export. A detailed expansion
must be a normal proposal the user accepts before it is the handoff source of truth.

Read the entire relevant accepted content. Show a size-limit error or an explicit bounded
strategy rather than losing constraints. Reuse existing provider, limits and error handling;
no background critic loop, extra agent, auto-paid test or keystroke-triggered calls. Sample mode
stays labeled. The fixture is test data, not a live review or a usable pinned source revision.

Use the 12 coverage lenses internally and expose readable findings alongside the prose. All
must be covered, open or N/A with reason. Exact accepted quotes anchor findings. No percentage
meter that confuses structural presence with semantic completeness. Manual review is available
and labeled; fixture review cannot authorize an arbitrary project.

## Connect the real accepted-state path

Map the app's accepted snapshot to Snapshot. Capture the current connector, target workspace,
next action and explicit scope. Default spending/external actions to not authorized. Compute
reviewSubjectDigest before the review request; reject a review from a different project,
revision, capture epoch, action, target or connector. Readiness is not acceptance or authority.

Call prepareHandoff after review. Show the complete resulting proposal, exact revision, target,
next action, limits, stopping conditions, unresolved findings and review provenance. Pending
edits/alternatives must not sneak in; explain when the displayed export excludes unsaved work.

Only an explicit existing/new “Approve Project handoff” control calls approveHandoff. Compute
needed hashes outside the persistence transaction, then re-read and compare-and-swap revision,
review subject and candidate digest inside a short durable transaction. Use the app's existing
operation IDs and concurrency protection. A failed/stale save cannot show success. Repeated
clicks or download retries reuse the same saved approval and exact files.

Export exactly proposal.md, handoff.json and CODEX-START.md. Reuse an existing archive/download
facility or use a reviewed small dependency only if needed. The exported folder must contain
only these files. Show “Handoff approved. Nothing has been executed.” Draft export remains
available and clearly unauthorized. Changing text, target, action or limits creates a new
review/approval; old approved bundles stay immutable and visibly refer to the old revision.

## The Build transition

The user can download the bundle, open the selected PRODUCT workspace in Codex, verify/import
with the trusted Project CLI, and invoke `$project build from <the approved handoff directory>`.
Provide accurate copyable next-step language and a working fallback for clipboard/download
failure. Do not invent a Codex URL scheme, claim to start a run, proxy a subscription, add a
server daemon or make an invisible API call. Connecting this repository is not execution.
Native one-click launch is a separate transport upgrade, not required by connector version 1.

Preserve the signature editorial SayFrame identity. Match existing type, spacing, review colors,
responsive composition and focus behavior. New review/permission states must be clear in words,
not just color. The integration should feel like the existing handoff grew more capable, not
like an enterprise setup panel was bolted onto the product.

## Complete acceptance, including retained data

Run existing tests before/after; no weakened assertions. Add the SDK fixture suite plus actual
app tests for complete-proposal generation through normal acceptance, export identity, paused
and stale responses, open gaps/N/A, manual versus fixture review, scope/revision invalidation,
competing tabs, late async digest results, duplicate approval, persistent reload and recovery.
Test an existing pre-integration database/backup and an already approved old handoff. Make any
schema migration additive, reversible where possible, and tested before using retained data.

Use the real UI to create/accept a project, propose and reject named ballots that violate its
privacy boundary, keep a coherent alternative, review, approve, download, and verify/import
that actual output with the trusted CLI in a disposable PRODUCT workspace. Reload and repeat
without losing previous revisions. Show missing-profile/network/clipboard/storage error paths.

Inspect desktop 1440×900 and mobile 390×844, narrow width, keyboard-only and reduced-motion
states. Inspect actual screenshots and fix layout/focus/overflow issues. Test hosted/public
mode still cannot trigger live paid provider calls. No deployment or paid calls are newly
authorized by this integration directive.

When an authenticated Codex host is available under the user's current permission, install
or safely update Project using its existing INSTALL.md procedure, verify actual discovery,
and run one bounded build from the produced approved fixture handoff. Inspect the built user
path against the handoff's I-/A- IDs. Report exact SayFrame/connector/product revisions, host,
actual model/effort, checks and source evidence. Do not describe a verifier test as a Codex run.
If host/auth/spending blocks that one check, complete independent implementation and mark it
NOT_RUN with the precise external action needed. Do not substitute a fake success indicator.

## Finish

Update SayFrame's existing current-state docs, entry instructions, environment examples only
if needed, and acceptance evidence. Record vendored provenance and how to review a connector
update. Report changed behavior, exact branch/revision, baseline/regression/browser evidence,
retained-data checks, real model calls, native Codex trial status and remaining limitations.
Use established authorized delivery paths; do not publish a new app or change repo visibility.
