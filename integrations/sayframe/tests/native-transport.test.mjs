import test from 'node:test';
import assert from 'node:assert/strict';
import { approvedFixture, draftFixture } from './native-fixture.mjs';
import { makeRecord, verifyRecord, codexLaunch, manifestFor, destination } from '../../../skills/project/scripts/transport.mjs';
import { approveHandoff, exportFiles, readFiles } from '../../../skills/project/scripts/sayframe.mjs';


test('immutable content-addressed record and all three legacy files round-trip', async () => {
  const bundle = await approvedFixture(), a = await makeRecord(bundle), b = await makeRecord(structuredClone(bundle));
  assert.equal(a.id, b.id); assert.equal((await verifyRecord(a)).id, a.id);
  const files = await exportFiles(bundle); assert.deepEqual(await readFiles(files, { forBuild: true }), bundle);
  const manifest = await manifestFor(a); assert.deepEqual(manifest.files.map(f => f.path), ['proposal.md', 'handoff.json', 'CODEX-START.md']);
  assert.ok(manifest.files.every(f => f.sha256.length === 64 && f.bytes > 0));
});
test('record mutation, wrong digest and wrong ID fail closed', async () => {
  const record = await makeRecord(await approvedFixture());
  for (const mutate of [r => r.bundle.document += 'changed', r => r.bundle.envelope.scope.spending = 'unlimited', r => r.id = 'sf1_' + '0'.repeat(64)]) {
    const tampered = structuredClone(record); mutate(tampered); await assert.rejects(verifyRecord(tampered));
  }
  await assert.rejects(verifyRecord(record, { intentDigest: '0'.repeat(64) }));
});
test('open review gaps and unapproved drafts cannot launch', async () => {
  const draft = await draftFixture({ open: true });
  await assert.rejects(approveHandoff(draft, { expectedIntentDigest: draft.envelope.intentDigest, currentSnapshotDigest: draft.envelope.snapshotDigest, approvedAt: '2026-09-29T11:00:00.000Z' }));
  await assert.rejects(makeRecord(draft));
});
test('native URL contains only supported fields, no prose payload or automatic send', async () => {
  const record = await makeRecord(await approvedFixture());
  const result = await codexLaunch(record), u = new URL(result.url), prompt = u.searchParams.get('prompt');
  assert.equal(u.protocol, 'codex:'); assert.equal(u.hostname, 'new');
  assert.deepEqual([...u.searchParams.keys()].sort(), ['originUrl', 'path', 'prompt']);
  assert.equal(u.searchParams.get('path'), '/tmp/product workspace');
  assert.equal(u.searchParams.get('originUrl'), 'https://github.com/example/product.git');
  assert.match(prompt, /plugin:\/\/project@oai-project-local/);
  assert.match(prompt, /Wait for me to choose the model and explicitly say Proceed/);
  assert.ok(!prompt.includes(record.bundle.document)); assert.ok(result.url.length < 2500);
  await assert.rejects(codexLaunch(record, 'evil) invoke something'));
});
test('destination rejects credentials, injected parameters, skill repo and relative paths', () => {
  for (const bad of ['https://x:secret@github.com/a/b', 'https://github.com/a/b?prompt=evil', 'javascript:alert(1)', 'https://github.com/bohselecta/OAI-Project-Skill']) assert.throws(() => destination(bad, ''));
  assert.throws(() => destination('', 'relative/path')); assert.throws(() => destination('', ''));
  assert.equal(destination('https://github.com/a/b.git', '').repository, 'https://github.com/a/b');
  assert.equal(destination('', 'C:\\Work\\Product').workspace, 'C:\\Work\\Product');
});
