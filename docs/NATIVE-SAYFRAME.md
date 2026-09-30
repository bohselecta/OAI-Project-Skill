# Native SayFrame intake

Project remains the same canonical construction workflow. The optional native plugin adds a
read-only intake skill and an authenticated connector; it does not add an agent scheduler or
programmatic model switching. The stable plugin ID remains **project**. The current package
version is separate from the unchanged `sayframe.project/1` connector/SDK version 1.0.0.

## Install deliberately

Use a complete checkout of a reviewed revision of this repository. Validate the package first. The root portable `plugin.json`, `mcp.json`,
`skills/` and `.agents/plugins/marketplace.json` make the local distribution. In a compatible
Codex host, add this repository checkout as a local plugin marketplace, then install its
**Project / OAI Project** entry. The configured marketplace ID is `oai-project-local`; the
plugin reference is `project@oai-project-local`. Do not claim directory availability until a
public listing has actually been submitted and accepted. Native installation/discovery has
not been exercised by this delivery environment.

An existing standalone `project` installation can conflict with a plugin copy of the same
skill. Inspect the host's selected source and explicitly choose the canonical copy in this
plugin. Preserve or reversibly disable an older standalone copy; do not uninstall it silently.
Ordinary standalone installation through `scripts/project_tool.py` remains available without
MCP setup. No global configuration is modified by validation or packaging.

The MCP server is a stdio Node 22+ child process, launched by the host. Node must be on that
host's executable path. Configure SayFrame using its explicit local setup, which writes
`~/.config/sayframe/connector.json` with only `{origin, readKey}`. The file must be private,
regular and not behind symlink components. A custom absolute filename can be supplied via
`SAYFRAME_CONNECTOR_CONFIG` in the host environment. Never put a key in chat or the repository.

## User experience and authority

SayFrame freezes the accepted proposal and prepares a `codex://new` URL carrying only ID,
expected intent digest, connector pin and target. Codex owns native workspace matching and
Send. The repository remote is not an automatic clone instruction. The user sends the
prepared intake prompt; `sayframe-intake` reads all three artifacts, verifies their identities
and hashes and inspects the selected workspace **without changes**. It reports limitations
rather than inventing readiness, then waits for model choice and **Proceed**.

After that explicit instruction, the canonical Project skill adopts the complete functional
contract rather than repeating the design interview. Its contract-freeze/model-cadence loop,
permission boundaries, retained-data requirements and evidence-based acceptance still apply.
Later implementation decisions are recorded as deltas, never edits to the frozen source.

The MCP surface has only `get_handoff`, `get_handoff_manifest`, `get_artifact` and
`verify_handoff`. It cannot write repository files, invoke a model, run a shell, switch models,
create a build or deploy. Integrity is not semantic completeness, identity or current consent.
The explicit post-Proceed staging CLI is separate from the read-only MCP tools.

## Fallback and operating limits

The existing three-file ZIP intake works without native transport. Local private Node hosting
is supported by the SayFrame backend implementation. That filesystem backend is not a durable
Vercel/serverless store; cloud multi-user hosting and OAuth are not implemented. Do not add
new paid services or widen account access as an incidental installation step.

Expired, revoked, truncated, malformed or hash-mismatched responses fail closed. A native
URL click is not proof the app opened. A plugin install is not proof a build ran. Previously
retrieved files are not recalled when read access is revoked.

## Checks

```sh
python3 scripts/project_tool.py validate
python3 -m unittest discover -s tests -v
node --test integrations/sayframe/tests/connector.test.mjs
node --test --test-timeout=10000 integrations/sayframe/tests/native-*.test.mjs
```

Native test HTTP fixtures verify this client's protocol handling, not the real SayFrame
backend. The cross-repository delivery suite separately exercises real service-to-MCP calls.
See [current verification scope](HANDOFF-STATUS.md) before treating this as a release.

## Primary interface references

- [Codex commands and native deep links](https://learn.chatgpt.com/docs/reference/commands)
- [OpenAI portable plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Portable plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)
- [Portable MCP configuration schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json)

The documented mechanisms are not substitutes for a real native-host trial of this package.
