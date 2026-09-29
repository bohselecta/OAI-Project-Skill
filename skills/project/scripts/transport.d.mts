import type { Handoff, Target } from './sayframe.d.mts';
export const TRANSPORT: 'sayframe.transport/1';
export const PLUGIN: string;
export const ID_PATTERN: RegExp;
export const MAX_BYTES: number;
export interface TransportRecord { protocol: typeof TRANSPORT; id: string; bundle: Handoff }
export function canonical(value: unknown): string;
export function makeRecord(bundle: Handoff): Promise<TransportRecord>;
export function verifyRecord(record: TransportRecord, expected?: { id?: string; intentDigest?: string }): Promise<TransportRecord>;
export function manifestFor(record: TransportRecord): Promise<{ protocol: string; id: string; revisionId: string; intentDigest: string; connector: Handoff['envelope']['connector']; target: Target; files: { path: string; bytes: number; sha256: string }[] }>;
export function normalizeRepository(value: string): string;
export function isAbsoluteWorkspace(value: string): boolean;
export function destination(repository?: string, workspace?: string): Target;
export function codexLaunch(record: TransportRecord, pluginReference?: string): Promise<{ url: string; prompt: string }>;
