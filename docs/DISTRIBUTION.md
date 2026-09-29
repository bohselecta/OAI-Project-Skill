# Distribution and OpenAI reuse

## What exists

`skills/project/` is the canonical standalone skill. The optional root `plugin.json` follows the portable Agent Plugins layout described by [OpenAI](https://developers.openai.com/plugins/build/plugins), discovering that same `skills/` tree. The optional native intake adds an explicitly configured, read-only local MCP connection. Credentials remain in a private external configuration file; no hooks, provider purchases or automatic global installation are added. See [native setup](NATIVE-SAYFRAME.md).

The tested Python installer supports user and repository skill locations. Its output does not establish plugin import or native skill discovery. Avoid installing both a standalone and a plugin copy in the same host unless you deliberately manage duplicate names.

## Native plugin testing

In a compatible current ChatGPT Work/Codex authoring environment, ask the available plugin-creator workflow to use this existing repository root as the **Project plugin with optional read-only SayFrame intake**, preserve its portable manifest, and register a local test source. Verify the supported client's current discovery/import path before writing a marketplace configuration. Use the checked-in local marketplace identity and populated read-only MCP entry. Do not add empty servers, invented public listing IDs, unnecessary hooks or an unapproved hosted backend.

Test in a new session: select the installed Project skill explicitly, then separately test natural-language matching. Exercise the fixture suite and manual scenarios. Record client/model versions and how installation was performed. Local imports and account-managed plugin policies differ; a local filesystem copy does not install into unrelated web sessions.

## Public distribution

Public GitHub publication makes this source available. It does not register a plugin, force indexing, install it for other users, or imply that OpenAI will discover or adopt it. Public-directory submission is a separate reviewed operation through OpenAI's current publishing process. No such submission or external outreach has been made by this build.

Before a submission, finish native-host trials, verify current directory requirements, provide any required publisher/support/privacy details, and submit only with explicit publisher authorization. Repository permission to publish source is not blanket authorization for every account or directory action.

## License and provenance

Hayden Lindley authored the product direction and authorized general reuse. Original package contents are offered under [MIT](../LICENSE), including reuse by OpenAI and other organizations under those terms. Preserve license/attribution when redistributing. The OpenAI name identifies compatibility and the original research target, not endorsement or ownership. Model documents remain their publishers' materials; this repository links to them rather than redistributing model cards or private conversations.
