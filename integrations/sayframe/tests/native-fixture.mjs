import { prepareHandoff, reviewSubjectDigest, approveHandoff, TOPICS } from '../../../skills/project/scripts/sayframe.mjs';
export const fixture = {
  projectId: 'fixture-next-chapter', title: 'Next Chapter', revisionId: 'revision-7', acceptedAt: '2026-09-28T10:00:00.000Z',
  sections: {
    purpose: 'Help a book club choose its next read without social pressure. Private ballots; aggregate totals only. No individual voting histories, invitations or purchases.',
    design: 'An editorial polling workspace. Create a poll, select one book, confirm a private vote, and see totals only after closing. Keyboard focus stays visible. Empty, invalid, offline and retry states preserve the vote draft. Warm paper, plum ink and cobalt actions.',
    approach: 'A local browser app with separate poll, ballot and tally components. IndexedDB retains ballots and closing state. No external provider. Closing is idempotent; no individual ballot is displayed. Tests cover create, vote, retry, close, retained data and keyboard use. Deliver a local build with checks. Multi-device sync is out of scope; untested participant outcomes remain unknown. 🦊',
  },
};
export async function draftFixture({ open = false } = {}) {
  const subject = { snapshot: fixture,
    connector: { repository: 'https://github.com/bohselecta/OAI-Project-Skill', commit: 'c6c53eec1355747c12f0ab75f4686f06780f949c', version: '1.0.0' },
    target: { workspace: '/tmp/product workspace', repository: 'https://github.com/example/product', baseCommit: null },
    scope: { action: 'Build this local test product', permitted: ['Implement and test locally'], prohibited: ['No purchases or external outreach'], spending: 'None', externalActions: 'None', stopConditions: ['Wait for Proceed before implementation', 'Stop after evidence-backed local acceptance'] },
  };
  return prepareHandoff({ ...subject, review: { subjectDigest: await reviewSubjectDigest(subject), method: 'manual', reviewer: 'TEST FIXTURE — not user review', reviewedAt: '2026-09-29T10:00:00.000Z',
    coverage: Object.entries(TOPICS).map(([topic, section]) => ({ topic, state: open ? 'open' : 'covered', rationale: 'Synthetic transport test evidence; not a participant or semantic evaluation.', refs: open ? [] : [{ section, quote: fixture.sections[section] }] })), findings: [] } });
}
export async function approvedFixture() {
  const draft = await draftFixture();
  return approveHandoff(draft, { expectedIntentDigest: draft.envelope.intentDigest, currentSnapshotDigest: draft.envelope.snapshotDigest, approvedAt: '2026-09-29T11:00:00.000Z' });
}
