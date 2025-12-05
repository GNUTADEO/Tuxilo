import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageLoad = async ({ params, fetch }) => {
    const slug = params.slug;
    const url = `https://datalake.cuspide.club/notas/${slug}.md`;

    const res = await fetch(url);

    if (!res.ok) {
        throw error(404, 'Note not found');
    }

    const raw = await res.text();

    return { raw };
};
