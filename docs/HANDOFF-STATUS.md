# Native handoff verification — status update

Scope: Full-application and cross-repository verification executed on 2026-09-29.

The cross-repository suite passed 18 Node tests against actual HTTP/auth/storage and an
actual stdio MCP child process. The independently runnable subsets passed 14 SayFrame tests
and 6 Project tests; those overlap, and must not be summed as unique coverage.

The production handoff dialog passed 10 real-Chromium checks in an offline harness at
1440px and 390px with keyboard and reduced motion.

Complete Project archive verification passed: 58 Python regressions, 40 existing connector tests, 6 native tests, strict connector declarations and sealed 20-file package validation (version 1.1.0). These checks ran on the exact a7c5dff source plus the delivered changes; native host discovery remains NOT_RUN.

Full SayFrame application verification ran and passed cleanly against locked dependencies:
- Static type check: `npm run typecheck` (0 errors)
- Linter: `npm run lint` (0 warnings, 0 errors)
- Unit tests: `npm run test` (9/9 Vitest invariant tests passing)
- Production build: `npm run build` (Next.js App Router 15.5 production compilation succeeded)
- Handoff test suite: `npm run test:handoff` (14/14 Node tests passing)
- Playwright E2E browser journeys: `npm run test:e2e` (9/9 Chromium journeys passing, verifying in-place edits, atomic revisions, IndexedDB approval, 3-file cryptographic ZIP export, sample switching, cross-tab CAS stale editor refusal, same-project revision history/restore, project switching during in-flight requests, backup relational remapping, and fail-closed Next HTTP adapter behavior)

Native Host Status:
Native `codex` binary is not installed on this local system (`ChatGPT.app` is present in `/Applications`). Local plugin configuration, read-only MCP transport, and protocol fixtures have been verified. The live desktop application launch/proceed trial is recorded as NOT_RUN.
Live provider calls remain fail-closed without explicit authorization (`SAYFRAME_ALLOW_LIVE=true` and valid budget).
Persistent storage uses local Node host storage; Vercel deployment correctly fails closed to ZIP export.

