#!/usr/bin/env python3
"""Offline packaging and reversible installation for Project (Python 3.10+).

No network, model calls, subprocesses, global configuration edits, or shell hooks.
The manifest detects drift; it is not a signature or a trust decision.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import date, datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tempfile
from typing import Iterator
from urllib.parse import urlparse
import uuid
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'skills' / 'project'
MANIFEST = 'manifest.json'
RECEIPT = '.project-install.json'
REQUIRED = {
    'SKILL.md', 'LICENSE', 'agents/openai.yaml', 'references/records.md',
    'references/cadence.md', 'references/acceptance.md', 'references/recovery.md',
    'references/model-policy.json', 'assets/evidence.example.json',
}


class ProjectError(ValueError):
    """A recoverable validation or installation error."""


def absolute(path: Path) -> Path:
    return Path(os.path.abspath(path.expanduser()))


def no_symlinks(path: Path) -> Path:
    """Reject symlink/reparse-point path components, including broken links."""
    path = absolute(path)
    for node in (path, *path.parents):
        if node.is_symlink() or (hasattr(node, 'is_junction') and node.is_junction()):
            raise ProjectError(f'Refusing linked path: {node}. Use an explicit real directory.')
        # Python 3.10/3.11 Windows: reject reparse points without Path.is_junction.
        if os.name == 'nt' and node.exists():
            import stat
            if getattr(node.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                raise ProjectError(f'Refusing reparse point: {node}')
    return path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ProjectError(f'Cannot read valid JSON at {path}: {exc}') from exc
    if not isinstance(value, dict):
        raise ProjectError(f'Expected a JSON object: {path}')
    return value


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8', newline='\n')


def files_in(package: Path) -> dict[str, str]:
    package = no_symlinks(package)
    if not package.is_dir():
        raise ProjectError(f'Package directory not found: {package}')
    found: dict[str, str] = {}
    for item in sorted(package.rglob('*')):
        no_symlinks(item)
        if item.is_dir():
            continue
        if not item.is_file():
            raise ProjectError(f'Not a regular file: {item}')
        rel = item.relative_to(package).as_posix()
        if rel in {MANIFEST, RECEIPT}:
            continue
        if '__pycache__' in item.parts or item.suffix == '.pyc':
            raise ProjectError(f'Unexpected generated file: {rel}')
        found[rel] = digest(item)
    return found


def metadata(package: Path) -> dict:
    """Validate our intentionally restricted YAML, not arbitrary YAML documents."""
    try:
        text = (package / 'SKILL.md').read_text(encoding='utf-8')
    except (OSError, UnicodeError) as exc:
        raise ProjectError(f'Cannot read SKILL.md: {exc}') from exc
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ProjectError('SKILL.md requires YAML front matter.')
    front, body = text[4:].split('\n---\n', 1)
    if re.findall(r'^name: (.+)$', front, re.M) != ['project']:
        raise ProjectError('The skill must have exactly one name: project.')
    descriptions = re.findall(r'^description: (.+)$', front, re.M)
    try:
        desc = json.loads(descriptions[0]) if len(descriptions) == 1 else None
    except json.JSONDecodeError as exc:
        raise ProjectError('Description must be a double-quoted YAML/JSON scalar.') from exc
    if not isinstance(desc, str) or not 20 <= len(desc) <= 1024:
        raise ProjectError('Description must contain 20–1024 characters.')
    if not all(t in desc for t in ('Project:', '$project', 'Do not')):
        raise ProjectError('Description must name the trigger and its exclusions.')
    versions = re.findall(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$', front, re.M)
    if len(versions) != 1 or 'license: MIT' not in front:
        raise ProjectError('Expected one semantic version and MIT metadata.')
    if len(text.splitlines()) > 500 or len(body.split()) > 3000:
        raise ProjectError('Core skill exceeds the progressive-disclosure budget.')
    if body.count('```') % 2:
        raise ProjectError('Unclosed Markdown code fence in SKILL.md.')
    for link in re.findall(r'\]\(([^)]+)\)', body):
        if '://' in link or link.startswith('#'):
            continue
        target = link.split('#')[0]
        if not safe_relative(target) or not (package / target).is_file():
            raise ProjectError(f'Missing or unsafe skill reference: {link}')
    return {'name': 'project', 'version': versions[0], 'description': desc,
            'skill_words': len(body.split()), 'skill_lines': len(text.splitlines())}


def safe_relative(value: str) -> bool:
    p = PurePosixPath(value)
    return bool(value) and not p.is_absolute() and '..' not in p.parts and '\\' not in value and ':' not in value and str(p) == value


def validate_policy(path: Path) -> dict:
    policy = load_json(path)
    if policy.get('schema_version') != 1:
        raise ProjectError('Unknown model policy schema.')
    try:
        verified = date.fromisoformat(policy['verified_on'])
        review = date.fromisoformat(policy['review_after'])
    except (KeyError, TypeError, ValueError) as exc:
        raise ProjectError('Policy requires ISO verification/review dates.') from exc
    if review <= verified:
        raise ProjectError('Policy review date must follow verification date.')
    sources = policy.get('sources', [])
    if not isinstance(sources, list) or not sources:
        raise ProjectError('Policy requires source provenance.')
    ids = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ProjectError('Each source must be an object.')
        uri = urlparse(source.get('url', ''))
        if uri.scheme != 'https' or uri.hostname not in {'openai.com', 'developers.openai.com', 'learn.chatgpt.com', 'help.openai.com'}:
            raise ProjectError('Model policy sources must be official HTTPS references.')
        if not source.get('id') or source['id'] in ids:
            raise ProjectError('Source IDs must be unique.')
        ids.add(source['id'])
    roles = policy.get('roles', {})
    if not isinstance(roles, dict) or set(roles) != {'reasoner', 'builder', 'mechanical'}:
        raise ProjectError('Policy must define the three stable roles.')
    for role in roles.values():
        if not isinstance(role, dict) or not role.get('candidate_id') or not role.get('sources'):
            raise ProjectError('Each role requires a candidate and provenance.')
        if not set(role['sources']) <= ids or not role.get('workflow_evaluation'):
            raise ProjectError('Role provenance/evaluation status is incomplete.')
    return policy


def validate(package: Path = PACKAGE) -> dict:
    package = no_symlinks(package)
    found = files_in(package)
    if not REQUIRED <= found.keys():
        raise ProjectError(f'Missing required files: {sorted(REQUIRED - found.keys())}')
    info = metadata(package)
    manifest = load_json(package / MANIFEST)
    if manifest.get('format_version') != 1 or manifest.get('package') != 'project' or manifest.get('version') != info['version']:
        raise ProjectError('Invalid manifest identity/version.')
    expected = manifest.get('files')
    if not isinstance(expected, dict) or not all(isinstance(k, str) and safe_relative(k) for k in expected):
        raise ProjectError('Manifest contains invalid paths.')
    if found != expected:
        changed = sorted(k for k in found.keys() | expected.keys() if found.get(k) != expected.get(k))
        raise ProjectError(f'Package drift/corruption: {changed}')
    ui = (package / 'agents/openai.yaml').read_text(encoding='utf-8')
    if 'allow_implicit_invocation: true' not in ui or '$project' not in ui:
        raise ProjectError('UI metadata must preserve implicit and explicit invocation.')
    policy = validate_policy(package / 'references/model-policy.json')
    return {**info, 'valid': True, 'files': len(found), 'manifest_sha256': digest(package / MANIFEST),
            'policy_version': policy['policy_version'], 'host_discovery': 'NOT_RUN'}


def seal(package: Path = PACKAGE) -> dict:
    package = no_symlinks(package)
    info = metadata(package)
    found = files_in(package)
    if not REQUIRED <= found.keys():
        raise ProjectError('Cannot seal an incomplete package.')
    validate_policy(package / 'references/model-policy.json')
    write_json(package / MANIFEST, {'format_version': 1, 'package': 'project',
                                   'version': info['version'], 'files': found})
    return validate(package)


def locations(skills_dir: Path) -> tuple[Path, Path, Path]:
    skills_dir = no_symlinks(skills_dir)
    if skills_dir.name != 'skills':
        raise ProjectError('The destination skills directory must be named skills.')
    dest = no_symlinks(skills_dir / 'project')
    backups = no_symlinks(skills_dir.parent / 'project-backups')
    lock = no_symlinks(skills_dir.parent / '.project-install.lock')
    return dest, backups, lock


@contextmanager
def locked(lock: Path) -> Iterator[None]:
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ProjectError(f'Installer lock exists: {lock}. Verify no installer is running before removing a stale lock.') from exc
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            handle.write(str(os.getpid()) + '\n')
        yield
    finally:
        lock.unlink(missing_ok=True)


def managed(dest: Path) -> dict:
    no_symlinks(dest)
    if not dest.is_dir():
        raise ProjectError(f'Not an installed directory: {dest}')
    no_symlinks(dest / RECEIPT)
    receipt = load_json(dest / RECEIPT)
    if receipt.get('package') != 'project' or receipt.get('installer_format') != 1:
        raise ProjectError('Refusing an unmanaged destination; inspect/migrate it explicitly.')
    # Reject nested linked contents even for backup/uninstall; do not follow them.
    for p in dest.rglob('*'):
        no_symlinks(p)
    return receipt


def new_backup(backups: Path) -> Path:
    backups.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    return backups / f'project-{stamp}-{uuid.uuid4().hex[:12]}'


def install(package: Path, skills_dir: Path, replace: bool = False, dry_run: bool = False) -> dict:
    package = no_symlinks(package)
    info = validate(package)
    dest, backups, lock = locations(skills_dir)
    if package == dest or dest in package.parents or package in dest.parents:
        raise ProjectError('Source and destination must not overlap.')
    if dest.exists():
        receipt = managed(dest)
        try:
            current = validate(dest)
        except ProjectError:
            current = None
        if current and current['manifest_sha256'] == info['manifest_sha256'] and receipt.get('manifest_sha256') == info['manifest_sha256']:
            return {'action': 'unchanged', 'path': str(dest), **info}
        if not replace:
            raise ProjectError('Existing installation differs. Review it, then use --replace to preserve a backup and update.')
    if dry_run:
        return {'action': 'would-install', 'path': str(dest), 'backup_root': str(backups), **info}
    with locked(lock):
        # Recheck after acquiring the lock; avoid a stale preflight decision.
        if dest.exists():
            managed(dest)
            if not replace:
                raise ProjectError('Destination appeared during install; rerun after inspection.')
        dest.parent.mkdir(parents=True, exist_ok=True)
        backups.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.stage-', dir=backups) as temp:
            stage = Path(temp) / 'project'
            shutil.copytree(package, stage)
            (stage / RECEIPT).unlink(missing_ok=True)
            staged = validate(stage)
            write_json(stage / RECEIPT, {'installer_format': 1, 'package': 'project',
                       'version': info['version'], 'manifest_sha256': staged['manifest_sha256']})
            backup = None
            if dest.exists():
                backup = new_backup(backups)
                os.replace(dest, backup)
            try:
                os.replace(stage, dest)
            except OSError:
                if backup and not dest.exists():
                    os.replace(backup, dest)
                raise
    return {'action': 'installed', 'path': str(dest), 'backup': str(backup) if backup else None, **info}


def status(skills_dir: Path) -> dict:
    dest, _, _ = locations(skills_dir)
    if not dest.exists():
        return {'action': 'not-installed', 'path': str(dest), 'host_discovery': 'NOT_RUN'}
    receipt = managed(dest)
    info = validate(dest)
    if receipt.get('manifest_sha256') != info['manifest_sha256']:
        raise ProjectError('Installed manifest differs from installation receipt.')
    return {'action': 'verified-files', 'path': str(dest), **info}


def uninstall(skills_dir: Path) -> dict:
    dest, backups, lock = locations(skills_dir)
    if not dest.exists():
        return {'action': 'not-installed', 'path': str(dest)}
    with locked(lock):
        managed(dest)
        backup = new_backup(backups)
        os.replace(dest, backup)
    return {'action': 'uninstalled-to-backup', 'path': str(dest), 'backup': str(backup)}


def restore(backup: Path, skills_dir: Path, replace: bool = False) -> dict:
    dest, backups, lock = locations(skills_dir)
    backup = no_symlinks(backup)
    if backup.parent != backups or not backup.name.startswith('project-'):
        raise ProjectError('Restore requires a backup in this installation\'s project-backups directory.')
    managed(backup)
    validate(backup)
    with locked(lock):
        if dest.exists() and not replace:
            raise ProjectError('An installation exists; --replace is required to preserve it and restore.')
        previous = None
        if dest.exists():
            managed(dest)
            previous = new_backup(backups)
            os.replace(dest, previous)
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.replace(backup, dest)
        except OSError:
            if previous and not dest.exists():
                os.replace(previous, dest)
            raise
    return {'action': 'restored', 'path': str(dest), 'backup': str(previous) if previous else None,
            **validate(dest)}


def pack(package: Path, out: Path) -> dict:
    info = validate(package)
    out = no_symlinks(out)
    package = absolute(package)
    if out == package or package in out.parents:
        raise ProjectError('Archive must be outside the skill package.')
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.pack-', dir=out.parent) as temp:
        staging = Path(temp) / 'project.zip'
        with zipfile.ZipFile(staging, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for rel in sorted([*files_in(package), MANIFEST]):
                zi = zipfile.ZipInfo(f'project/{rel}', date_time=(2026, 1, 1, 0, 0, 0))
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = 0o100644 << 16
                zi.create_system = 3
                archive.writestr(zi, (package / rel).read_bytes())
        os.replace(staging, out)
    return {'action': 'packed', 'path': str(out), 'sha256': digest(out), **info}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, default=PACKAGE)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('validate', 'seal'):
        sub.add_parser(name)
    p = sub.add_parser('pack'); p.add_argument('--out', type=Path, required=True)
    for name in ('install', 'status', 'uninstall', 'restore'):
        p = sub.add_parser(name)
        scope = p.add_mutually_exclusive_group()
        scope.add_argument('--skills-dir', type=Path, help='Explicit directory named skills; defaults to ~/.agents/skills')
        scope.add_argument('--repo', type=Path, help='Install within this repository\'s .agents/skills')
        if name in ('install', 'restore'):
            p.add_argument('--replace', action='store_true')
        if name == 'install':
            p.add_argument('--dry-run', action='store_true')
        if name == 'restore':
            p.add_argument('--backup', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'validate': result = validate(args.package)
        elif args.command == 'seal': result = seal(args.package)
        elif args.command == 'pack': result = pack(args.package, args.out)
        else:
            skills = args.skills_dir or (args.repo / '.agents/skills' if args.repo else Path.home() / '.agents/skills')
            if args.command == 'install': result = install(args.package, skills, args.replace, args.dry_run)
            elif args.command == 'status': result = status(skills)
            elif args.command == 'uninstall': result = uninstall(skills)
            else: result = restore(args.backup, skills, args.replace)
        print(json.dumps(result, indent=2))
        return 0
    except (ProjectError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
