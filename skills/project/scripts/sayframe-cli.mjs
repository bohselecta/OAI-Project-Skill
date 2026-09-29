#!/usr/bin/env node
/** Local verification/import only. Never invokes Codex, Git, a shell, or a model. */
import * as fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { FILES, readFiles, verifyHandoff, sha256 } from './sayframe.mjs';

async function realPath(input) {
  const absolute = path.resolve(input);
  for (let item = absolute; ; item = path.dirname(item)) {
    try {
      const stat = await fs.lstat(item);
      if (stat.isSymbolicLink()) throw new Error('Refusing linked path: ' + item);
    } catch (e) { if (e.code !== 'ENOENT') throw e; }
    if (path.dirname(item) === item) break;
  }
  return absolute;
}
async function load(directory, options) {
  directory = await realPath(directory);
  const entries = (await fs.readdir(directory)).sort();
  if (entries.join('|') !== [...FILES].sort().join('|')) throw new Error('Bundle must contain exactly the three connector files');
  const files = {};
  for (const name of FILES) {
    const file = await realPath(path.join(directory, name));
    const stat = await fs.lstat(file);
    if (!stat.isFile() || stat.size > 2 * 1024 * 1024) throw new Error('Invalid or oversized bundle file');
    const bytes = await fs.readFile(file);
    files[name] = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  }
  return { files, bundle: await readFiles(files, options) };
}
export async function run(args) {
  const forBuild = args.includes('--for-build');
  const positional = args.filter(a => a !== '--for-build');
  const [command, source, workspace] = positional;
  if (!['verify', 'import'].includes(command) || !source || args.filter(a => a === '--for-build').length > 1
      || positional.length !== (command === 'import' ? 3 : 2)) {
    throw new Error('Usage: node sayframe-cli.mjs verify BUNDLE [--for-build] | import BUNDLE WORKSPACE [--for-build]');
  }
  const { files, bundle } = await load(source, { forBuild });
  const result = await verifyHandoff(bundle, { forBuild });
  if (command === 'verify') return { ...result, executed: false };
  const root = await realPath(workspace);
  if (!(await fs.stat(root)).isDirectory()) throw new Error('Workspace must already exist');
  const parent = await realPath(path.join(root, '.project', 'sayframe'));
  await fs.mkdir(parent, { recursive: true });
  const lockPath = await realPath(path.join(parent, '.import.lock'));
  const lock = await fs.open(lockPath, 'wx'); // Concurrent imports fail safely; never steal a stale lock.
  let temp = null;
  try {
    const packageDigest = await sha256(JSON.stringify(files));
    const destination = await realPath(path.join(parent, 'handoff-' + packageDigest.slice(0, 24)));
    try {
      await fs.lstat(destination);
      const existing = await load(destination, { forBuild });
      if (JSON.stringify(existing.files) !== JSON.stringify(files)) throw new Error('Existing handoff conflicts; nothing was overwritten');
      return { ...result, directory: destination, alreadyPresent: true, executed: false };
    } catch (e) { if (e.code !== 'ENOENT') throw e; }
    temp = await fs.mkdtemp(path.join(parent, '.incoming-'));
    for (const name of FILES) await fs.writeFile(path.join(temp, name), files[name], { encoding: 'utf8', flag: 'wx' });
    // Under the import lock, never replace any pre-existing destination, even an empty directory.
    try { await fs.lstat(destination); throw new Error('Destination appeared during import; retry after inspection'); }
    catch (e) { if (e.code !== 'ENOENT') throw e; }
    await fs.rename(temp, destination);
    temp = null;
    return { ...result, directory: destination, alreadyPresent: false, executed: false };
  } finally {
    if (temp) await fs.rm(temp, { recursive: true, force: true });
    await lock.close();
    await fs.unlink(lockPath);
  }
}
if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  run(process.argv.slice(2)).then(result => console.log(JSON.stringify(result, null, 2)))
    .catch(error => { console.error('SayFrame import: ' + error.message); process.exitCode = 1; });
}
