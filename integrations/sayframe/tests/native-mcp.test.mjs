import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
import { harness } from './native-http-fixture.mjs';
import { approvedFixture } from './native-fixture.mjs';
import { makeRecord } from '../../../skills/project/scripts/transport.mjs';


test('real MCP subprocess initializes, lists only read tools, retrieves and verifies exact HTTP fixture record (not the SayFrame backend)', async () => {
  const h = await harness();
  const bundle = await approvedFixture(), record = await makeRecord(bundle);
  await h.store.publish(bundle);
  const child = spawn(process.execPath, [fileURLToPath(new URL('../../../skills/project/scripts/sayframe-mcp.mjs', import.meta.url))], {
    env: { ...process.env, SAYFRAME_CONNECTOR_CONFIG: h.config }, stdio: ['pipe', 'pipe', 'pipe'],
  });
  const lines = createInterface({ input: child.stdout });
  const pending = new Map(); let count = 0, stderr = '';
  child.stderr.on('data', chunk => { stderr += chunk; });
  lines.on('line', line => { const result = JSON.parse(line); const done = pending.get(result.id); if (done) { pending.delete(result.id); done(result); } });
  const ask = (method, params) => new Promise(resolve => {
    const id = ++count; pending.set(id, resolve); child.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n');
  });
  try {
    assert.equal((await ask('tools/list')).error.code, -32000);
    assert.equal((await ask('initialize', { protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 'test', version: '1' } })).result.protocolVersion, '2025-06-18');
    child.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
    const listing = (await ask('tools/list')).result;
    assert.deepEqual(listing.tools.map(t => t.name), ['get_handoff', 'get_handoff_manifest', 'get_artifact', 'verify_handoff']);
    assert.ok(listing.tools.every(t => t.annotations.readOnlyHint && t.annotations.destructiveHint === false));
    const args = { id: record.id, intentDigest: bundle.envelope.intentDigest };
    const check = (await ask('tools/call', { name: 'verify_handoff', arguments: args })).result;
    assert.equal(check.isError, false);
    assert.equal(JSON.parse(check.content[0].text).executionStarted, false);
    const complete = (await ask('tools/call', { name: 'get_handoff', arguments: args })).result;
    assert.deepEqual(JSON.parse(complete.content[0].text).record, record);
    const forbidden = (await ask('tools/call', { name: 'execute_build', arguments: args })).result;
    assert.equal(forbidden.isError, true);
    await h.store.revoke(record.id);
    const revoked = (await ask('tools/call', { name: 'verify_handoff', arguments: args })).result;
    assert.equal(revoked.isError, true);
    assert.match(revoked.content[0].text, /410/);
    assert.ok(!JSON.stringify(revoked).includes(h.readKey));
    assert.equal(stderr, '');
  } finally { lines.close(); child.kill(); await new Promise(resolve => child.once('exit', resolve)); await h.close(); }
});
