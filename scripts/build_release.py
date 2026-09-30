#!/usr/bin/env python3
"""Build deterministic, offline Codex/Claude preview archives and SHA256SUMS.

Does not publish, tag, install, call models, or change host settings.
"""
import argparse
from pathlib import Path
import sys
import tempfile
import zipfile

import build_claude_skill
import project_tool

ROOT = Path(__file__).resolve().parents[1]


def build(out, root=ROOT):
    out = project_tool.no_symlinks(Path(out))
    if out.exists():
        raise ValueError('Output directory already exists; choose a new destination.')
    if root / 'skills/project' in out.parents or root / build_claude_skill.OUTPUT in out.parents:
        raise ValueError('Release output must be outside both skill packages.')
    info = project_tool.validate(root / 'skills/project')
    build_claude_skill.build(root, check=True)
    version = (root / 'VERSION').read_text().strip()
    if version != info['version']:
        raise ValueError('Release version differs from canonical skill.')
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.release-', dir=out.parent) as temporary:
        stage = Path(temporary) / 'release'
        stage.mkdir()
        codex = stage / f'project-codex-{version}.zip'
        project_tool.pack(root / 'skills/project', codex)
        claude = stage / f'project-claude-code-{version}.zip'
        with zipfile.ZipFile(claude, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, content in sorted(build_claude_skill.expected_files(root).items()):
                entry = zipfile.ZipInfo('project/' + name, date_time=(2026, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                entry.create_system = 3
                archive.writestr(entry, content)
        sums = ''.join(f'{project_tool.digest(p)}  {p.name}\n' for p in sorted(stage.glob('*.zip')))
        (stage / 'SHA256SUMS').write_text(sums, encoding='utf-8', newline='\n')
        if out.exists():
            raise ValueError('Destination appeared during build; nothing was overwritten.')
        stage.rename(out)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(f'Release artifacts prepared: {build(args.out_dir)}')
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
