"""Release inventory and reproducible artifacts; no host or model assertions."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_claude_skill
import build_release
import project_tool


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def test_archives_are_deterministic_and_checksums_match(self):
        first = build_release.build(self.root / 'first')
        second = build_release.build(self.root / 'second')
        version = (ROOT / 'VERSION').read_text().strip()
        self.assertEqual(sorted(p.name for p in first.iterdir()), ['SHA256SUMS', f'project-claude-code-{version}.zip', f'project-codex-{version}.zip'])
        for item in first.iterdir():
            self.assertEqual(item.read_bytes(), (second / item.name).read_bytes())
        for line in (first / 'SHA256SUMS').read_text().splitlines():
            digest, name = line.split('  ')
            self.assertEqual(digest, hashlib.sha256((first / name).read_bytes()).hexdigest())

    def test_archives_reproduce_exact_installable_packages(self):
        output = build_release.build(self.root / 'artifacts')
        version = (ROOT / 'VERSION').read_text().strip()
        with zipfile.ZipFile(output / f'project-codex-{version}.zip') as archive:
            archive.extractall(self.root / 'codex')
        self.assertTrue(project_tool.validate(self.root / 'codex/project')['valid'])
        with zipfile.ZipFile(output / f'project-claude-code-{version}.zip') as archive:
            self.assertEqual(set(archive.namelist()), {'project/' + p for p in build_claude_skill.expected_files()})
            archive.extractall(self.root / 'claude')
        self.assertEqual(build_claude_skill.differences(self.root / 'claude/project', build_claude_skill.expected_files()), [])

    def test_existing_destination_is_preserved(self):
        destination = self.root / 'existing'
        destination.mkdir()
        marker = destination / 'keep.txt'
        marker.write_text('user work')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            build_release.build(destination)
        self.assertEqual(marker.read_text(), 'user work')

    def test_stale_claude_distribution_blocks_artifacts(self):
        fixture = self.root / 'fixture'
        for source in ('skills/project', 'adapters/claude-code', '.claude/skills/project'):
            shutil.copytree(ROOT / source, fixture / source)
        shutil.copyfile(ROOT / 'VERSION', fixture / 'VERSION')
        (fixture / '.claude/skills/project/LICENSE').write_text('wrong')
        with self.assertRaises(ValueError):
            build_release.build(self.root / 'blocked', fixture)
        self.assertFalse((self.root / 'blocked').exists())

    def test_public_metadata_agrees_with_version(self):
        version = (ROOT / 'VERSION').read_text().strip()
        self.assertEqual(json.loads((ROOT / 'plugin.json').read_text())['version'], version)
        self.assertIn(f'**Version:** {version} public preview', (ROOT / 'README.md').read_text())
        self.assertIn(f'## {version} —', (ROOT / 'CHANGELOG.md').read_text())
        self.assertIn(f'version: "{version}"', (ROOT / '.claude/skills/project/SKILL.md').read_text())
        self.assertEqual((ROOT / 'LICENSE').read_bytes(), (ROOT / '.claude/skills/project/LICENSE').read_bytes())


if __name__ == '__main__':
    unittest.main()
