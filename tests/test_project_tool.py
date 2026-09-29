"""Deterministic package/install checks, not LLM behavioral evaluations."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('project_tool', ROOT / 'scripts/project_tool.py')
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        # macOS's /var is a symlink; use its real path to test our no-link policy.
        self.root = Path(self.temp.name).resolve()
        self.package = self.root / 'source/project'
        shutil.copytree(tool.PACKAGE, self.package)
        self.skills = self.root / 'home/.agents/skills'
        self.dest = self.skills / 'project'

    def tearDown(self):
        self.temp.cleanup()

    def installed(self):
        return tool.install(self.package, self.skills)

    def change_source(self):
        path = self.package / 'references/recovery.md'
        path.write_text(path.read_text(encoding='utf-8') + '\nMaintainer clarification.\n', encoding='utf-8')
        tool.seal(self.package)

    def link(self, target, source, directory=False):
        try:
            target.symlink_to(source, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f'OS does not permit unprivileged symlink creation: {exc}')

    def test_package_validates_without_claiming_host_discovery(self):
        result = tool.validate(self.package)
        self.assertTrue(result['valid'])
        self.assertEqual(result['host_discovery'], 'NOT_RUN')
        self.assertLess(result['skill_words'], 3000)

    def test_every_package_file_is_covered(self):
        manifest = tool.load_json(self.package / tool.MANIFEST)
        self.assertEqual(manifest['files'], tool.files_in(self.package))
        # Verify the exact reviewed inventory, not the pre-connector count of nine.
        self.assertEqual(set(manifest['files']), {
            'LICENSE', 'SKILL.md', 'agents/openai.yaml', 'assets/evidence.example.json',
            'references/acceptance.md', 'references/cadence.md',
            'references/model-policy.json', 'references/records.md',
            'references/recovery.md', 'references/sayframe.md',
            'scripts/sayframe.mjs', 'scripts/sayframe.d.mts', 'scripts/sayframe-cli.mjs',
            'references/sayframe-transport.md', 'scripts/private-fs.mjs',
            'scripts/sayframe-fetch.mjs', 'scripts/sayframe-mcp.mjs', 'scripts/sayframe-remote.mjs',
            'scripts/transport.mjs', 'scripts/transport.d.mts',
        })

    def test_drift_refused_without_resealing(self):
        (self.package / 'SKILL.md').write_text('broken', encoding='utf-8')
        with self.assertRaises(tool.ProjectError):
            tool.validate(self.package)

    def test_extra_file_refused(self):
        (self.package / 'extra.txt').write_text('surprise', encoding='utf-8')
        with self.assertRaisesRegex(tool.ProjectError, 'drift'):
            tool.validate(self.package)

    def test_missing_file_refused(self):
        (self.package / 'LICENSE').unlink()
        with self.assertRaisesRegex(tool.ProjectError, 'Missing'):
            tool.validate(self.package)

    def test_manifest_traversal_refused(self):
        path = self.package / tool.MANIFEST
        data = tool.load_json(path)
        data['files']['../outside'] = '0' * 64
        tool.write_json(path, data)
        with self.assertRaisesRegex(tool.ProjectError, 'paths'):
            tool.validate(self.package)

    def test_frontmatter_duplicate_name_refused(self):
        path = self.package / 'SKILL.md'
        text = path.read_text(encoding='utf-8').replace('name: project', 'name: project\nname: project')
        path.write_text(text, encoding='utf-8')
        with self.assertRaises(tool.ProjectError):
            tool.seal(self.package)

    def test_missing_reference_refused(self):
        path = self.package / 'SKILL.md'
        path.write_text(path.read_text(encoding='utf-8') + '\n[bad](references/missing.md)\n', encoding='utf-8')
        with self.assertRaisesRegex(tool.ProjectError, 'reference'):
            tool.seal(self.package)

    def test_invalid_model_source_refused(self):
        path = self.package / 'references/model-policy.json'
        policy = tool.load_json(path)
        policy['sources'][0]['url'] = 'https://openai.com.attacker.invalid/model'
        tool.write_json(path, policy)
        with self.assertRaisesRegex(tool.ProjectError, 'official'):
            tool.seal(self.package)

    def test_invalid_policy_dates_refused(self):
        path = self.package / 'references/model-policy.json'
        policy = tool.load_json(path)
        policy['review_after'] = policy['verified_on']
        tool.write_json(path, policy)
        with self.assertRaises(tool.ProjectError):
            tool.seal(self.package)

    def test_unknown_role_source_refused(self):
        path = self.package / 'references/model-policy.json'
        policy = tool.load_json(path)
        policy['roles']['reasoner']['sources'] = ['fabricated']
        tool.write_json(path, policy)
        with self.assertRaises(tool.ProjectError):
            tool.seal(self.package)

    def test_fresh_install_and_status(self):
        result = self.installed()
        self.assertEqual(result['action'], 'installed')
        self.assertTrue((self.dest / 'SKILL.md').is_file())
        self.assertEqual(tool.status(self.skills)['action'], 'verified-files')
        self.assertIsNone(result['backup'])

    def test_reinstall_is_idempotent(self):
        self.installed()
        before = (self.dest / tool.RECEIPT).stat().st_mtime_ns
        self.assertEqual(self.installed()['action'], 'unchanged')
        self.assertEqual((self.dest / tool.RECEIPT).stat().st_mtime_ns, before)
        self.assertFalse(list((self.skills.parent / 'project-backups').glob('project-*')))

    def test_dry_run_has_no_filesystem_side_effects(self):
        result = tool.install(self.package, self.skills, dry_run=True)
        self.assertEqual(result['action'], 'would-install')
        self.assertFalse(self.skills.parent.exists())

    def test_unmanaged_destination_never_overwritten(self):
        self.dest.mkdir(parents=True)
        sentinel = self.dest / 'SKILL.md'
        sentinel.write_text('user-owned', encoding='utf-8')
        with self.assertRaises(tool.ProjectError):
            tool.install(self.package, self.skills, replace=True)
        self.assertEqual(sentinel.read_text(encoding='utf-8'), 'user-owned')

    def test_upgrade_requires_explicit_replace(self):
        self.installed()
        old = tool.digest(self.dest / tool.MANIFEST)
        self.change_source()
        with self.assertRaisesRegex(tool.ProjectError, '--replace'):
            self.installed()
        self.assertEqual(tool.digest(self.dest / tool.MANIFEST), old)

    def test_upgrade_preserves_backup_outside_discovery(self):
        self.installed()
        old = tool.digest(self.dest / tool.MANIFEST)
        self.change_source()
        result = tool.install(self.package, self.skills, replace=True)
        backup = Path(result['backup'])
        self.assertEqual(tool.digest(backup / tool.MANIFEST), old)
        self.assertNotIn(self.skills, backup.parents)
        self.assertNotEqual(tool.digest(self.dest / tool.MANIFEST), old)

    def test_modified_managed_install_preserved(self):
        self.installed()
        (self.dest / 'notes.txt').write_text('local customization', encoding='utf-8')
        result = tool.install(self.package, self.skills, replace=True)
        self.assertEqual((Path(result['backup']) / 'notes.txt').read_text(encoding='utf-8'), 'local customization')
        self.assertFalse((self.dest / 'notes.txt').exists())

    def test_uninstall_moves_instead_of_deleting(self):
        self.installed()
        result = tool.uninstall(self.skills)
        self.assertFalse(self.dest.exists())
        self.assertTrue((Path(result['backup']) / 'SKILL.md').exists())
        self.assertEqual(tool.uninstall(self.skills)['action'], 'not-installed')

    def test_restore_from_backup(self):
        self.installed()
        backup = Path(tool.uninstall(self.skills)['backup'])
        self.assertEqual(tool.restore(backup, self.skills)['action'], 'restored')
        self.assertFalse(backup.exists())
        self.assertEqual(tool.status(self.skills)['action'], 'verified-files')

    def test_restore_over_install_requires_replace(self):
        self.installed()
        backup = Path(tool.uninstall(self.skills)['backup'])
        self.installed()
        with self.assertRaisesRegex(tool.ProjectError, '--replace'):
            tool.restore(backup, self.skills)
        result = tool.restore(backup, self.skills, replace=True)
        self.assertTrue(Path(result['backup']).is_dir())

    def test_foreign_or_corrupted_backup_refused(self):
        self.installed()
        backup = Path(tool.uninstall(self.skills)['backup'])
        with self.assertRaises(tool.ProjectError):
            tool.restore(self.package, self.skills)
        (backup / 'SKILL.md').write_text('modified', encoding='utf-8')
        with self.assertRaises(tool.ProjectError):
            tool.restore(backup, self.skills)
        self.assertTrue(backup.exists())

    def test_failed_replacement_restores_old_install(self):
        self.installed()
        old = tool.digest(self.dest / tool.MANIFEST)
        self.change_source()
        real_replace = os.replace
        def fail_staging(src, dst):
            if Path(src).parent.name.startswith('.stage-') and Path(dst) == self.dest:
                raise OSError('injected disk failure')
            return real_replace(src, dst)
        with patch.object(tool.os, 'replace', side_effect=fail_staging):
            with self.assertRaisesRegex(OSError, 'injected'):
                tool.install(self.package, self.skills, replace=True)
        self.assertEqual(tool.digest(self.dest / tool.MANIFEST), old)
        self.assertEqual(tool.status(self.skills)['action'], 'verified-files')
        self.assertFalse((self.skills.parent / '.project-install.lock').exists())

    def test_failed_restore_rolls_back_current(self):
        self.installed()
        backup = Path(tool.uninstall(self.skills)['backup'])
        self.change_source()
        self.installed()
        current = tool.digest(self.dest / tool.MANIFEST)
        real_replace = os.replace
        def fail_backup(src, dst):
            if Path(src) == backup:
                raise OSError('restore failure')
            return real_replace(src, dst)
        with patch.object(tool.os, 'replace', side_effect=fail_backup):
            with self.assertRaises(OSError):
                tool.restore(backup, self.skills, replace=True)
        self.assertEqual(tool.digest(self.dest / tool.MANIFEST), current)

    def test_busy_lock_is_respected(self):
        self.skills.parent.mkdir(parents=True)
        lock = self.skills.parent / '.project-install.lock'
        lock.write_text('another-process', encoding='utf-8')
        with self.assertRaisesRegex(tool.ProjectError, 'lock exists'):
            self.installed()
        self.assertEqual(lock.read_text(encoding='utf-8'), 'another-process')
        self.assertFalse(self.dest.exists())

    def test_linked_source_rejected(self):
        linked = self.root / 'linked'
        self.link(linked, self.package, True)
        with self.assertRaises(tool.ProjectError):
            tool.validate(linked)

    def test_linked_package_file_rejected(self):
        outside = self.root / 'outside'
        outside.write_text('secret', encoding='utf-8')
        self.link(self.package / 'extra', outside)
        with self.assertRaises(tool.ProjectError):
            tool.seal(self.package)

    def test_linked_destination_rejected(self):
        self.skills.mkdir(parents=True)
        other = self.root / 'other'
        other.mkdir()
        self.link(self.dest, other, True)
        with self.assertRaises(tool.ProjectError):
            self.installed()
        self.assertFalse(list(other.iterdir()))

    def test_broken_link_destination_rejected(self):
        self.skills.mkdir(parents=True)
        self.link(self.dest, self.root / 'missing', True)
        with self.assertRaises(tool.ProjectError):
            self.installed()

    def test_nested_installed_link_rejected(self):
        self.installed()
        outside = self.root / 'outside'
        outside.write_text('retain', encoding='utf-8')
        self.link(self.dest / 'extra', outside)
        with self.assertRaises(tool.ProjectError):
            tool.uninstall(self.skills)
        self.assertEqual(outside.read_text(encoding='utf-8'), 'retain')

    def test_source_destination_overlap_rejected(self):
        with self.assertRaisesRegex(tool.ProjectError, 'overlap'):
            tool.install(self.package, self.package / 'skills')

    def test_destination_must_be_skills_directory(self):
        with self.assertRaisesRegex(tool.ProjectError, 'named skills'):
            tool.install(self.package, self.root / 'arbitrary')

    def test_unrelated_config_is_untouched(self):
        config = self.skills.parent / 'config.toml'
        config.parent.mkdir(parents=True)
        config.write_text('user configuration', encoding='utf-8')
        self.installed()
        tool.uninstall(self.skills)
        self.assertEqual(config.read_text(encoding='utf-8'), 'user configuration')

    def test_receipt_drift_detected(self):
        self.installed()
        receipt = self.dest / tool.RECEIPT
        data = tool.load_json(receipt)
        data['manifest_sha256'] = 'f' * 64
        tool.write_json(receipt, data)
        with self.assertRaisesRegex(tool.ProjectError, 'receipt'):
            tool.status(self.skills)

    def test_deterministic_zip_and_extraction(self):
        a = tool.pack(self.package, self.root / 'a.zip')
        b = tool.pack(self.package, self.root / 'b.zip')
        self.assertEqual(a['sha256'], b['sha256'])
        out = self.root / 'extracted'
        with zipfile.ZipFile(a['path']) as archive:
            archive.extractall(out)
        self.assertTrue(tool.validate(out / 'project')['valid'])

    def test_zip_excludes_installation_receipt(self):
        self.installed()
        packed = tool.pack(self.dest, self.root / 'installed.zip')
        with zipfile.ZipFile(packed['path']) as archive:
            self.assertNotIn('project/' + tool.RECEIPT, archive.namelist())

    def test_cannot_pack_inside_package(self):
        with self.assertRaises(tool.ProjectError):
            tool.pack(self.package, self.package / 'nested.zip')

    def test_cli_smoke_and_repo_scope(self):
        command = [sys.executable, str(ROOT / 'scripts/project_tool.py'), '--package', str(self.package)]
        repo = self.root / 'repo with spaces'
        run = subprocess.run(command + ['install', '--repo', str(repo)], capture_output=True, text=True, timeout=15)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue((repo / '.agents/skills/project/SKILL.md').is_file())
        run = subprocess.run(command + ['status', '--repo', str(repo)], capture_output=True, text=True, timeout=15)
        self.assertEqual(json.loads(run.stdout)['action'], 'verified-files')
        run = subprocess.run(command + ['install', '--skills-dir', str(self.root / 'bad')], capture_output=True, text=True, timeout=15)
        self.assertEqual(run.returncode, 1)
        self.assertIn('error', json.loads(run.stderr))

    def test_status_absent_does_not_create_directories(self):
        self.assertEqual(tool.status(self.skills)['action'], 'not-installed')
        self.assertFalse(self.skills.parent.exists())


if __name__ == '__main__':
    unittest.main()
