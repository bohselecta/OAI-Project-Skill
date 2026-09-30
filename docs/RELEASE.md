# Public release preparation

## Current release scope

**1.2.0 public preview** provides Codex and Claude Code skill packages. Source is public
under the existing MIT license. Offline correctness and cross-platform packaging are tested;
authenticated native-host and model-backed behavioral trials remain **NOT_RUN**. Preview
users must review the skill and retain their host's normal permissions/approval controls.
Do not advertise a stable/native-certified release, measured cost savings or guaranteed delivery.

Preparing this repository does not publish a GitHub Release, tag, marketplace listing or
hosted service. A maintainer may perform those separately after reviewing the exact source,
checks and limitations. Do not introduce publisher credentials or change visibility as a
side effect of packaging. For stable/native-host claims, record the outstanding trials below.

## Validate a reviewed revision

Use Python 3.10+ and Node 22+. No paid model, provider credential or dependency installation
is required for these checks. From a complete trusted checkout:

```bash
python3 scripts/project_tool.py validate
python3 scripts/build_claude_skill.py --check
python3 -m unittest discover -s tests -v
node --test --test-timeout=10000 integrations/sayframe/tests/connector.test.mjs integrations/sayframe/tests/claude-adapter.test.mjs integrations/sayframe/tests/native-mcp.test.mjs integrations/sayframe/tests/native-transport.test.mjs
python3 scripts/build_release.py --out-dir dist/project-1.2.0
```

Use a new output directory: packaging refuses an existing destination and does not replace
artifacts. On Windows use `python` if appropriate. For source changes, intentionally review
and reseal canonical changes, regenerate the Claude adapter, then repeat every affected check.
Do not use the seal command to conceal an unexpected downloaded-package mismatch.

The output contains:

```text
project-codex-1.2.0.zip
project-claude-code-1.2.0.zip
SHA256SUMS
```

Both ZIPs contain a top-level `project/` folder and its MIT license. They contain different
host metadata and must not be confused. Their generation is deterministic for identical
inputs. CI uploads these under the `project-release` artifact, alongside the existing exact
source tar and standalone Codex evidence. GitHub Actions artifact access follows GitHub's
normal account/repository rules; building locally is always available.

Verify archive bytes before extraction:

```python
from pathlib import Path
import hashlib

folder = Path('dist/project-1.2.0')
for line in (folder / 'SHA256SUMS').read_text().splitlines():
    expected, filename = line.split('  ', 1)
    assert Path(filename).name == filename, 'Unexpected checksum path'
    assert hashlib.sha256((folder / filename).read_bytes()).hexdigest() == expected, filename
print('Archive checksums match')
```

A checksum detects mismatch, not publisher identity: trust the pinned source/CI provenance.
Extract to a temporary location and inspect before installing; never unzip over an existing
skill. For Codex, prefer the repository's reversible [installer](../INSTALL.md). For Claude,
copy the complete extracted folder using the non-overwriting [installation guide](CLAUDE-CODE.md).
A standalone ZIP omits the source repository's tooling; retain a trusted source checkout
for validation, updates and recovery. Native plugin testing needs the complete source tree.

## Maintainer checklist

- Keep VERSION, canonical skill metadata/manifest, root plugin, generated Claude package,
  README and changelog consistent; retain separate SayFrame protocol/SDK version 1.0.0
- Preserve the MIT license and attribution; no new legal terms are needed
- Run the complete local suite, inspect generated output and all affected documentation links
- Review tracked files/diff for accidental secrets, personal paths and private transcripts;
  tests may contain clearly synthetic tokens, never working credentials
- Inspect exact-head CI on Linux, macOS and Windows, then exact-final-main CI after merging;
  an older green commit does not validate a later change
- Build fresh artifacts, verify checksums and test extraction; associate published assets
  with the same reviewed source commit, if a maintainer later publishes them
- Preserve truthful NOT_RUN limits in any release notes and point users to [SECURITY](../SECURITY.md),
  [CONTRIBUTING](../CONTRIBUTING.md) and [validation evidence](VALIDATION.md)

## Outstanding native-host evidence

Before a stable or broadly host-tested claim, record actual discovery, explicit/natural
invocation, permission boundaries, model switching/resume, cancellation, and behavioral
acceptance in each supported host. Use [Claude's host checklist](CLAUDE-CODE.md#evidence-and-remaining-checks),
[Codex evaluation guidance](../evals/README.md) and [native SayFrame limits](NATIVE-SAYFRAME.md).
Test the optional native Codex launch/Proceed flow separately from file-based intake.
Authenticated accounts, permitted tools and explicit budget for any paid trials are external
prerequisites. Source preparation and offline tests cannot manufacture this evidence.
