// src/types/note.ts
import type { SvelteComponent } from 'svelte';

export interface NoteMetadata {
	title: string;
	date: string;
	tags?: string[];
	description?: string;
	[key: string]: unknown; // Optional: remove if you want to be strict
}

export interface MarkdownModule {
	default: typeof SvelteComponent;
	metadata?: NoteMetadata;
}
