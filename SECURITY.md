# Security and privacy

Project is an instruction skill plus optional offline Python tooling and an optional authenticated read-only SayFrame MCP client. The MCP client performs bounded retrieval only from its explicit private configuration; proposal text cannot redirect it. The installer makes no network requests or model calls and adds no runtime hooks. It does not collect analytics. An agent following the skill may use its host's tools to fulfill a user's task; the host's permissions, sandbox, privacy policies, and approvals remain authoritative.

Review a trusted, pinned source revision before installation. Manifest hashes detect drift but are not signatures. The validator supports this package's restricted metadata form; it is not a general untrusted-package security scanner. The installer refuses unmanaged destinations, symlinks/reparse points, and accidental replacement. This deliberately conservative policy may require using real paths on systems with symlinked home directories.

Backups stay outside skill discovery and are never deleted automatically. Handled rename failures are rolled back; power loss, hostile concurrent filesystem changes, and forced process termination are not claimed to be transactional or adversary-safe. Inspect a stale lock and existing backups before recovery.

`evals/run.py check --allow-exec` executes generated Python. Inspect that code first and run in a real disposable OS/container sandbox without secrets or network privileges. The fixture directory and timeout are not a security sandbox. Tests of prompt-injection resistance are behavioral scenarios, not a proof against all attacks.

Do not put API keys, credentials, private chat logs, or personal data into fixtures, issues, telemetry, or PRs. Use a repository private vulnerability-reporting channel if the maintainer has enabled one. If unavailable, open only a minimal non-sensitive issue asking for a private channel; do not publish exploit details or secrets. Rotate exposed credentials through their provider, not through repository history edits alone.

Claude Code users should preserve existing skill copies before copying the complete adapter; see [safe installation and recovery](docs/CLAUDE-CODE.md). Release SHA256SUMS checks archive bytes but does not authenticate the publisher. Neither adapter grants tools or bypasses host approvals.
