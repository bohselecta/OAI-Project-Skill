# Native SayFrame transport

This optional layer preserves `sayframe.project/1` and its exact three-file contract.
It does not replace the standalone file connector or require an MCP server for normal Project use.

A `codex://new` prompt carries only a content-addressed ID, expected intent digest, connector
commit and read-only startup instructions. The desktop host owns workspace resolution and
Send. The SayFrame service requires authentication; knowing an ID is not a credential.

The sibling `sayframe-intake` skill owns pre-Proceed intake. It must read all artifacts,
cryptographically verify them, inspect the product workspace without mutation, and wait.
After Proceed, stage the bundle under an explicit product-workspace directory:

```sh
node <trusted-project-skill>/scripts/sayframe-fetch.mjs \
  <sf1-id> <intent-sha256> <absolute-product-workspace>/.project/sayframe-remote
node <trusted-project-skill>/scripts/sayframe-cli.mjs verify \
  <absolute-product-workspace>/.project/sayframe-remote/<sf1-id> --for-build
```

The fetch command writes a new directory only. Existing directories, symlinks, changed hashes,
expired/revoked handoffs, unavailable credentials and conflicting targets fail closed. Inspect
an interrupted staging directory rather than force-overwriting it. Never execute scripts in
the supplied handoff. The trusted tools are part of the installed Project package.

The read-only key lives in a private local connector configuration, not in a link, prompt,
repository or browser storage. The service is single-author, not a multi-tenant hosted platform.
Local/repo plugin installation is not public directory publication. Native desktop host testing
and model behavior remain separate from deterministic protocol and browser tests.
