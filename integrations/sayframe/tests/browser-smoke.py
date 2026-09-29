"""Optional browser SDK smoke; not a SayFrame UI or Codex host test.

Requires Python Playwright and an installed Chromium. Run from repository root:
  python integrations/sayframe/tests/browser-smoke.py [--chromium /path/to/chromium]
No package installation or network access is performed by this script.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chromium')
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as p:
            options = {'headless': True}
            if args.chromium:
                options['executable_path'] = args.chromium
            browser = p.chromium.launch(**options)
            page = browser.new_page()
            page.goto(f'http://127.0.0.1:{server.server_port}/')
            result = page.evaluate('''async () => {
              const sdk = await import('/skills/project/scripts/sayframe.mjs');
              const input = await (await fetch('/integrations/sayframe/fixtures/next-chapter.json')).json();
              const draft = await sdk.prepareHandoff(input);
              if (draft.envelope.approval !== null) throw Error('Draft was approved');
              const approved = await sdk.approveHandoff(draft, {
                expectedIntentDigest: draft.envelope.intentDigest,
                currentSnapshotDigest: draft.envelope.snapshotDigest,
                approvedAt: '2026-09-29T12:02:00.000Z'
              });
              const files = await sdk.exportFiles(approved);
              const read = await sdk.readFiles(files, {forBuild:true});
              if (JSON.stringify(read) !== JSON.stringify(approved)) throw Error('Round trip changed data');
              for (const value of Object.values(input.snapshot.sections)) {
                if (!files['proposal.md'].includes(value)) throw Error('Prose was lost');
              }
              files['proposal.md'] += '\\nUnexpected text';
              let rejected = false;
              try { await sdk.readFiles(files, {forBuild:true}); } catch { rejected = true; }
              if (!rejected) throw Error('Tamper was accepted');
              return {result:'PASS', mode:'browser SDK fixture smoke', prosePreserved:true,
                roundTrip:true, tamperRejected:true, executed:false};
            }''')
            result['browser'] = browser.version
            print(json.dumps(result, indent=2))
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == '__main__':
    main()
