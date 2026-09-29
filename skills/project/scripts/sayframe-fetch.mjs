#!/usr/bin/env node
/** Explicit post-Proceed staging; not an MCP write tool. Never overwrite a workspace file. */
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fetchRecord } from './sayframe-remote.mjs';
import { exportFiles } from './sayframe.mjs';
import { privateDirectory } from './private-fs.mjs';
const [id, digest, parent] = process.argv.slice(2);
if (!id || !digest || !parent || !path.isAbsolute(parent)) {
  process.stderr.write('Usage: node sayframe-fetch.mjs <handoff-id> <intent-digest> <absolute-staging-directory>\n'); process.exitCode = 2;
} else {
  try {
    const record = await fetchRecord(id, digest);
    await privateDirectory(parent);
    const folder = path.join(parent, id);
    await fs.mkdir(folder, { mode: 0o700 }); // EEXIST is intentionally not overwritten.
    const files = await exportFiles(record.bundle);
    for (const [name, content] of Object.entries(files)) await fs.writeFile(path.join(folder, name), content, { flag: 'wx', mode: 0o600 });
    process.stdout.write(JSON.stringify({ directory: folder, intentDigest: digest, executionStarted: false }) + '\n');
  } catch (error) { process.stderr.write('Staging failed; no build started. ' + error.message + '\n'); process.exitCode = 1; }
}
