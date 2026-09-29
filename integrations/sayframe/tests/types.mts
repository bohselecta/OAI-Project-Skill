import { prepareHandoff, exportFiles, approveHandoff, reviewSubjectDigest, type HandoffInput, type ExportedFiles } from '../../../skills/project/scripts/sayframe.mjs';
async function typeContract(input: HandoffInput): Promise<ExportedFiles> {
  const { review, ...subject } = input;
  review.subjectDigest = await reviewSubjectDigest(subject);
  const draft = await prepareHandoff(input);
  const approved = await approveHandoff(draft, { expectedIntentDigest: draft.envelope.intentDigest,
    currentSnapshotDigest: draft.envelope.snapshotDigest, approvedAt: new Date().toISOString() });
  return exportFiles(approved);
}
// @ts-expect-error A transport snapshot cannot contain a fake fourth language section.
const notASection: HandoffInput['snapshot']['sections'] = { purpose: 'a', design: 'b', approach: 'c', build: 'go' };
// @ts-expect-error Fixture is not an alternate approval field.
const notApproval: Parameters<typeof approveHandoff>[1] = { approved: true };
void typeContract; void notASection; void notApproval;
