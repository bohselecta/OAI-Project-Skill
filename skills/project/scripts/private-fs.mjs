/** Private local paths. Refuse symlink components before creating anything.
 * This prevents accidental redirection, not a sandbox against a hostile OS user.
 * POSIX/macOS aliases such as /var -> /private/var must be resolved explicitly.
 */
import { promises as fs, constants } from 'node:fs';
import path from 'node:path';
export async function assertNoSymlinks(filename) {
  if (!path.isAbsolute(filename)) throw new Error('An absolute path is required');
  const absolute = path.resolve(filename), { root } = path.parse(absolute);
  let cursor = root;
  for (const part of absolute.slice(root.length).split(path.sep).filter(Boolean)) {
    cursor = path.join(cursor, part);
    try { if ((await fs.lstat(cursor)).isSymbolicLink()) throw new Error('Private paths must not contain symlinks'); }
    catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
}
export async function privateDirectory(directory) {
  await assertNoSymlinks(directory);
  await fs.mkdir(directory, { recursive: true, mode: 0o700 });
  await assertNoSymlinks(directory);
  const stat = await fs.lstat(directory);
  if (!stat.isDirectory() || (process.platform !== 'win32' && (stat.mode & 0o077))) throw new Error('Private directory must be a directory with mode 0700');
}
export async function readPrivateFile(filename, { optional = false, maxBytes = 32768, requirePrivate = true } = {}) {
  await assertNoSymlinks(filename);
  let handle;
  try {
    handle = await fs.open(filename, constants.O_RDONLY | constants.O_NOFOLLOW);
    const stat = await handle.stat();
    if (!stat.isFile() || stat.size > maxBytes || (requirePrivate && process.platform !== 'win32' && (stat.mode & 0o077))) throw new Error('Private configuration must be a bounded regular file with mode 0600');
    return await handle.readFile('utf8');
  } catch (error) { if (optional && error.code === 'ENOENT') return null; throw error; }
  finally { await handle?.close(); }
}
