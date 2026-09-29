"""Repository/distribution consistency checks; not native plugin import tests."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_plugin_identity_and_version_match(self):
        plugin = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
        manifest = json.loads((ROOT / 'skills/project/manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(plugin['name'], 'project')
        self.assertEqual(plugin['version'], manifest['version'])
        self.assertEqual(plugin['version'], (ROOT / 'VERSION').read_text().strip())
        self.assertEqual(plugin['$schema'], 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json')
        self.assertEqual(plugin['license'], 'MIT')
    def test_explicit_read_only_transport_without_implicit_hooks(self):
        for path in ('.mcp.json', 'hooks', '.codex/config.toml'):
            self.assertFalse((ROOT / path).exists(), path)
        self.assertEqual(sorted(p.name for p in (ROOT / 'skills').iterdir() if p.is_dir()), ['project', 'sayframe-intake'])
        config = json.loads((ROOT / 'mcp.json').read_text(encoding='utf-8'))
        self.assertEqual(config, {'$schema':'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json', 'mcpServers': {'sayframe': {
            'type':'stdio', 'command': 'node', 'args': ['skills/project/scripts/sayframe-mcp.mjs'], 'cwd': '${PLUGIN_ROOT}'}}})
        self.assertNotIn('env', config['mcpServers']['sayframe'])
        intake = (ROOT / 'skills/sayframe-intake/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('Proceed', intake)
        self.assertIn('Do not clone', intake)
        marketplace = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
        self.assertEqual(marketplace['plugins'][0]['name'], 'project')
        self.assertEqual(marketplace['plugins'][0]['source'], {'source':'local', 'path':'./'})
    def test_license_in_standalone_package(self):
        self.assertEqual((ROOT / 'LICENSE').read_bytes(), (ROOT / 'skills/project/LICENSE').read_bytes())
    def test_document_links_resolve_locally(self):
        for path in list(ROOT.glob('*.md')) + list((ROOT / 'docs').glob('*.md')) + [ROOT / 'evals/README.md']:
            for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if '://' in link or link.startswith('#'): continue
                self.assertTrue((path.parent / link.split('#')[0]).exists(), f'{path}: {link}')
    def test_scenarios_unique_and_unrun(self):
        data = json.loads((ROOT / 'evals/scenarios.json').read_text())
        self.assertEqual(data['status'], 'NOT_RUN')
        ids = [s['id'] for s in data['scenarios']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 15)
    def test_example_evidence_never_prefills_success(self):
        data = json.loads((ROOT / 'evals/run-record.example.json').read_text())
        self.assertTrue(data['example_only'])
        self.assertEqual(data['outcome'], 'NOT_RUN')
        self.assertTrue(all(v is None for v in data['usage'].values()))


if __name__ == '__main__':
    unittest.main()
