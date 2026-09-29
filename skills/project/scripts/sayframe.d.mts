export type Section = 'purpose' | 'design' | 'approach';
export type Topic = 'outcome' | 'scope' | 'journeys' | 'presentation' | 'states' | 'components' | 'data' | 'interfaces' | 'invariants' | 'acceptance' | 'delivery' | 'risks';
export interface Snapshot { projectId: string; title: string; revisionId: string; acceptedAt: string; sections: Record<Section, string> }
export interface Reference { section: Section; quote: string }
export interface Coverage { topic: Topic; state: 'covered' | 'not-applicable' | 'open'; rationale: string; refs: Reference[] }
export interface Finding { id: string; kind: 'contradiction' | 'tradeoff' | 'unknown'; blocking: boolean; state: 'open' | 'resolved'; summary: string; refs: Reference[] }
export interface Review { subjectDigest: string; method: 'manual' | 'model' | 'fixture'; reviewer: string; reviewedAt: string; coverage: Coverage[]; findings: Finding[] }
export interface Connector { repository: string; commit: string; version: string }
export interface Target { workspace: string; repository: string | null; baseCommit: string | null }
export interface Scope { action: string; permitted: string[]; prohibited: string[]; spending: string; externalActions: string; stopConditions: string[] }
export interface HandoffInput { snapshot: Snapshot; connector: Connector; target: Target; scope: Scope; review: Review }
export interface Envelope {
  protocol: 'sayframe.project/1'; connector: Connector;
  snapshot: Omit<Snapshot, 'sections'>;
  spans: Record<Section, { start: number; end: number }>;
  documentDigest: string; snapshotDigest: string; target: Target; scope: Scope;
  review: Review; intentDigest: string;
  approval: null | { approvedAt: string; intentDigest: string };
}
export interface Handoff { document: string; envelope: Envelope }
export interface Verification { valid: true; approved: boolean; blockers: string[]; intentDigest: string; snapshotDigest: string; projectId: string; revisionId: string }
export type ExportedFiles = Record<'proposal.md' | 'handoff.json' | 'CODEX-START.md', string>;
export const VERSION: '1.0.0';
export const REPOSITORY: 'https://github.com/bohselecta/OAI-Project-Skill';
export const SECTIONS: readonly Section[];
export const TOPICS: Readonly<Record<Topic, Section>>;
export const FILES: readonly (keyof ExportedFiles)[];
export function sha256(text: string): Promise<string>;
export function snapshotDigest(snapshot: Snapshot): Promise<string>;
export function prepareHandoff(input: HandoffInput): Promise<Handoff>;
export function verifyHandoff(bundle: Handoff, options?: { forBuild?: boolean }): Promise<Verification>;
export function approveHandoff(bundle: Handoff, confirmation: { expectedIntentDigest: string; currentSnapshotDigest: string; approvedAt: string }): Promise<Handoff>;
export function exportFiles(bundle: Handoff): Promise<ExportedFiles>;
export function readFiles(files: ExportedFiles, options?: { forBuild?: boolean }): Promise<Handoff>;
export function loadConnector(options: { repository?: string; ref: string; fetchImpl?: typeof fetch; signal?: AbortSignal }): Promise<{ connector: Connector; manifest: Record<string, string>; authoring: string }>;
export function reviewSubjectDigest(input: Omit<HandoffInput, 'review'>): Promise<string>;
