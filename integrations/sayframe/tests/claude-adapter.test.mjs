/** Exercise the shipped Claude package after copying it outside the repository. */
import test from 'node:test';
import assert from 'node:assert/strict';
import * as fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
const root = fileURLToPath(new URL('../../../', import.meta.url));

test('isolated Claude package verifies approved bundles and rejects drafts and tampering', async t => {
  const temp = await fs.realpath(await fs.mkdtemp(path.join(os.tmpdir(), 'claude-project-')));
  t.after(() => fs.rm(temp, { recursive: true, force: true }));
  const skill = path.join(temp, '.claude', 'skills', 'project');
  await fs.cp(path.join(root, '.claude/skills/project'), skill, { recursive: true });
  const { prepareHandoff, approveHandoff, exportFiles } = await import(pathToFileURL(path.join(skill, 'scripts/sayframe.mjs')));
  const input = JSON.parse(await fs.readFile(path.join(root, 'integrations/sayframe/fixtures/next-chapter.json'), 'utf8'));
  const draft = await prepareHandoff(input);
  const approved = await approveHandoff(draft, {
    expectedIntentDigest: draft.envelope.intentDigest,
    currentSnapshotDigest: draft.envelope.snapshotDigest,
    approvedAt: '2026-09-30T00:00:00.000Z',
  });
  const bundle = path.join(temp, 'bundle');
  await fs.mkdir(bundle);
  async function write(value) {
    for (const [name, text] of Object.entries(await exportFiles(value))) await fs.writeFile(path.join(bundle, name), text);
  }
  const cli = (...args) => spawnSync(process.execPath, [path.join(skill, 'scripts/sayframe-cli.mjs'), 'verify', bundle, ...args], { encoding: 'utf8', cwd: temp });
  await write(draft);
  assert.equal(cli().status, 0);
  assert.notEqual(cli('--for-build').status, 0);
  await write(approved);
  const valid = cli('--for-build');
  assert.equal(valid.status, 0, valid.stderr);
  assert.equal(JSON.parse(valid.stdout).executed, false);
  await fs.appendFile(path.join(bundle, 'proposal.md'), '\nTampered scope');
  assert.notEqual(cli('--for-build').status, 0);
  assert.equal(await fs.stat(path.join(temp, '.project')).catch(() => null), null);
});
