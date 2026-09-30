"""Offline Claude adapter checks, not authenticated Claude Code/model trials."""
import importlib.util
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_claude_skill', ROOT / 'scripts/build_claude_skill.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ClaudeSkillTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        shutil.copytree(ROOT / 'skills/project', self.root / 'skills/project')
        shutil.copytree(ROOT / 'adapters/claude-code', self.root / 'adapters/claude-code')

    def test_checked_in_package_is_exact_generated_distribution(self):
        self.assertEqual(builder.build(ROOT, check=True), 12)

    def test_rebuild_is_deterministic_and_canonical_files_unchanged(self):
        before = {p.relative_to(self.root / 'skills/project'): p.read_bytes()
                  for p in (self.root / 'skills/project').rglob('*') if p.is_file()}
        builder.build(self.root)
        first = builder.expected_files(self.root)
        builder.build(self.root)
        self.assertEqual(builder.differences(self.root / builder.OUTPUT, first), [])
        self.assertEqual(before, {p.relative_to(self.root / 'skills/project'): p.read_bytes()
                         for p in (self.root / 'skills/project').rglob('*') if p.is_file()})

    def test_drift_is_detected_then_regenerated(self):
        builder.build(self.root)
        canonical = self.root / 'skills/project/references/acceptance.md'
        canonical.write_text(canonical.read_text() + '\nNew acceptance guidance.\n')
        with self.assertRaisesRegex(ValueError, 'stale'):
            builder.build(self.root, check=True)
        builder.build(self.root)
        self.assertEqual((self.root / builder.OUTPUT / 'references/acceptance.md').read_bytes(), canonical.read_bytes())
        builder.build(self.root, check=True)

    def test_missing_and_modified_output_fail_check(self):
        builder.build(self.root)
        (self.root / builder.OUTPUT / 'LICENSE').unlink()
        (self.root / builder.OUTPUT / 'SKILL.md').write_text('corrupt')
        with self.assertRaises(ValueError):
            builder.build(self.root, check=True)

    def test_unexpected_files_are_preserved_and_rejected(self):
        builder.build(self.root)
        extra = self.root / builder.OUTPUT / 'local-change.txt'
        extra.write_text('preserve me')
        for check in (True, False):
            with self.assertRaisesRegex(ValueError, 'Unexpected'):
                builder.build(self.root, check=check)
        self.assertEqual(extra.read_text(), 'preserve me')

    def test_changed_adapter_anchor_fails_closed(self):
        path = self.root / 'skills/project/SKILL.md'
        path.write_text(path.read_text().replace('explicit $project invocation', 'new invocation'))
        with self.assertRaisesRegex(ValueError, 'anchor changed'):
            builder.build(self.root)
        self.assertFalse((self.root / builder.OUTPUT).exists())

    def test_standalone_copy_has_all_local_references_and_imports(self):
        # No canonical repo siblings exist at the installation destination.
        installed = self.root / 'isolated/.claude/skills/project'
        shutil.copytree(ROOT / builder.OUTPUT, installed)
        for path in installed.rglob('*.md'):
            for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if '://' not in link and not link.startswith('#'):
                    target = (path.parent / link.split('#')[0]).resolve()
                    self.assertTrue(target.is_relative_to(installed), str(target))
                    self.assertTrue(target.is_file(), str(target))
        for path in installed.rglob('*.mjs'):
            for relative in re.findall(r"from ['\"](\.[^'\"]+)['\"]", path.read_text()):
                self.assertTrue((path.parent / relative).is_file())
        self.assertEqual((installed / 'LICENSE').read_bytes(), (ROOT / 'LICENSE').read_bytes())

    def test_no_hidden_host_configuration_or_model_override(self):
        text = (ROOT / builder.OUTPUT / 'SKILL.md').read_text()
        frontmatter = text.split('---', 2)[1]
        keys = {line.split(':', 1)[0] for line in frontmatter.splitlines() if line and not line.startswith(' ')}
        self.assertEqual(keys, {'name','description','argument-hint','license','metadata'})
        self.assertIn('$ARGUMENTS', text)
        self.assertNotIn('$project', text)
        self.assertFalse((ROOT / builder.OUTPUT / 'agents').exists())
        self.assertFalse((ROOT / builder.OUTPUT / 'manifest.json').exists())
        policy = json.loads((ROOT / builder.OUTPUT / 'references/model-policy.json').read_text())
        self.assertEqual(set(policy['roles']), {'reasoner','builder','mechanical'})
        self.assertTrue(all(r['workflow_evaluation'] == 'NOT_RUN' for r in policy['roles'].values()))

    def test_linked_output_is_rejected_when_platform_supports_links(self):
        (self.root / '.claude/skills').mkdir(parents=True)
        elsewhere = self.root / 'elsewhere'
        elsewhere.mkdir()
        try:
            (self.root / builder.OUTPUT).symlink_to(elsewhere, target_is_directory=True)
        except OSError as error:
            self.skipTest(f'Symlinks unavailable: {error}')
        with self.assertRaisesRegex(ValueError, 'linked output'):
            builder.build(self.root)
        self.assertEqual(list(elsewhere.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
