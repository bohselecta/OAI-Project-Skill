# SayFrame connector contract — 1.0.0

Status: implementation contract. Protocol: `sayframe.project/1`. Consumer: Project skill
1.0.0 candidate with the bundled SayFrame intake reference. This is not a release/certification
claim for an installed SayFrame app or Codex host.

## Ownership and boundaries

SayFrame owns the accepted Purpose / Design / Approach and its immutable history. It develops
the entire proposal, including functional architecture. The connector transports that accepted
meaning; Project checks technical reality and builds it. No second model rewrites the brief
on export. The connector never calls a model, executes a shell, runs Git or launches an agent.

The module is dependency-free ESM, usable in browsers with Web Crypto/secure context and modern
AbortSignal support, and Node 22+. Declarations are adjacent `.d.mts`. The CLI needs Node only;
the existing Project installer and non-SayFrame workflow remain Python/Markdown as before.

## Public operations

- `loadConnector({ repository, ref, fetchImpl?, signal? })`: opt-in public read-only discovery.
  Resolve the explicit branch/tag/ref to a commit, then fetch the descriptor and authoring
  profile at that same commit. Only this known repository, fixed paths, supported version,
  bounded response and matching profile hash are accepted. Never execute downloaded code.
- `reviewSubjectDigest({ snapshot, connector, target, scope })`: bind an actual semantic
  review to exact accepted text, revision, destination, next action, limits and connector pin.
- `prepareHandoff({ snapshot, connector, target, scope, review })`: validate and snapshot
  accepted language. Returns a DRAFT; cannot authorize. Review may include open gaps for review.
- `snapshotDigest(snapshot)`: compare the live accepted snapshot with the reviewed snapshot.
- `approveHandoff(bundle, { expectedIntentDigest, currentSnapshotDigest, approvedAt })`:
  call only after the user sees and explicitly approves the exact candidate. Reject stale
  identity, missing coverage or open blockers; retain original approval on an identical retry.
- `verifyHandoff(bundle, { forBuild? })`: structure, provenance fields, exact-reference and
  integrity validation; fail closed on unknown protocol/fields. Not a semantic oracle.
- `exportFiles(bundle)` / `readFiles(files, { forBuild? })`: deterministic three-file transport.

`prepareHandoff` accepts only an app-supplied accepted snapshot (IDs, title, acceptedAt and
three sections). Its input is NOT a model-response schema. The host must never let a model
choose acceptance, scope, destination, timestamp, digest binding or invocation permissions.

## Three files; one canonical language document

`proposal.md` holds the full accepted prose with Purpose / Design / Approach headings.
`handoff.json` holds protocol, pinned connector, source revision identity, UTF-8 byte spans,
document/snapshot/intent SHA-256, target, permission scope, review and optional approval.
It does not hold a competing summary or the transcript. Coverage references are short exact
quotes, not a second requirements document. `CODEX-START.md` is deterministic intake guidance;
modified startup instructions are rejected by the verifier.

Section spans use zero-based UTF-8 byte offsets, end-exclusive. Verification extracts each
span, requires valid UTF-8, and re-renders the exact document and spans. Hashing uses UTF-8
and a recursively key-sorted, no-whitespace JSON serialization for supported JSON fields.
The intent digest covers every envelope field except itself and approval. The snapshot digest
covers its metadata plus exact sections. Approval binds the intent digest; timestamps are ISO
UTC with milliseconds. No arbitrary numbers beyond validated byte offsets are hashed.

String limits: 300,000 UTF-16 code units per section, 12,000 per explanatory field, two MiB
per JSON operation. Preserve whitespace/Unicode; reject invalid Unicode/control characters,
missing/extra fields and malformed input. Do not silently truncate a complete accepted brief.
The 12 required coverage IDs and section mapping are exported as TOPICS. Each is covered with
exact relevant quotes, reasoned N/A, or open. Fixture reviews and open blocking gaps cannot be
approved. Advisory unknowns remain visible and can accompany a bounded prototype.

## Atomic host integration (not supplied by an SDK hash)

Hashing is asynchronous. SayFrame must re-read and compare-and-swap the accepted revision,
review subject and displayed candidate INSIDE its final durable transaction after hashing.
A second tab, edit, restore, action change, canceled session or connector update invalidates
that candidate. Do not hash asynchronously inside an IndexedDB transaction and let it expire.
Persist the approved bundle and operation ID atomically. Download/copy retry uses those bytes,
not newly generated prose or a new approval. A failed durable save is not an approval success.

The SDK defensively copies at async boundaries, but cannot enforce the host database transaction,
user gesture, capture epoch, UI review, secrets policy or process sandbox. Those are integration
acceptance requirements, not features to pretend the connector already enforces.

## Consumer staging and threat model

CLI verify/import validates before writing, rejects extra files and linked path components,
serializes imports with an exclusive lock and publishes a completed temporary directory under
`.project/sayframe/handoff-<package-digest-prefix>`. Re-import is idempotent only for identical
files. Changed/tampered prior imports and unrelated files are preserved, never overwritten.
It never alters root AGENTS.md, project contracts, Git state or skill installation. No shell is
constructed from project text. Source/target directories are local trusted-workspace inputs;
this is not an adversarial multi-user filesystem service. Host OS permissions still matter.

A digest detects alteration against an expected value; anyone can recompute it. It proves
neither authorship nor human consent. Codex must verify current user invocation and actual
workspace before acting. Scope language constrains an obedient agent; it is not an enforcement
layer. A package cannot revoke already running work; revocation happens in the executor.

## Stable acceptance IDs

SC-01 exact full-text round trip; SC-02 no automatic approval/execution; SC-03 immutable,
stale-safe approval; SC-04 revision/action/target/profile-bound review; SC-05 meaningful
coverage/provenance distinctions; SC-06 fail-closed malformed/tampered data; SC-07 non-destructive
idempotent local import; SC-08 explicit pinned read-only discovery; SC-09 installable consumer
intake; SC-10 host adapter, browser/retained-data checks and native Codex trial.

SC-01–09 have deterministic connector checks. SC-10 requires the existing SayFrame workspace
and authenticated host: complete it using ANTIGRAVITY.md. No fabricated end-to-end claim.
